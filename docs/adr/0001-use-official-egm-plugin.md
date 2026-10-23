# 0001. Test the official EGM plugin instead of maintaining a Claude Code port

- Status: Accepted
- Date: 2026-10-23

## Context

This repo started as a Claude Code port of Google's Elephant-Goldfish Model (EGM)
plugin: upstream skills vendored from commit `9a208f9`, adapted by a script
(plugin-root paths, `egm:` subagent types, read-only `tools` allowlists). It passed
validation and a full brainstorm, draft, and review run.

On 2026-10-22 upstream merged official Claude Code support
(google/elephant-goldfish-model#103, commit `dbce39c`). It covers the same ground and
more: Claude-only agent adapters in `.claude-plugin/agents/` (so shared persona
frontmatter stays harness-neutral), `omitClaudeMd` reviewer isolation, Cowork support,
docs (`docs/claude.md`), and integration tests. Rerunning the same flow on it produced
the same behaviour (see `docs/egm-runs.md`).

## Decision

Delete the vendored port (`plugins/egm/`, `scripts/vendor_egm.py`,
`scripts/claude_adapters/`, the playground marketplace). Keep this repo as an
end-to-end test harness that installs the official plugin from
`google/elephant-goldfish-model` into a throwaway fixture project.

## Consequences

- No vendored copy to keep in sync; tests always run the latest upstream
  (`setup_project.sh` refreshes the marketplace).
- Upstream regressions show up here directly. `EGM_PLUGIN_DIR` still lets a local
  checkout be tested, for example before proposing an upstream change.
- One-way in practice: the port was never committed, so bringing it back means
  redoing the adaptation. Upstream's adapters make that unnecessary.

## Alternatives considered

- **Keep the port alongside upstream.** Duplicates upstream's work with weaker
  isolation (no `omitClaudeMd`) and Claude tool names in shared persona frontmatter.
- **Fork upstream and add Claude support there.** Redundant once #103 landed.
