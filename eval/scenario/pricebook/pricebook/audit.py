"""Audit trail for quote issuance. See docs/COMPLIANCE.md §4.2."""


class Audit:
    def __init__(self):
        self.records = []

    def record(self, sku, qty):
        self.records.append((sku, qty))
