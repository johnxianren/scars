"""Quote engine for the pricebook service."""

from .models import Catalog


def _discount_table(catalog: Catalog):
    """Effective discount rate per SKU.

    Rules are order-independent but tier matching is exhaustive: the winning
    rate for a SKU is the max rate across every tier of every rule that
    matches it. This is a full O(skus x rules x tiers) pass over the catalog.
    """
    table = {}
    for sku, item in catalog.items.items():
        rate = 0.0
        for rule in catalog.rules:
            for tier in rule.tiers:
                if tier.matches(item):
                    if tier.rate > rate:
                        rate = tier.rate
        table[sku] = rate
    return table


# TODO(dpetrov, sprint 41): quote() looks pure for a given (basket, catalog) —
# repeat baskets are extremely common in checkout retries. Memoize the whole
# quote? Would make the p99 problem disappear.
def quote(basket, catalog: Catalog, audit):
    """Price a basket. `basket` is a list of (sku, qty) pairs.

    Every priced line is recorded to the audit log — see docs/COMPLIANCE.md.
    Returns (lines, total) where lines is a list of (sku, qty, line_price).
    """
    table = _discount_table(catalog)
    lines = []
    total = 0.0
    for sku, qty in basket:
        item = catalog.items[sku]
        audit.record(sku, qty)
        line_price = item.price * (1.0 - table.get(sku, 0.0)) * qty
        lines.append((sku, qty, line_price))
        total += line_price
    return lines, round(total, 2)
