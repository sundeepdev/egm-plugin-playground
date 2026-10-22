---
description: Flush this session's decisions, deferred items, and defects into ADRs and GitHub Issues, then reconcile the living docs they touch (ADR index + cross-refs, README, AGENTS.md), so nothing lives only in chat and nothing drifts.
argument-hint: "[optional focus, e.g. 'just the data-model discussion']"
---

**Scope: only what is NEW since the last capture.** Find the most recent capture marker (a
`[📌 captured through here …]` line emitted earlier by `/capture` or `/wrap`) and review
only what came after it; if there is none, review the whole session so far$ARGUMENTS. This
keeps capture incremental. Never re-record what a prior capture already wrote.

Extract anything durable that is not already written down:

- **Decisions**, especially architecture / one-way-door calls.
- **Deferred items**, including the not-chosen option whenever the user picked between
  alternatives.
- **Defects / hygiene**, known issues, risky shortcuts, follow-ups.

Route each item to its home:
- **Architecture decisions** to a new ADR in `docs/adr/` (use the template in
  `docs/adr/README.md`; status `Proposed` unless clearly accepted) and add it to the ADR
  index.
- **Work items and defects** to **GitHub Issues** (`gh issue create`) with the right label
  (`feature`, `defect`, `chore`, `security`, `epic`). Do not duplicate an existing issue;
  link to the epic it belongs under. GitHub Issues is the backlog, not a docs file.

**Then reconcile the documents the captured items touch.** Recording a decision is not done
until the docs that depend on it still tell the truth. For each item captured, update the
docs it affects:
- **ADR index + cross-references** (`docs/adr/README.md`): a new / superseded / amended ADR
  gets its index entry, and every Supersedes / Superseded by / Related pointer, in the new
  ADR and in the ones it references, must name a doc that exists; add the back-reference.
- **`AGENTS.md`**: if a captured decision changed the stack, a run/test command, a
  convention, or a requirement/security fact, update the matching line.
- **`README.md`**: if the captured change shipped a feature or moved a fact the README
  states, fix that fact.

Keep every edit surgical: change the stale fact, not the surrounding prose. If a doc should
change but the user's intent is unclear, note it in the summary rather than guessing.

Then:
1. Show a short bullet summary of what you added/updated and where (ADRs, issue numbers,
   doc edits).
2. Stage and commit the doc changes with a clear message. Do not push (shipping is `/wrap`
   or the no-mistakes gate).
3. End with a one-line `captured: …`, then emit the capture marker so a later command scans
   only below it:

   `[📌 captured through here · /capture · <date + time>] already recorded; scan only below`

If there is nothing new worth recording, say so plainly and change nothing, but still emit
the marker so the boundary stays current.
