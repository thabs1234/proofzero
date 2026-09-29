// Executes the real <script> from greenboard.html against the real
// problems/_status.json, using a minimal DOM stub. Verifies the render
// logic and that every JSON key the page reads actually exists.
const fs = require("fs");
const path = require("path");

// Resolve paths relative to THIS script, never an absolute machine path,
// so the check runs identically locally and in CI.
const ROOT = path.resolve(__dirname, "..");
const htmlPath = path.join(ROOT, "greenboard.html");
const jsonFile = path.join(ROOT, "problems", "_status.json");

for (const f of [htmlPath, jsonFile]) {
  if (!fs.existsSync(f)) {
    console.error("FAIL: required file missing: " + f);
    process.exit(1);
  }
}
console.log("repo root: " + ROOT);

const html = fs.readFileSync(htmlPath, "utf8");

const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error("FAIL: no <script> block found"); process.exit(1); }
const src = m[1];
console.log("extracted script: " + src.length + " chars");

// ---- minimal DOM stub ----
function mkEl(tag) {
  const el = {
    tagName: tag, _html: "", _text: "", children: [],
    set innerHTML(v) { this._html = v; }, get innerHTML() { return this._html; },
    set textContent(v) { this._text = v; }, get textContent() { return this._text; },
    appendChild(c) { this.children.push(c); return c; },
  };
  return el;
}
const nodes = {};
for (const id of ["cards", "stats", "meta"]) nodes[id] = mkEl("div");

global.document = {
  getElementById: (id) => nodes[id] || null,
  createElement: (t) => mkEl(t),
};

global.fetch = async (url) => {
  if (url.indexOf("_status.json") === -1) throw new Error("unexpected fetch " + url);
  return { ok: true, status: 200, json: async () => JSON.parse(fs.readFileSync(jsonFile, "utf8")) };
};

const errors = [];
process.on("unhandledRejection", (e) => errors.push(e));

// ---- run the page script ----
const fn = new Function(src + "\n//# sourceURL=greenboard.js");
fn();

setTimeout(() => {
  if (errors.length) {
    console.log("\nJS ERRORS:");
    errors.forEach(e => console.log("  " + e));
    process.exit(1);
  }

  const cards = nodes["cards"].children;
  const stats = nodes["stats"].children.map(s => s._html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim());

  console.log("\nSTATS:");
  stats.forEach(s => console.log("  " + s));
  console.log("\nCARDS RENDERED: " + cards.length);

  const data = JSON.parse(fs.readFileSync(jsonFile, "utf8"));
  const byTitle = {};
  for (const c of cards) {
    const t = c._html.match(/<span class="t">([^<]*)<\/span>/);
    const tag = c._html.match(/<span class="tag [^"]*">([^<]*)<\/span>/);
    byTitle[t ? t[1] : "??"] = { tag: tag ? tag[1] : "??", html: c._html };
  }

  const problems = data.problems;
  let fail = 0;
  const seen = [];

  for (const p of problems) {
    seen.push(p.title);
    const r = byTitle[p.title];
    if (!r) { console.log("  MISSING CARD: " + p.title); fail++; continue; }

    // expectation from the real data
    const exp = p.status === "solved" ? "solved"
      : p.verified_here ? "run here"
      : p.verified_elsewhere ? "cited, not reproduced"
      : "no finite check";
    if (r.tag !== exp) { console.log(`  TAG MISMATCH ${p.title}: got "${r.tag}" want "${exp}"`); fail++; }

    // every problem without a local check must SAY SO on its own card
    const noLocal = !p.verified_here && p.status !== "solved";
    const saysNoTool = r.html.includes("no bounded check for this problem");
    if (noLocal && !saysNoTool) { console.log(`  ${p.title}: lacks a local check but card does not disclose it`); fail++; }
    if (!noLocal && saysNoTool) { console.log(`  ${p.title}: falsely claims no local check`); fail++; }

    // a cited bound must never be rendered as a local command
    const showsCmd = r.html.includes("<dt>command</dt>");
    if (showsCmd && !p.verified_here) { console.log(`  ${p.title}: shows a command with no verified_here`); fail++; }
    if (showsCmd && p.verified_here && !r.html.includes(p.verified_here.command.split(" ").pop())) {
      console.log(`  ${p.title}: command text does not match the JSON command`); fail++;
    }

    // runtime must be rendered only when the JSON actually measured one
    if (r.html.includes("runtime") && !(p.verified_here && p.verified_here.runtime_sec != null)) {
      console.log(`  ${p.title}: shows a runtime with none recorded in JSON`); fail++;
    }
  }

  for (const t of Object.keys(byTitle)) if (!seen.includes(t)) { console.log("  EXTRA CARD: " + t); fail++; }

  // No fabricated claim may appear in text the PAGE itself authored.
  // Sourced field values (bounds, caveats, open edges, notes) legitimately
  // contain numbers like 2^68 and words like "proved" — those come from
  // _status.json and are the whole point of the board. So strip every
  // JSON-sourced string out of each card, then require the residue
  // (labels, chrome, the page's own wording) to be free of claims.
  const BANNED = ["2^68", "2^70", "2^69", "4\u00d710^18", "4x10^18", "10^12", "10^13",
                  "10^6 zeros", "breakthrough", "proved", "proof that", "verified to",
                  // An auditor run mutated "never a proof" -> "is a proof" and the
                  // checker passed. Banning "proved"/"proof that" does not catch
                  // the plain assertion, so name the assertion forms too.
                  "is a proof", "are proofs", "constitutes a proof", "this is a proof",
                  "solves the", "solution to the", "we have solved", "fully solved",
                  "settles the", "resolves the"];
  let fail2 = 0;
  for (const p of problems) {
    const r = byTitle[p.title];
    if (!r) continue;
    let residue = r.html;
    const sourced = [];
    if (p.verified_here) for (const v of Object.values(p.verified_here)) sourced.push(String(v));
    if (p.verified_elsewhere) for (const v of Object.values(p.verified_elsewhere)) sourced.push(String(v));
    for (const k of ["open_edge", "note", "caveat", "title", "field", "solved_on",
                     "verified_on_disk", "first_stated", "negative_control", "id", "file", "tool"]) {
      if (p[k] != null) sourced.push(String(p[k]));
    }
    for (const s of sourced) residue = residue.split(s).join(" ");
    residue = residue.replace(/&mdash;/g, " ").replace(/&[a-z]+;/g, " ");
    for (const bad of BANNED) {
      if (residue.indexOf(bad) !== -1) {
        const ctx = residue.slice(Math.max(0, residue.indexOf(bad) - 90),
                                  residue.indexOf(bad) + 90).replace(/<[^>]+>/g, " ");
        console.log(`  PAGE-AUTHORED CLAIM on ${p.title}: "${bad}" :: ${ctx.trim()}`);
        fail2++;
      }
    }
  }
  // NOTE: the fail2 -> fail fold happens AFTER the chrome block below.
  // Folding it here let chrome findings print but never fail the run (M3).

  // Same check across the PAGE CHROME, not just the cards. M3 showed a
  // bound invented in the page's own prose escaped a card-only scan.
  {
    const strip = html
      .replace(/<script>[\s\S]*?<\/script>/g, " ")
      .replace(/<style>[\s\S]*?<\/style>/g, " ")
      .replace(/<[^>]+>/g, " ")
      .replace(/&mdash;/g, " ").replace(/&[a-z]+;/g, " ");
    for (const bad of BANNED) {
      if (strip.indexOf(bad) !== -1) {
        const i = strip.indexOf(bad);
        console.log(`  PAGE-AUTHORED CLAIM in chrome: "${bad}" :: ` +
          strip.slice(Math.max(0, i - 90), i + 90).replace(/\s+/g, " ").trim());
        fail2++;
      }
    }
  }

  // Fold AFTER both the card and chrome scans, so neither can be silently
  // reported-but-not-failed.
  if (fail2) { fail += fail2; }

  // The chrome must AFFIRMATIVELY carry the no-local-check disclosure.
  // An auditor run deleted the sentence outright and every other check
  // still passed, because nothing required the sentence to exist — only
  // that cards not contradict it. Absence of a disclosure is itself a lie.
  {
    const noCheck = problems.filter((p) => !p.tool).length;
    const plain = html
      .replace(/<script>[\s\S]*?<\/script>/g, " ")
      .replace(/<style>[\s\S]*?<\/style>/g, " ")
      .replace(/<[^>]+>/g, " ")
      .replace(/&mdash;/g, " ").replace(/&[a-z]+;/g, " ")
      .replace(/\s+/g, " ");
    if (noCheck > 0) {
      // Require the AFFIRMATIVE disclosure sentence, not merely the legend
      // label "No finite check" (which survives deleting the prose and so
      // made an earlier version of this check vacuous).
      const saysIt = /no (honest )?(finite|bounded) check[^.]{0,80}(is|as) a deliberate absence|computation is not the right tool|deliberate absence, not an oversight/i;
      if (!saysIt.test(plain)) {
        console.log(`  CHROME OMITS the no-local-check disclosure, though ${noCheck} problems have no tool`);
        fail++;
      }
    }
  }

  // Sanity: the sourced residue check must still be able to see a real
  // claim. If stripping removed everything, the test is vacuous.
  const collatz = byTitle["Collatz Conjecture"];
  if (collatz && collatz.html.indexOf("2^68") === -1) {
    console.log("  TEST IS VACUOUS: expected the sourced 2^68 context on the Collatz card");
    fail++;
  }

  console.log("\nproblems=" + problems.length + " cards=" + cards.length +
              " noLocalCheck=" + problems.filter(p => !p.verified_here && p.status !== "solved").length);
  console.log(fail === 0 ? "\nALL RENDER CHECKS PASSED" : "\n" + fail + " CHECK(S) FAILED");
  process.exit(fail === 0 ? 0 : 1);
}, 400);
