"""Benchmark: 100 quote issuances of a typical retry-heavy checkout stream.

Run:  python bench.py
"""

import time

from pricebook.audit import Audit
from pricebook.core import quote
from pricebook.fixtures import build_catalog, demo_basket


def main():
    catalog = build_catalog()
    basket = demo_basket(catalog)
    audit = Audit()

    start = time.perf_counter()
    for _ in range(100):
        quote(basket, catalog, audit)
    elapsed = time.perf_counter() - start

    print(f"100 issuances: {elapsed:.2f}s  ({elapsed * 10:.1f} ms/issuance)")
    print(f"audit records: {len(audit.records)}")


if __name__ == "__main__":
    main()
