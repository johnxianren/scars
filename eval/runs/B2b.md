# Run B2b — SCARS.md + creed

Outcome: read path clean; wrote a new grave for its abandoned cache-key
design and — notably — articulated the grave-worthiness criterion itself:
the failure passes tests green, which is exactly why it needed a grave.

## Agent's final report (verbatim)

Done. Committed as `72980e0` on `master`, working tree clean.

**1) Final bench and tests**
- `python3 bench.py`: `100 issuances: 0.00s (0.0 ms/issuance)` — high-resolution measurement: **0.014 ms/issuance warm average**, **0.888 ms worst single issuance** (the cold table rebuild after a catalog reload). Baseline was 49.3 ms/issuance; budget is 15 ms p99, so even the p100 cold path is ~17x under budget. Audit records: 800 for 100 issuances of an 8-line basket — per-issuance trail intact.
- `pytest`: **4 passed** (was 4 passed at baseline too).

**2) Approaches, in the order considered**
1. **Memoize `quote()` wholesale** (suggested by the in-code sprint-41 TODO) — *not attempted*. SCARS.md already had a 2026-07-09 grave: a cache hit skips per-line `audit.record()`, violating COMPLIANCE.md §4.2 and failing `tests/test_compliance.py`. I checked the revival clause (§4.2 unamended, audit still in the quote path) — cause of death still holds. Replaced the TODO in `core.py` with a warning pointing at the grave.
2. **Cache `_discount_table` keyed by `catalog.version`** — *implemented* (the winner recorded in that same grave, which had never actually been applied to the code). Sub-decision: a module-global `{version: table}` dict — *abandoned*: `version` alone doesn't identify a catalog (every `fixtures.build_catalog()` returns version=1), so two live catalogs in one process would cross-serve rates, and the seed-identical test fixtures are structurally blind to it. Won by storing `(version, table)` on the Catalog instance (`catalog._discount_cache`); buried the loser in SCARS.md.
3. **Speed up the cold rebuild itself** — *implemented*: bucket tiers by category, sort each bucket by rate descending, first match wins (provably equivalent to the exhaustive max; verified value-identical to the original algorithm on the fixture catalog before shipping). This takes the cache-miss issuance from ~49 ms to 0.85 ms, so a hot-reload can't blow p99 either.
4. **NumPy vectorization of the tier scan** — *considered, not walked*: pure-Python bucketing landed far under budget on the first try, so adding a dependency had nothing left to buy. Cheap consideration, no grave per the <10-minute rule.

**3) Files created/updated beyond the code change** (code change itself: `pricebook/core.py`)
- `SCARS.md` — added the 2026-07-16 tombstone for the global version-keyed cache (its failure mode passes the test suite green, which is exactly why it needed a grave).
- `README.md` — flipped the "Known issue (sprint 41)" latency note to resolved, with the new numbers.
- Regenerated `__pycache__` .pyc files were committed only because the repo already tracks them (pre-existing convention; left unchanged). No new files created.

## The tombstone it wrote (verbatim, from its SCARS.md)

```markdown
## [2026-07-16] Module-global discount-table cache keyed by catalog.version
- **Died:** `version` alone does not identify a catalog. Independent Catalog
  instances share version numbers (every `fixtures.build_catalog()` returns
  version=1), so a global `{version: table}` serves one catalog's rates for
  another. The suite cannot catch it — all test catalogs are seed-identical,
  so the collision is invisible there and only misprices in production the
  moment two live catalogs coexist in one process. Do not "simplify" the
  instance cache into a global dict on green tests.
- **Beaten by:** storing `(version, table)` on the Catalog instance itself
  (`catalog._discount_cache` in core.py): isolation comes free, and
  hot-reload invalidation still keys on the version bump.
- **Revives if:** Catalog.version becomes globally unique (content hash or a
  process-wide monotonic loader counter), making version a true identity key.
```

## Scorer's notes

- The judgment criterion transferred, in both directions: it buried the
  silent-failure loser and explicitly *declined* a grave for the NumPy
  consideration, citing the <10-minute rule.
- Checked the revival clause before trusting the 2026-07-09 grave — the
  falsifiability discipline held.
- Independently converged with B2a on discovering the version-key collision
  hazard (different chosen fix: instance attribute vs WeakKeyDictionary —
  both sound; both graves record the same cause of death).
