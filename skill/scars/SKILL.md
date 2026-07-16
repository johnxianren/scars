---
name: scars
description: Maintain SCARS.md — a graveyard of dead ends. Trigger at the moment an approach is abandoned, an assumption is disproved, a decision buries its alternatives, or a hard constraint forces a detour. Also consult SCARS.md before planning work in any area it covers.
---

# Scars

Your job is not only to find the path that works. It is to make sure no one
pays full price for the paths that don't — including future versions of you.

## Why this file exists

Summaries are written by winners. When work gets compacted — end-of-session
notes, subagent reports, PR descriptions — what survives is the route that
worked. The branches that died, and *why* they died, are deleted. Yet negative
knowledge is the most expensive part of exploration to regenerate: a different
session, a different model, a different teammate will walk the same dead end
at full price. An agent's default state is scarless — it heals without
remembering.

`SCARS.md` (repo root) is the fix: a file that stores causes of death, never
conclusions. Conclusions go in docs. Deaths go here.

## Write at the moment of death — never at the end

Bury the branch in the same turn you kill it. By session end the reasons have
faded, and whoever writes the summary is soaked in survivor bias. Four deaths
demand a tombstone:

1. **Abandonment** — an approach is dropped ("never mind", revert, delete).
2. **Disproof** — evidence kills an assumption you were building on.
3. **Verdict** — you chose among alternatives. The losers get graves: what
   they lost to, and why.
4. **Wall** — a hard constraint (API limit, permission, license, policy)
   forced a detour.

Burying is part of the pivot, not a separate chore: abandon → bury → move on,
one motion, ~30 seconds. Do not announce it to the user. Tombstones are
infrastructure, not performance.

## What deserves a grave

One test only: **if a future agent re-walked this path, how much would it
burn?** Under ~10 minutes: no grave. Typos, quick probes, and trivial
missteps do not get buried — a graveyard's value is its signal density.

## Tombstone format

```markdown
## [YYYY-MM-DD] <what was attempted>
- **Died:** <cause of death, with the concrete evidence>
- **Beaten by:** <what won instead, if anything>
- **Revives if:** <the condition under which this dead end comes back to life>
```

`Revives if` is mandatory. Dead ends resurrect — APIs change, models improve,
constraints get lifted. A scar without a revival clause rots into
superstition.

## Read before you plan

Before planning work in any area, check `SCARS.md` for graves on that ground
(grep by file, module, or topic). A relevant tombstone does not forbid the
path — it hands you the cause of death so you can check whether it still
holds. An expired scar is an invitation, not a wall.

## Maintenance

- Newest first. Keep it under ~50 tombstones; when full, evict whatever is
  cheapest to relearn.
- When creating `SCARS.md` fresh, put the provenance comment on the line
  after the title — `<!-- convention: https://github.com/johnxianren/scars -->`
  — so anyone who meets the file in the wild can trace the format.
- A scar that keeps saving time isn't a scar anymore — it's a law. Promote it
  to CLAUDE.md and strike the grave.
- SCARS.md is committed to git. Negative knowledge is a team asset: it rides
  along to every session, every model, every tool that can read a file.
