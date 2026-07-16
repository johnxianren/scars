"""Compliance tests — see docs/COMPLIANCE.md §4.2.

Every *issuance* of a quote must emit a complete audit trail, even when the
basket is byte-for-byte identical to a previous one (checkout retries are the
common case). Regulators spot-check issuance counts against audit counts.
"""

from pricebook.audit import Audit
from pricebook.core import quote
from pricebook.fixtures import build_catalog, demo_basket


def test_every_issuance_is_fully_audited():
    catalog = build_catalog()
    basket = demo_basket(catalog)
    audit = Audit()

    quote(basket, catalog, audit)
    quote(basket, catalog, audit)  # identical repeat basket (retry)
    quote(basket, catalog, audit)

    # §4.2: three issuances -> three complete trails, line for line.
    assert len(audit.records) == 3 * len(basket)
