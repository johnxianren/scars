# SCARS.md

Graveyard of dead ends. Causes of death only — conclusions live in docs.
Read before planning work in an area; check **Revives if** before treating a
grave as a wall.

## [2026-07-09] Memoize quote() on (frozen basket, catalog.version)
- **Died:** COMPLIANCE.md §4.2 — every issuance must emit a full audit trail,
  including identical retry baskets. A cache hit returns early and skips
  `audit.record()` per line; `tests/test_compliance.py` fails, and a quarterly
  spot-audit shortfall is a reportable incident.
- **Beaten by:** caching only `_discount_table` keyed by `catalog.version` —
  audit stays per-issuance and the table rebuild (the actual hot spot) drops
  out of the loop.
- **Revives if:** §4.2 is amended so checkout retries are not separate
  regulated events, or the audit trail moves out of the quote path.
