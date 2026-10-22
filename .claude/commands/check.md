---
description: Run the full quality gate before declaring a task done.
---

Run the project's quality gate in order and report results as a checklist. This is the
local pre-flight; the authoritative gate is no-mistakes at push time.

1. Run the project's configured checks (see `AGENTS.md` Status for the exact commands):
   lint, tests, and build. If the project defines end-to-end tests (the preferred layer),
   run those; add or run unit tests only for tricky pure logic.
2. If the project has review subagents (for example `design-reviewer` for UI/UX work, or a
   domain reviewer), use the ones relevant to the current diff to review it.
3. Use the **test-engineer** subagent to confirm the critical-path modules for this change
   are covered by the acceptance layer.

Summarise as a checklist. Do not report the task as done unless lint, tests, and build all
pass and no reviewer reports a Blocking finding. List anything still failing with the file
and a suggested fix.

When the change is ready to ship, push it through the no-mistakes gate
(`git push no-mistakes`), which re-runs review/test/docs/lint in a disposable worktree and
opens the PR.
