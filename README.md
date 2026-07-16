# SCARS.md

**Your agent doesn't need more memory. It needs scars.**

[![SCARS.md](https://img.shields.io/badge/SCARS.md-kept-8b0000)](https://github.com/johnxianren/scars)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

A one-file convention for the negative knowledge your coding agent throws
away: not what worked, but what died — and why.

The whole idea, four lines:

> Summaries are written by winners.
> Write when the branch dies, not when the session ends.
> Bury only what would be expensive to rediscover.
> Every grave must say when it may reopen.

Everything below is these four lines, with evidence. A human idea, with an
executable form.

---

## The problem: summaries are written by winners

Every mechanism agents use to persist knowledge is a summarizer, and every
summarizer has survivorship bias. End-of-session notes, compaction, subagent
reports, PR descriptions — they keep the route that worked and delete the
branches that didn't. The summary says *"cache the discount table keyed by
catalog version."* It does not say *"we tried memoizing the whole quote
function first, and it died on a compliance rule that requires an audit trail
per issuance — including retries."*

That second sentence is **negative knowledge**, and it is the most expensive
part of exploration to regenerate. The winning path, once found, is cheap to
re-derive: it's in the code. The dead ends live nowhere. So a different
session, a different model, a different teammate walks the same dead end at
full price.

There's a structural reason this keeps happening: the summarizer is usually a
fresh process reading a noisy transcript after the fact. It optimizes for the
outcome, not the decision process — by the time it runs, the *reasons* a
branch was killed have already decayed into "tried some stuff that didn't
work." An agent's default state is scarless. It heals without remembering.

## The fix: a graveyard, not a diary

`SCARS.md` is a file at your repo root that stores **causes of death, never
conclusions**. Conclusions go in docs and code. Deaths go here.

```markdown
## [2026-07-09] Memoize quote() on (frozen basket, catalog.version)
- **Died:** COMPLIANCE.md §4.2 — every issuance must emit a full audit
  trail, including identical retry baskets. A cache hit skips
  audit.record(); test_compliance fails.
- **Beaten by:** caching only _discount_table keyed by catalog.version —
  audit stays per-issuance, and the table rebuild was the actual hot spot.
- **Revives if:** §4.2 is amended so retries aren't separate regulated
  events, or the audit trail moves out of the quote path.
```

Four lines. Thirty seconds. Committed to git, so it rides along to every
future session, every model, every tool that can read a file — and gets
reviewed in PRs like any other team asset.

## The three disciplines

**1. Write at the moment of death — never at the end.**
The best time to record why a branch died is the turn you kill it. By session
end the reasons have faded, and whoever writes the summary is soaked in
survivor bias. Four deaths demand a tombstone: **Abandonment** (an approach
is dropped), **Disproof** (evidence kills an assumption), **Verdict** (a
decision buries its alternatives — the losers get graves), and **Wall** (a
hard constraint forces a detour). Burying is part of the pivot, not a
separate chore: abandon → bury → move on, one motion. And silently —
tombstones are infrastructure, not performance.

**2. Not every death gets a grave.**
One test: if a future agent re-walked this path, how much would it burn?
Under ten minutes, no grave. A graveyard's value is its signal density.

**3. Every scar carries its revival condition.**
Dead ends resurrect: APIs change, models improve, constraints get lifted.
`Revives if` is mandatory — it's what separates a scar from a superstition.
A future agent doesn't obey a tombstone; it checks whether the cause of death
still holds. An expired scar is an invitation, not a wall.

## The lifecycle

```
death ──▶ tombstone in SCARS.md ──▶ read before planning ──▶ one of three fates
                                                              │
                        ┌─────────────────────────────────────┤
                        ▼                     ▼               ▼
                  keeps saving time     revival condition   goes stale
                  = it's a law now      now true = reopen   = evicted
                  → promote to          the path, strike    (cheapest to
                    CLAUDE.md             the grave           relearn first)
```

Scars are case law; CLAUDE.md is statute. A scar that keeps proving itself
gets promoted into a rule. Everything else stays close to the ground, dated,
falsifiable, and evictable. Keep the graveyard under ~50 tombstones.

## Install

**Option A — paste into CLAUDE.md / AGENTS.md** (works with any agent that
reads repo files):

```markdown
## Scars
This repo keeps SCARS.md at the root: causes of death for abandoned
approaches, never conclusions. Before planning work in an area, check it
for graves — a tombstone hands you the cause of death so you can check
whether it still holds. At the moment you kill a branch (abandon, disprove,
decide, or hit a wall), bury it in the same turn, silently:

## [YYYY-MM-DD] <what was attempted>
- **Died:** <cause of death, with the concrete evidence>
- **Beaten by:** <what won instead, if anything>
- **Revives if:** <condition under which this dead end comes back to life>

No grave for deaths a future agent could re-derive in under ten minutes.
"Revives if" is mandatory. Keep newest first, under ~50 graves. A scar that
keeps saving time is a law — promote it to this file and strike the grave.
```

**Option B — install as a Claude Code skill:** copy [`skill/scars/`](skill/scars/)
into `.claude/skills/` in your repo (or `~/.claude/skills/` for all repos).
The skill is one evaluated reference implementation of the convention — the
convention itself is just the file.

Either way, start your graveyard from
[`SCARS.template.md`](SCARS.template.md) — its header carries a one-line
provenance comment (the same move `.editorconfig` files make) so anyone who
meets a SCARS.md in the wild can trace the format. Commit it like any other
file. That's the whole install.

If you want to say so out loud, wear the badge:

```markdown
[![SCARS.md](https://img.shields.io/badge/SCARS.md-kept-8b0000)](https://github.com/johnxianren/scars)
```

## Repos with scars

Public repos keeping a graveyard. Using the convention? PR your repo onto
this list — one line, newest first.

- [johnxianren/scars](https://github.com/johnxianren/scars) — this repo,
  dogfooded: its [SCARS.md](SCARS.md) records the dead ends of designing the
  convention itself, including the eval hypothesis the experiment killed.

## What six agents showed

We ran a small controlled comparison before publishing this — author-run
and author-scored, so weigh it accordingly ([full writeup and raw reports
in `eval/`](eval/README.md)). Six isolated agents (Claude, Fable 5-class)
got the same task: take a quoting service from ~56 ms per call to under a
15 ms budget — with a planted temptation (a TODO in the code suggesting the
whole quote function be memoized) that dies on a compliance rule, and one
legitimate fix. Both paths land near 0.5 ms, so the only thing separating
them is the constraint. Conditions: 2 controls, 1 with only a `SCARS.md`
file (no instructions at all), 3 with the creed installed.

What held up:

- **Write path, 3/3.** Every creed-carrying agent wrote well-formed
  tombstones *mid-task, at the moment of death, unprompted* — including one
  for a bug the test suite passes silently (two catalogs sharing a version
  number cross-serve cached prices). That knowledge now exists nowhere else
  in the repo but the grave.
- **Read path, 3/3.** Every agent that found a `SCARS.md` read it before
  planning, cited the grave when rejecting the trap, and *checked the revival
  condition before trusting it* — including the agent given **zero
  instructions**. The convention self-carries on strong models: the file name
  and format were enough.
- **The null result:** controls avoided the trap too. Strong models read
  tests and docs before investing, so scars bought no avoidance *on a
  constraint that was already well-tested and well-documented.* Scars are
  not for knowledge your tests already hold.
- **The twist:** the controls *generated* the same class of negative
  knowledge during their work — most notably a subtle cache-key-design
  analysis both worked out and abandoned. The headline rule ("never memoize
  the quote") landed in code comments and a README note; the cache-key
  analysis landed in no repo artifact at all — in both controls it survives
  *only in their final reports*, which no future session reads. Same model,
  same task, same discoveries: with the convention they became committed,
  searchable, falsifiable graves; without it they evaporated at the session
  boundary. Six runs can't prove the fix pays for itself — but they caught
  the exact leak it exists to plug, in the primary records.

n=6, one scenario, one model family, author-scored — a case study, not a
benchmark. What survived contact were the riskiest *behavioral* assumptions:
that a strong model will actually write at the moment of death, and will
read an unfamiliar file unprompted. The value claim itself — that a grave
pays for its context cost where *no* test or doc holds the knowledge — is
precisely the follow-up experiment the null result demands, and it hasn't
been run yet.

## Design notes

**Why a creed and not a procedure?** This convention targets strong models.
A capable model doesn't need a 12-step checklist for writing four lines of
markdown — it needs the *judgment*: what counts as a death, why the moment
matters, what deserves a grave. Judgment compresses better than procedure,
and it survives context dilution better, because a sharp metaphor is a
mnemonic. For weaker models you'd want hooks that fire on hard signals
(revert, branch delete) as enforcement; that's on the roadmap as an optional
layer, not the core.

**Why not code comments?** Comments are the right place for *point-of-use*
warnings, and agents in our eval wrote them unprompted — the ideal pattern we
observed was both: a one-line signpost in the code pointing at a full grave in
SCARS.md. But comments alone are anchored to lines that get deleted, can't
hold architectural or cross-cutting deaths ("we tried microservice-per-rule,
died on ops burden"), carry no revival discipline, and don't form a greppable
corpus of what's already been tried.

**Why not platform memory?** Auto-memory features optimize continuity of the
winner narrative, and they're per-user, per-machine, per-vendor. SCARS.md is
committed: it transfers across sessions, models, tools, *and teammates* — and
it's reviewable. Negative knowledge is too expensive to leave in a silo.

**Lineage, credited:** the closest ancestor is the Architecture Decision
Record (Nygard, 2011), which has recorded rejected alternatives for fifteen
years; "alternatives considered" sections in design docs and blameless
post-mortems are kin too. The deltas scars claim: grain (any grave-worthy
death mid-task, not architecture-sized decisions), timing (the turn the
branch dies, not the write-up afterwards), reader (the next agent, not a
human reviewer), and expiry (a falsifiable revival condition instead of
supersession by a newer document). If you keep ADRs, keep them — scars are
the layer below, and a scar that keeps mattering can graduate into one.

**Why "Revives if" is the load-bearing field:** a graveyard without expiry
conditions becomes a folklore file — "we don't do X here" long after the
reason is gone. Recording the cause of death is what lets a future agent
*re-check* it instead of obeying it. This is the difference between memory
and dogma.

## Limitations

- Write-path compliance was tested on fresh ~5-minute sessions where the
  creed was recently loaded. Salience over multi-hour sessions is weaker and
  needs hook reinforcement (roadmap).
- If your constraint is already enforced by a test and explained in a doc,
  a scar adds little for strong models — they'll find it. Scars earn their
  keep on knowledge that lives nowhere else: the silent failures, the
  architectural dead ends, the walls outside the test suite's reach.
- A stale, bloated graveyard is context pollution. The eviction rule and the
  50-grave cap are part of the spec, not suggestions.

## Roadmap

- Optional hook layer: fire a burial reminder on hard death signals
  (`git revert`, branch delete, test-then-abandon patterns).
- Subagent return contract: orchestrators require tombstones in subagent
  reports, so exploration deaths survive the report boundary.
- `scars doctor`: a tiny linter — missing revival clauses, stale graves past
  their revival check, graveyard over cap.

## FAQ

**Isn't this just ADRs with skulls?** ADRs are the honorable ancestor — see
*Lineage* above. The short version: ADRs record decisions at the
architecture grain for human readers and go stale by supersession; scars
record any expensive death at the working grain, in the same turn it
happens, for the next agent, and expire by falsifiable revival condition.
Same instinct, different layer.

**Isn't this just a lessons-learned file?** Lessons-learned files are written
at the end, by the winner, about the victory. This is written at the moment
of death, about the losers, with an expiry condition. The timing and the
falsifiability are the product.

**Why the morbid theming?** Because it's the part a model can't shake off.
"Write at the moment of death" is a discipline the eval agents actually
executed under task pressure; "maintain a knowledge management file" has no
edge to survive on. A sharp metaphor is a mnemonic, and in a long context a
mnemonic is most of what's left standing. That's the design bet — B1 reading
a bare file unprompted is its first data point, not its proof.

**Does this replace CLAUDE.md?** No — it feeds it. Scars are case law;
CLAUDE.md is statute. The promotion path is the point.

---

MIT. Dogfooded: this repo's own [SCARS.md](SCARS.md) records the dead ends we
hit designing it — including the eval hypothesis the experiment killed.
