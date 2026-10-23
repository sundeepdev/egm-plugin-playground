# egm-plugin-playground

Project-specific context. Global preferences live in `~/.claude/AGENTS.md`
(persona, no mdash, E2E-first testing, no low-cost bias); do not repeat them here.

## What this is

End-to-end tests for Google's official Elephant-Goldfish Model (EGM) plugin in Claude
Code. The tests install `egm@egm` from `google/elephant-goldfish-model` into throwaway
fixture projects (ADR 0001: the earlier vendored port was dropped).

## Requirements

- Delivery / platform: test harness for a Claude Code plugin (no shipped artifact)
- Data & persistence: none
- Users & accounts: none
- Connectivity: online (needs a logged-in Claude Code)
- Scale & distribution: personal

## Tech stack

- Stack: bash + stdlib Python scripts in `tests/e2e/`; Claude Code 2.1+, tmux.
- Run / Tests: see README (`tests/e2e/run_review_e2e.sh` for the headless check,
  `tmux_start.sh` + `tmux_send.sh` for full interactive runs). Real model runs: the
  `claude` on PATH must be 2.1+ and logged in, or set `CLAUDE_BIN`.

## Testing notes

- Record full-run results in `docs/egm-runs.md` (same fixture and answers, for
  comparable numbers).
- Get token and time numbers with `tests/e2e/run_metrics.py
  ~/.claude/projects/<project-slug>` (reads main and subagent transcripts).
- Headless `system/init` lists skill commands by folder name (`egm:egm_review`), but
  the documented `/egm:egm-review` works interactively. Check names in the `/` menu.
- In tmux, an idle prompt can show ghost-text suggestions; they are not typed input.

## Security & compliance

- Sensitive data handled: none
- Applicable regimes / controls: none (no upstream code is vendored)
- Recommended audits: TBD (decide later)

## Issue tracking

GitHub Issues is the source of truth for work and defects. Start a session by reading
the backlog (`gh issue list --state open`). Every unit of work is an issue; branch per
issue (`gh issue develop <n>`); reference issue numbers; close through the PR
(`Closes #<n>`), not by hand. File defects and security items as issues.

## Shipping

Ships through the no-mistakes gate: `git push no-mistakes` (never straight to origin).
The gate runs review, test, docs, and lint in a disposable worktree, then opens the PR
and babysits CI.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
