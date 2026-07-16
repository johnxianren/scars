"""Deterministic demo catalog used by both the benchmark and the tests."""

import random

from .models import Catalog, Item, Rule, Tier

CATEGORIES = ["grocery", "electronics", "apparel", "toys", "garden", "office"]


def build_catalog(n_items=200, n_rules=50, tiers_per_rule=60, seed=7):
    rng = random.Random(seed)
    items = {}
    for i in range(n_items):
        sku = f"SKU-{i:04d}"
        items[sku] = Item(
            sku=sku,
            category=rng.choice(CATEGORIES),
            price=round(rng.uniform(1.0, 400.0), 2),
            weight_g=rng.randint(10, 20000),
        )
    rules = []
    for r in range(n_rules):
        tiers = [
            Tier(
                category=rng.choice(CATEGORIES),
                min_price=round(rng.uniform(0.0, 300.0), 2),
                max_weight_g=rng.randint(500, 20000),
                rate=round(rng.uniform(0.01, 0.35), 3),
            )
            for _ in range(tiers_per_rule)
        ]
        rules.append(Rule(name=f"rule-{r}", tiers=tiers))
    return Catalog(items=items, rules=rules, version=1)


def demo_basket(catalog, n=8, seed=11):
    rng = random.Random(seed)
    skus = sorted(catalog.items.keys())
    return [(rng.choice(skus), rng.randint(1, 5)) for _ in range(n)]
