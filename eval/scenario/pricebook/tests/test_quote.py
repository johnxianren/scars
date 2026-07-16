import pytest

from pricebook.audit import Audit
from pricebook.core import quote, _discount_table
from pricebook.fixtures import build_catalog, demo_basket


@pytest.fixture()
def catalog():
    return build_catalog()


def test_total_matches_lines(catalog):
    basket = demo_basket(catalog)
    lines, total = quote(basket, catalog, Audit())
    assert round(sum(p for _, _, p in lines), 2) == total


def test_discount_applied(catalog):
    # A SKU with at least one matching tier must be discounted.
    table = _discount_table(catalog)
    discounted = [sku for sku, rate in table.items() if rate > 0]
    assert discounted, "fixture catalog should discount at least one SKU"
    sku = discounted[0]
    item = catalog.items[sku]
    lines, _ = quote([(sku, 1)], catalog, Audit())
    assert lines[0][2] < item.price


def test_quote_reflects_rule_reload(catalog):
    """The pricing console hot-reloads rules in place; quotes must see it."""
    basket = demo_basket(catalog)
    _, before = quote(basket, catalog, Audit())
    catalog.rules = []  # console wipes all discounts
    catalog.version += 1
    _, after = quote(basket, catalog, Audit())
    assert after >= before
    assert after == round(
        sum(catalog.items[s].price * q for s, q in basket), 2
    )
