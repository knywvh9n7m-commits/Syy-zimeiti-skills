#!/usr/bin/env python3
"""Rough request-cost planner. Endpoint/account pricing remains authoritative."""
from __future__ import annotations

import argparse
import math


def estimate(requests: int, low: float | None = None, high: float | None = None):
    if requests < 0:
        raise ValueError("requests must be >= 0")
    if low is None and high is None:
        return None
    if low is None or high is None:
        raise ValueError("provide both --low and --high, or neither")
    if not math.isfinite(low) or not math.isfinite(high) or low < 0 or high < 0 or low > high:
        raise ValueError("invalid price range")
    return requests * low, requests * high


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--requests", type=int, required=True)
    p.add_argument("--low", type=float, help="Explicit assumed low USD price per request")
    p.add_argument("--high", type=float, help="Explicit assumed high USD price per request")
    args = p.parse_args()
    try:
        result = estimate(args.requests, args.low, args.high)
    except ValueError as exc:
        p.error(str(exc))
    print(f"requests: {args.requests}")
    if result is None:
        print("Cost unknown: no unit-price assumption was supplied.")
    else:
        lo, hi = result
        print(f"Assumption-based planning range: ${lo:.4f} - ${hi:.4f}")
    print("Actual current endpoint/account pricing is authoritative.")


if __name__ == "__main__":
    main()
