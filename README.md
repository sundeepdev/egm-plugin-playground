# project-template

Base template for new projects that use the agentic workflow. It sets up **how the
agents and the workflow operate**, not what you build with. It is intentionally free
of any tech stack.

## What a new project gets from this template

- **Project memory**: `AGENTS.md` (with `CLAUDE.md` symlinked to it) that extends the
  global `~/.claude/AGENTS.md`, never duplicating the global preferences.
- **Planning convention**: planning scratch lives in `.claude/plan/`, gitignored.
- **Issue-driven work**: GitHub Issues is the source of truth. The `/new-project`
  skill creates the standard labels (`feature`, `defect`, `chore`, `e2e`, `epic`).
- **Shipping through the no-mistakes gate**: `git push no-mistakes`, never straight to
  origin.
- **Session commands** (`.claude/commands/`): `/start` (orient from the last handoff +
  open issues + real git/CI state), `/capture` (flush decisions to ADRs and work to
  Issues, incrementally), `/wrap` (end-of-session capture + doc reconcile + session-log +
  handoff), `/check` (local quality gate before the no-mistakes gate).
- **Review subagents** (`.claude/agents/`): `engineering-lead`, `design-reviewer`,
  `test-engineer`. Add domain-specific agents per project.
- **Docs scaffolding**: `docs/adr/` (architecture decision records) and
  `docs/session-log.md` (session journal), which `/capture` and `/wrap` maintain.

## Deliberately no tech stack

Choose the stack from the project's requirements, not up front. `AGENTS.md` keeps
Stack / Run / Tests as `TBD` until the requirements are understood and the decision
is made. Do not add a framework, build tool, or language scaffold to this template.

## Usage

Recommended, via the skill:

```
/new-project <name>
```

Or directly with the GitHub CLI:

```sh
gh repo create <name> --private --template sundeepdev/project-template --clone
```

After instantiating, the `/new-project` skill sets the HTTPS origin, runs
`no-mistakes init`, points the gate remote at HTTPS, and creates the issue labels.
Then the first move is to capture the goal as epic and slice issues and understand
the requirements **before** choosing a stack.
