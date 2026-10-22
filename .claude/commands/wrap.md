---
description: End-of-session wrap-up. Capture (incrementally, since the last marker), reconcile the living docs (README, ADR index, AGENTS.md), write a named session record to docs/session-log.md, verify the tree is green and committed, and leave a clean handoff + capture marker.
---

Wrap up this session so nothing is lost, every doc still tells the truth, the session is
reviewable later, and the next session starts clean.

**Scope: only what is NEW since the last capture.** Find the most recent capture marker (a
`[📌 captured through here …]` line from `/capture` or `/wrap`) and consider only what came
after it; if there is none, use the whole session. Never re-capture or duplicate what a
prior command already recorded.

Do these in order and stop if a step genuinely fails:

1. **Capture** (same as `/capture`): scan the in-scope conversation for decisions, deferred
   items, and defects not yet written down. Architecture decisions to a new ADR in
   `docs/adr/`; work items and defects to GitHub Issues with the right label. When the user
   chose between options, record the not-chosen one (as a deferred issue or in the ADR's
   Alternatives). Do not duplicate what exists.

2. **Reconcile the backlog**: on GitHub Issues, close anything shipped this session via its
   PR (`Closes #<n>`), and make sure the open issues + epics leave an unambiguous entry
   point for a fresh session.

3. **Reconcile the living docs (consistency sweep)**: propagate any spec / design /
   architecture / feature change into every living document that must stay true, so context
   never drifts:
   - **`README.md`**: re-check its change-prone facts (what is built + its "as of" date,
     any counts, the project structure, the tech stack).
   - **`docs/adr/README.md`**: a new / superseded / amended ADR updates its entry + status,
     and every cross-reference resolves to a doc that exists; add the back-reference.
   - **`AGENTS.md`**: only if a rule, command, convention, stack choice, requirement, or
     security fact changed.
   Keep edits surgical. If a doc should change but the user's intent is unclear, flag it in
   the handoff rather than guessing.

4. **Write the session record**: append (or update) this session's entry at the top of
   `docs/session-log.md` (newest first). Head it `## <YYYY-MM-DD> · <short session name>`
   derived from the session's main thread. The entry records, in brief:
   - Summary: 2 to 4 sentences, what the session set out to do and what changed.
   - Shipped / merged: PRs opened and merged (with `#`), what is now live vs in-flight.
   - Docs & ADRs: ADRs created/updated, README reconciled.
   - Decisions: key product/architecture calls and the not-chosen options parked.
   - State: lint / test / build / CI status at wrap.
   - Handoff / next: recommended next step + open threads or blockers.
   If an entry for this session already exists, update it rather than appending a duplicate.

5. **Verify state** (skip the build only if no code changed this session): run the project's
   configured lint / test / build (see `AGENTS.md` Status). Report pass/fail. If anything
   fails, STOP and surface it. Do not wrap a broken tree.

6. **Commit + push**: `git status`. If there is uncommitted code, list it and ask before
   committing (never blind-commit half-done work). Commit the doc / README / session-log
   changes from steps 1 to 4 with a clear message. Ship code through the no-mistakes gate
   (`git push no-mistakes`), not straight to origin. If a push fails, surface it rather than
   leaving it silently unpushed.

7. **Handoff + close**: a short note in chat (what shipped, which docs were reconciled, the
   recommended next step, any run reminders), pointing at the new `docs/session-log.md`
   entry. End with a one-line `wrapped: …`, then emit the capture marker:

   `[📌 captured through here · /wrap · <date + time>] nothing above needs re-capturing`

If the tree is already clean and nothing new needs capturing or reconciling, say so plainly,
but still write the session record (step 4) and emit the marker.
