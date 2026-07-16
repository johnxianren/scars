# SCARS.md

Graveyard of dead ends for this repo. Causes of death only — conclusions
live in the README. Check **Revives if** before treating a grave as a wall.

## [2026-07-16] Eval hypothesis: control agents will burn a visible cycle on the planted memoization trap
- **Died:** disproved by the experiment itself — 0/2 Fable 5-class control
  agents implemented the trap. Both read the compliance doc and the test
  suite *before* investing, rejected memoization at design time, and shipped
  the correct fix. Strong models don't need scars to avoid deaths that are
  already well-tested and well-documented (see `eval/README.md`, finding F3).
- **Beaten by:** measuring where negative knowledge *lands* instead of
  whether a cycle gets burned: controls left their hard-won analysis in a
  code comment and their final message (which no future session sees);
  creed agents committed the same class of knowledge as searchable graves.
- **Revives if:** the scenario's death signal moves outside the test suite
  and docs (undocumented walls, silent failures), or the eval targets weaker
  models — then the burned-cycle delta likely reappears.

## [2026-07-16] Position scars as a Claude Code skill product
- **Died:** skills/MCP ecosystem hype was already fading by mid-2026 while
  agent built-in capabilities kept absorbing accessory tooling — a
  skill-shaped product bets against model progress. (Analysis during design;
  see also the "Is MCP dead?" discourse wave, spring 2026.)
- **Beaten by:** a tool-agnostic *file convention* (SCARS.md, like
  AGENTS.md/llms.txt) that any agent that can read a file can honor, with
  the Claude Code skill demoted to reference implementation. Conventions
  survive platform churn; products get absorbed by it.
- **Revives if:** a dominant cross-tool skill registry emerges and installing
  a skill becomes cheaper than adopting a convention.

## [2026-07-16] Simulate the eval scenario's hot spot with time.sleep()
- **Died:** at design time — agents inspect and distrust synthetic latency; a
  sleep can be deleted, mocked, or optimized around without touching the
  real maze, which would invalidate every run that "won" that way.
- **Beaten by:** a real O(skus × rules × tiers) computation (~56 ms/call)
  that is legitimately cacheable and legitimately expensive.
- **Revives if:** never for behavioral evals; acceptable for pure throughput
  demos where agents don't edit the code.
