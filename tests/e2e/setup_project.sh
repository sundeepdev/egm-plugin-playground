#!/usr/bin/env bash
# Create a throwaway copy of the fixture project with the official EGM plugin
# (google/elephant-goldfish-model) installed at project scope.
#
# Usage: tests/e2e/setup_project.sh <dest_dir>
# Set EGM_PLUGIN_DIR to test a local EGM checkout instead: nothing is
# installed, and callers pass --plugin-dir "$EGM_PLUGIN_DIR" to claude.
# Set CLAUDE_BIN to pick a Claude Code binary (needs plugin support, 2.1+).
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
dest="$1"
claude="${CLAUDE_BIN:-claude}"

if [ -e "$dest" ]; then
  echo "refusing to reuse existing $dest" >&2
  exit 1
fi
cp -R "$here/fixture-project" "$dest"
git -C "$dest" init -q
git -C "$dest" add -A
git -C "$dest" -c user.name=e2e -c user.email=e2e@example.invalid \
  commit -qm fixture

if [ -z "${EGM_PLUGIN_DIR:-}" ]; then
  # Idempotent; the marketplace is registered in user settings, the plugin
  # is enabled only in $dest/.claude/settings.json.
  "$claude" plugin marketplace add google/elephant-goldfish-model >/dev/null
  "$claude" plugin marketplace update egm >/dev/null
  (cd "$dest" && "$claude" plugin install egm@egm --scope project >/dev/null)
fi
echo "$dest"
