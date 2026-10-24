#!/usr/bin/env bash
# Start an interactive Claude Code session in tmux on a fresh EGM test project,
# for driving brainstorm/draft/review end to end with tmux_send.sh.
#
# Usage: tests/e2e/tmux_start.sh <dest_dir>
# Then answer the folder-trust prompt: tmux_send.sh --keys Down Enter
# Stop with: tmux kill-session -t "${EGM_TMUX_SESSION:-egm}"
# Env: CLAUDE_BIN, EGM_PLUGIN_DIR (see setup_project.sh), EGM_TMUX_SESSION.
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
dest="$1"
t="${EGM_TMUX_SESSION:-egm}"
claude="${CLAUDE_BIN:-claude}"

"$here/setup_project.sh" "$dest" >/dev/null
dest="$(cd "$dest" && pwd)"

cmd="'$claude' --permission-mode acceptEdits"
cmd+=" --allowedTools 'Read Grep Glob Agent Write Edit AskUserQuestion Bash(git:*) Bash(ls:*)'"
if [ -n "${EGM_PLUGIN_DIR:-}" ]; then cmd+=" --plugin-dir '$EGM_PLUGIN_DIR'"; fi

tmux new-session -d -s "$t" -x 200 -y 60 -c "$dest" "$cmd"
sleep 7
tmux capture-pane -t "$t" -p | grep -v '^\s*$' | tail -12
echo "project: $dest  (tmux session: $t)"
