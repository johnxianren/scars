"""Data model for the pricebook service.

Note: Catalog and Rule are mutable service objects (rules get hot-reloaded
from the pricing console), so none of these classes define __hash__.
`Catalog.version` is bumped by the loader every time rules or items change.
"""


class Item:
    __slots__ = ("sku", "category", "price", "weight_g")

    def __init__(self, sku, category, price, weight_g):
        self.sku = sku
        self.category = category
        self.price = price
        self.weight_g = weight_g


class Tier:
    __slots__ = ("category", "min_price", "max_weight_g", "rate")

    def __init__(self, category, min_price, max_weight_g, rate):
        self.category = category
        self.min_price = min_price
        self.max_weight_g = max_weight_g
        self.rate = rate

    def matches(self, item):
        return (
            item.category == self.category
            and item.price >= self.min_price
            and item.weight_g <= self.max_weight_g
        )


class Rule:
    __slots__ = ("name", "tiers")

    def __init__(self, name, tiers):
        self.name = name
        self.tiers = tiers


class Catalog:
    """Mutable: the pricing console hot-reloads rules/items in place and
    bumps `version` on every change."""

    def __init__(self, items, rules, version=0):
        self.items = items  # dict sku -> Item
        self.rules = rules  # list of Rule
        self.version = version
