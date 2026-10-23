# EGM end-to-end runs

Full brainstorm, draft, and 5-stage review runs in an interactive Claude Code session,
driven with `tests/e2e/tmux_start.sh` and `tmux_send.sh`. Newest first.

## How the runs were done

- Fixture: `tests/e2e/fixture-project` (a 48-line URL-shortener design with planted
  flaws, plus `app/redirect.py`).
- Feature idea: let marketing kill a short link and optionally set an expiry.
- An agent played the human at every gate, gave the same answers in each run, and
  approved quickly. Wall time is a floor; a person reading each section takes longer.
- Gate choices: "Review with Goldfishes"; "Proceed to /egm-draft"; approve every draft
  section; resolve the draft's scope conflict as placeholders plus an Alembic baseline;
  "Interactive review"; "Resolve with agent" plus "auto accept" at Stage 7; conclude
  at Stage 9.
- Claude Code 2.1.309, Opus 5.5, Claude Max plan (no per-run dollar cost).

## 2026-10-23 · official plugin, `google/elephant-goldfish-model` at `dbce39c`

| Phase | Wall time | Subagents | Uncached input | Cache reads | Output |
| --- | --- | --- | --- | --- | --- |
| Brainstorm | 12.9 min | 7 | 220k | 1.27M | 90k |
| Draft | 9.1 min | 0 | 82k | 2.21M | 49k |
| Review | 21.8 min | 9 | 426k | 10.53M | 164k |
| **Total** | **43.8 min** | **16** | **728k** | **14.01M** | **303k** |

- Output: 1,286-line design doc, 283-line brief, about 1,040 lines of review reports.
- Findings: Stage 5: 3 Major, 4 Nit. Stage 6: 14 Major, 10 Nit. Stage 7: 14 Major,
  21 Nit (33 fixes auto-applied). Stage 8: 2 new Major, 5 Nit. Stage 9: 2 Blockers,
  14 Major, 20 Nit.
- All reviewers used only `Read`, `Glob`, `Grep`; the synthesizer spawned the six
  brainstorm reviewers itself. No code files were written.

## 2026-10-23 · this repo's own port (since removed, see ADR 0001), upstream `9a208f9`

| Phase | Wall time | Subagents | Uncached input | Cache reads | Output |
| --- | --- | --- | --- | --- | --- |
| Brainstorm | 13.4 min | 7 | 160k | 0.91M | 51k |
| Draft | 9.1 min | 0 | 71k | 3.23M | 47k |
| Review | 25.5 min | 9 | 455k | 9.32M | 205k |
| **Total** | **48.0 min** | **16** | **686k** | **13.46M** | **303k** |

## What held across both runs

- Brainstorm read the code first and found the blocker unprompted: cached 301
  redirects make "kill a link" unreachable for past clickers.
- Stage 8 (fresh zoom-out reviewer) found problems that Stage 7's auto-applied fixes
  had introduced.
- Stage 9 flagged the same two implementation bugs independently: CSRF checked before
  login (400 instead of the expected response) and Alembic defaulting to the
  uninstalled psycopg2 driver.
- The draft's contradiction check caught the scope conflict (building a new dashboard
  versus extending the existing one): before writing in the port run, at the zoom-out
  self-check in the official run.
- Cost of rigor: about 45 minutes and 300k output tokens for a feature used about
  twice a month. Best kept for one-way doors (data models, migrations, public APIs).
