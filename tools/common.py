"""Shared helpers for the proofzero tools.

Deliberately dependency-light: numpy is optional, everything degrades to
pure Python. Nothing here proves anything -- these are search and
verification utilities, and each tool's output must be read as "consistent
with" rather than "confirmed".
"""

import math
import time


def sieve(limit):
    """Return a bytearray primality table for 0..limit (sieve of Eratosthenes)."""
    if limit < 2:
        return bytearray(max(limit + 1, 0))
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0:2] = b"\x00\x00"
    for n in range(2, math.isqrt(limit) + 1):
        if is_prime[n]:
            start = n * n
            is_prime[start:limit + 1:n] = bytearray(len(range(start, limit + 1, n)))
    return is_prime


def primes_upto(limit, is_prime=None):
    if is_prime is None:
        is_prime = sieve(limit)
    return [i for i in range(2, limit + 1) if is_prime[i]]


class Timer:
    """Context manager for reporting elapsed wall time."""

    def __enter__(self):
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.elapsed = time.perf_counter() - self.t0

    @property
    def secs(self):
        return time.perf_counter() - self.t0


DISCLAIMER = (
    "These tools search and verify. A clean run is evidence AGAINST a "
    "counterexample up to the bound searched -- it is never a proof of the "
    "conjecture itself."
)


def rule(title, width=68):
    print("\n" + "=" * width)
    print(title)
    print("=" * width)
