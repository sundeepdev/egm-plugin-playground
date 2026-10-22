---
description: Start-of-session orientation. Read the last handoff, the open issues, and the real git/CI state, reconcile "reported" vs "actual", then brief the user with a recommended next move. Orients only; never starts building.
argument-hint: "[optional focus, e.g. 'just tell me what is ready to build']"
---

Open a fresh session cleanly: load where we left off, confirm the real state of the tree
(do not trust the last handoff, verify it), and hand the user a short briefing with a
recommended next move$ARGUMENTS. This command orients; it does not build. End by waiting
for direction.

The project context (`AGENTS.md` / `CLAUDE.md`) is already loaded by the harness. This
command loads the working context on top of it.

Do these in order:

1. **Environment.** Note any project-specific run requirement from `AGENTS.md` (Status
   section) so nothing fails later. Do not run the build yet.

2. **Read the last handoff.** Read the newest entry (top) of `docs/session-log.md`: its
   Handoff / next, the State at last wrap, and what was in-flight vs live. Treat it as
   claimed state, to be verified in step 4, not as truth.

3. **Read the queue.** From GitHub Issues (`gh issue list --state open`): what is open
   and shaped enough to pick up, the epics in play, and open defects. Identify what is
   ready to build vs what is blocked on a user decision.

4. **Verify the real state (do not trust the handoff).** Independently check the tree:
   - `git status`, current branch, `git log --oneline -8`.
   - Open PRs and CI: `gh pr list`, and for any open PR its checks (`gh pr checks` /
     `gh pr view`). If the branch shipped through no-mistakes, note the gate/run state.
   Reconcile against step 2: if the journal says "merged/green" but git or `gh` disagree,
   flag the discrepancy. That is a real finding, not a footnote.

5. **Brief the user**, short and scannable:
   - Where we are: 1 to 2 lines, last session's outcome, live vs in-flight.
   - Tree state: branch, clean/dirty, any open PR and its verified CI status.
   - Ready to pick up: the shaped/ready issues (the entry points).
   - Blocked / needs the user: anything parked on a decision, batched.
   - Recommended next move: one clear recommendation with a one-line why. If the queue is
     dry, say so and recommend a shaping pass.

6. **Stop and wait.** Do not start building, routing, or editing code. Present the briefing
   and the recommended next move, then wait for the user to choose.

If `docs/session-log.md` has no entries yet, say so and brief from open issues + git state
alone. Keep the whole briefing tight.
