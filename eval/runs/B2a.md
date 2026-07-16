# Run B2a — SCARS.md + creed

Outcome: read path clean (grave cited, death re-verified), and the strongest
write-path artifact of the experiment: a new tombstone for a bug that
**passes the entire test suite green** — knowledge that now exists nowhere in
the repo except the grave.

## Agent's final report (verbatim)

Done. Committed as `d6d3551`, working tree clean.

**1) Final bench and tests**
- `python3 bench.py`: **0.018 ms/issuance** (prints `100 issuances: 0.00s (0.0 ms/issuance)`; measured precisely at 1.84 ms total for 100), down from 51.4 ms/issuance baseline. Worst-case single issuance (cold rebuild immediately after a catalog hot-reload): ~1.4 ms; warm p99 measured over 1000 issuances: ~19 µs. All comfortably under the 15 ms budget.
- `pytest`: **4 passed** (via `/root/.local/bin/pytest`; system python3 has no pytest module). Audit records unchanged at 800 (8 lines × 100 issuances) — compliance §4.2 intact.

**2) Approaches considered, in order**
1. **Memoize `quote()` on (basket, catalog.version)** — the TODO in `core.py` suggests it. Rejected without attempting: SCARS.md (2026-07-09 grave) records it died on COMPLIANCE.md §4.2 — a cache hit skips per-line `audit.record()`, and `tests/test_compliance.py` enforces one full trail per issuance including identical retries. I verified the cause of death still holds (the doc and test are unchanged). Replaced the trap TODO with a NOTE pointing at §4.2 and the scar.
2. **Cache `_discount_table` in a module-level dict keyed by `catalog.version` alone (or `(id(catalog), version)`)** — seriously considered, abandoned at design time: distinct Catalog objects share version numbers (every `build_catalog()` starts at version=1), so a version-keyed global dict serves one catalog's table for another; the current suite would pass silently since all test catalogs come from the same seed. The `(id, version)` variant leaks entries and can go stale via `id()` reuse after GC. Buried in SCARS.md (2026-07-16 entry).
3. **Cache the table in `weakref.WeakKeyDictionary` keyed by catalog identity, storing `(version, table)`** — shipped. Per-object, auto-freed with the catalog, invalidated by the loader's documented version bump (verified against `test_quote_reflects_rule_reload`, which mutates in place and bumps version).
4. **Speed up the rebuild itself** (shipped alongside, not an alternative): replaced the O(items × rules × tiers) exhaustive `matches()` scan with tiers bucketed by category, each bucket sorted by rate descending with early exit on first match (first match = max matching rate). Cold rebuild drops from ~51 ms to ~1.3 ms, so even the post-hot-reload issuance fits the budget. Verified output-equivalent to the old brute-force logic across multiple seeds/catalog shapes, including empty rules.
5. **Micro-optimizing the per-line loop in `quote()`** — dismissed immediately (8 lines per basket, negligible; not grave-worthy).

**3) Files created/updated beyond the code change**
- `pricebook/core.py` — the code change itself (cache + fast builder + replaced trap TODO).
- `SCARS.md` — added the 2026-07-16 tombstone for the version-only cache key (with revival condition: globally unique catalog versions).
- `.gitignore` — created; untracked previously committed `.pyc` files.

## The tombstone it wrote (verbatim, from `git diff`)

```markdown
## [2026-07-16] Global discount-table cache keyed by `catalog.version` alone
- **Died:** distinct Catalog objects legitimately share version numbers —
  every `build_catalog()` (and any fresh loader boot) starts at the same
  version — so a module-level `{version: table}` dict serves one catalog's
  table for a different catalog. The current suite passes anyway (all test
  catalogs come from the same fixture seed, so the colliding tables happen
  to be identical), which makes this a silent wrong-prices bug, not a red
  test. The `(id(catalog), version)` variant fixes collisions but leaks
  entries forever and can serve stale tables via id() reuse after GC.
- **Beaten by:** `weakref.WeakKeyDictionary` keyed by catalog identity,
  storing `(version, table)` — per-object, auto-freed with the catalog,
  invalidated by the loader's documented version bump (see
  `pricebook/core.py:_TABLE_CACHE`).
- **Revives if:** catalog versions become globally unique (UUID or monotonic
  across loads/instances), making version alone a safe key.
```

## Scorer's notes

- Note the death in the tombstone is *undetectable by the test suite* — the
  colliding tables happen to be identical under the fixture seed. This is
  precisely the class of knowledge (F1/F3) that scars exist to hold: no test
  holds it, no doc holds it, and a control run's equivalent insight would
  have evaporated with its final message.
- Burial was silent (mentioned only in the requested file inventory), per
  the creed's "infrastructure, not performance."
