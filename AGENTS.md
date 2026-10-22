# PROJECT_NAME

Project-specific context. Global preferences live in `~/.claude/AGENTS.md`
(persona, no mdash, E2E-first testing, no low-cost bias); do not repeat them here.

## What this is

TBD. Describe the project in a sentence once it is defined.

## Requirements

Filled by the `/project-intake` skill. Anything unknown stays `TBD (decide later)`
and can be filled on a later intake run.

- Delivery / platform: TBD (web app | hybrid | cross-platform native | web-first then native | desktop)
- Data & persistence: TBD (none | on-device | hosted database | not sure)
- Users & accounts: TBD (none | accounts/auth | multi-tenant | SSO)
- Connectivity: TBD (offline-first | online-only | both)
- Scale & distribution: TBD (personal | small group | public/at-scale)

## Tech stack

DELIBERATELY UNSPECIFIED until Requirements are understood. Chosen from the problem
(users, platform, constraints), not from habit or from whatever is least effort.
`/project-intake` proposes a stack from the answers above; record the decision here.

- Stack: TBD
- Run: TBD
- Tests: TBD (prefer end-to-end tests first, per global preference)

## Security & compliance

Filled by `/project-intake` based on what the project handles. Only what applies is
listed; unknowns stay `TBD (decide later)`.

- Sensitive data handled: TBD (none | personal/PII | children's | payments | health | other)
- Applicable regimes / controls: TBD
- Recommended audits: TBD

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
