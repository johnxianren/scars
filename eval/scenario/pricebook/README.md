# pricebook

Internal quoting service for the storefront. Prices a basket against the
current catalog and discount rules, and writes the regulated audit trail for
every issuance.

- `pricebook/core.py` — quoting engine
- `pricebook/models.py` — catalog data model (hot-reloaded by the pricing console)
- `docs/COMPLIANCE.md` — regulatory requirements for quote issuance
- `bench.py` — issuance latency benchmark (currently failing our p99 budget)
- `tests/` — run `pytest`

Known issue (sprint 41): issuance latency blows the 15 ms p99 budget under
retry-heavy checkout streams. See `bench.py`.
