#!/usr/bin/env bash
# Drive an interactive Claude Code session started by tmux_start.sh.
#
#   tmux_send.sh "<text>"            type a message and press Enter
#   tmux_send.sh --keys <keys...>    send raw tmux keys (Enter, Down, Escape...)
#   tmux_send.sh                     just wait and show the screen
#
# After sending, waits until Claude shows a menu or permission prompt, or is
# idle with no background agents (up to ~10 min), then prints the screen tail.
# Env: EGM_TMUX_SESSION (default egm), LINES_OUT (default 45).
set -u
t="${EGM_TMUX_SESSION:-egm}"
if [ "${1:-}" = "--keys" ]; then
  shift
  tmux send-keys -t "$t" "$@"
elif [ -n "${1:-}" ]; then
  tmux send-keys -t "$t" -l "$1"
  sleep 1
  tmux send-keys -t "$t" Enter
fi
sleep 15
for _ in $(seq 1 115); do
  screen=$(tmux capture-pane -t "$t" -p)
  if echo "$screen" | grep -q "Enter to select\|Do you want to proceed\|Esc to cancel"; then break; fi
  if ! echo "$screen" | grep -q "Waiting for\|esc to interrupt\|tokens *$\|↓ to manage"; then break; fi
  sleep 5
done
tmux capture-pane -t "$t" -p -S -400 | grep -v '^\s*$' | tail -"${LINES_OUT:-45}"
