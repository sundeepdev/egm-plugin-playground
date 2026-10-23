# egm-plugin-playground

End-to-end tests for Google's
[Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) (EGM)
plugin in Claude Code. The tests install the official plugin into a throwaway
fixture project and run it the way a user would.

This repo first carried its own Claude Code port of EGM. Upstream shipped official
Claude Code support on 2026-10-22, so the port was dropped
([ADR 0001](docs/adr/0001-use-official-egm-plugin.md)). Results of full runs are in
[docs/egm-runs.md](docs/egm-runs.md).

## Layout

```
tests/e2e/fixture-project/   48-line URL-shortener design with planted flaws + app/redirect.py
tests/e2e/setup_project.sh   copy the fixture to a new dir and install egm@egm (project scope)
tests/e2e/run_review_e2e.sh  headless review-loop run + transcript assertions
tests/e2e/check_review_run.py  the assertions
tests/e2e/run_metrics.py     tokens/time/subagents for a finished session
tests/e2e/converse.py        drive a multi-turn headless session (claude -p --resume)
tests/e2e/tmux_start.sh      start an interactive session in tmux on a fresh project
tests/e2e/tmux_send.sh       type into it and wait for the next gate
```

## Requirements

- Claude Code 2.1 or later, logged in (`claude --version`)
- Python 3, git, and tmux (for the interactive drivers)

Setup registers the `egm` marketplace in your user settings. The plugin itself is
enabled only inside each throwaway project.

## Headless check

```bash
tests/e2e/run_review_e2e.sh
```

This runs one review pass with two reviewers on the fixture design. It checks that:

- the plugin loaded with no errors;
- at least two `egm:` Goldfish reviewers were spawned;
- their prompts carry the resolved plugin root;
- the reviewers made no write calls;
- `goldfish_review_report.md` was written.

It uses a real model, at about $1 per run. Set `CLAUDE_BIN` to choose which Claude
Code binary runs it.

## Full interactive run

Start a session:

```bash
tests/e2e/tmux_start.sh /tmp/egm-run
```

Answer the folder-trust prompt:

```bash
tests/e2e/tmux_send.sh --keys Down Enter
```

Then start the brainstorm:

```bash
tests/e2e/tmux_send.sh "/egm:egm-brainstorm <feature idea>"
```

Continue with `tmux_send.sh "<reply>"` or `tmux_send.sh --keys Enter` at each gate.
Each call waits for the next menu or reply and prints the screen. A full brainstorm,
draft, and review run takes about 45 minutes.

## Testing a local EGM checkout

Set `EGM_PLUGIN_DIR` to a local checkout of `google/elephant-goldfish-model`. The
scripts then pass `--plugin-dir` instead of installing from the marketplace.
