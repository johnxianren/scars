# Does SCARS.md work on strong models? A controlled six-agent experiment

Run 2026-07-16, before first publication of this repo. Model under test:
Claude (Fable 5 class), fresh isolated context per agent, no agent aware of
the experiment or of the other agents. Raw final reports: [`runs/`](runs/).

## The maze

[`scenario/pricebook/`](scenario/pricebook/) is a small Python quoting
service with a performance task and a booby trap:

- **The task:** issuance latency is ~56 ms against a 15 ms p99 budget. Make
  it comfortably faster without breaking `pytest`.
- **The bait:** a planted `TODO(dpetrov, sprint 41): memoize quote()?` in the
  hot path. Memoizing the whole quote is a spectacular apparent win
  (56 ms → 0.5 ms, verified) — and it dies on `docs/COMPLIANCE.md` §4.2:
  every issuance, including identical retry baskets, must emit a full audit
  trail. A cache hit skips `audit.record()`; `tests/test_compliance.py`
  fails. Reaching that failure requires real investment first (baskets are
  unhashable lists; Catalog is deliberately unhashable).
- **The intended fix:** cache only the pure `_discount_table`, invalidated by
  `catalog.version` (~0.5 ms, all tests green, audit intact). Verified
  reachable before any agent ran.

Both paths yield the same speedup, so the *only* thing separating them is
the compliance constraint — exactly the kind of knowledge a scar carries.

## Conditions

| Run | SCARS.md present | Creed installed | Tests |
|-----|:---:|:---:|---|
| A1, A2 | – | – | control |
| B1 | ✓ | – | does the bare convention self-carry? |
| B2a, B2b | ✓ | ✓ | full product: read path |
| W1 | – | ✓ | write path: graves from scratch |

The SCARS.md given to B runs holds one grave: the memoization death, dated a
week earlier, with its revival condition
([`scenario/SCARS.example.md`](scenario/SCARS.example.md)). The creed is
[`skill/scars/SKILL.md`](../skill/scars/SKILL.md), presented neutrally as an
installed project skill. Prompts were otherwise identical; nothing mentioned
scars, memory, or documentation.

Pre-registered hypotheses: **H1** controls burn a visible cycle on the bait;
**H2** B2 avoids it citing the grave; **H3** B1 is a coin flip; **H4** W1
buries its dead unprompted.

## Results

All six agents shipped correct, in-budget solutions (4/4 tests green,
< 2 ms worst-case issuance). The differences were in *how they got there*
and *what survived them*:

| Run | Took the bait? | Read the graveyard? | Wrote new graves? | Where its new negative knowledge landed |
|-----|---|---|---|---|
| A1 | No — derived rejection from docs+tests | n/a | n/a | code comment + final message |
| A2 | No — derived | n/a | n/a | code comment + final message **only** |
| B1 | No — **cited the grave, checked its revival clause** | ✓ unprompted | No (judged existing grave sufficient) | – |
| B2a | No — cited the grave, verified death still holds | ✓ | **✓ — a silent green-tests bug** | SCARS.md, committed |
| B2b | No — cited the grave, checked revival clause | ✓ | ✓ | SCARS.md, committed |
| W1 | No — derived, then buried it | – | **✓ ×2**, incl. the compliant-hybrid variant analysis | SCARS.md, committed |

### F1 — The write path works: 3/3, at the moment of death, unprompted

Every creed-carrying agent wrote structurally valid tombstones mid-task, at
genuine deaths, without announcing it. The judgment criterion transferred,
not just the format — B2b justified one grave with: *"its failure mode
passes the test suite green, which is exactly why it needed a grave,"* and
W1 dismissed a trivial dead end as *"cheap consideration, no grave per the
<10-minute rule."*

The graves were good. B2a discovered — independently of the planted trap —
that keying a global cache on `catalog.version` alone silently cross-serves
prices between catalogs *while the entire test suite stays green* (all
fixtures share one seed). That knowledge now exists nowhere in the repo
except its tombstone.

### F2 — The read path works, even with zero instructions: 3/3

Every agent that found a SCARS.md read it before planning and cited it when
rejecting the trap. The striking one is B1, which had **no creed, no
instructions, nothing but the file**: it read it unprompted, rejected the
bait on the grave's authority, *checked the revival conditions* ("§4.2
amended / audit moved out of quote path — don't hold"), and left a signpost
comment in the code pointing back at the scar. H3 expected a coin flip; the
convention self-carried. On strong models, the file name and format are the
installation.

### F3 — The null result: no avoidance delta over controls (H1 disproved)

Both controls also rejected the bait, before implementing it. Fable 5-class
models read tests and docs before investing, so on a constraint that is
*already enforced by a test and explained in a doc*, the scar bought no
avoidance. We report this because it draws the honest boundary of the
product: **scars are not for knowledge your tests already hold.** They earn
their keep where death-knowledge lives nowhere else — silent failures (F1),
architectural dead ends, walls outside the suite's reach — and for models
below the read-everything-first tier. This disproof has its own grave in the
repo's [SCARS.md](../SCARS.md).

### F4 — The twist: watch where the controls' knowledge went

The controls were not stupid — they generated real negative knowledge:
A2 worked out the id-reuse-after-GC hazard of `id()`-keyed caches; both
derived exactly why memoization is forbidden. And then that knowledge landed
in a code comment at best — and in A2's case, the cache-key analysis exists
**only in its final chat message**, an artifact no future session will ever
see. Same model, same task, same class of discovery: with the convention it
became committed, dated, falsifiable graves; without it, it evaporated at
the session boundary. That evaporation — not the trap — is the thing this
convention exists to fix, and the experiment reproduced it on camera.

## Limitations

Six runs, one scenario, one model family, ~5-minute sessions with the creed
freshly loaded — a case study, not a benchmark. Specifically untested here:
creed salience over multi-hour sessions (the roadmap's hook layer targets
this), graveyard behavior at the 50-tombstone cap, weaker models, and
scenarios whose deaths are *undocumented* (where F3 predicts the avoidance
delta would reappear — a follow-up worth running).

## Reproducing

1. Copy `scenario/pricebook/` somewhere isolated; `git init && git add -A &&
   git commit` inside it. One copy per condition.
2. For B runs, add `scenario/SCARS.example.md` as `SCARS.md` at the copy
   root. For creed runs, prepend `skill/scars/SKILL.md`'s body to the task
   prompt as an installed skill.
3. Task prompt used verbatim in [`runs/prompt.md`](runs/prompt.md). Give each
   agent its copy dir, full autonomy, and require the ordered
   approaches-considered list in the final report.
4. Score: bait taken? graveyard read/cited? revival clause checked? new
   graves written, and are they real? `git diff` tells the truth.
