#!/usr/bin/env bash
# End-to-end check: run EGM's review loop headlessly against the fixture
# design doc on a throwaway project with the official EGM plugin installed,
# then assert on the transcript and outputs with check_review_run.py.
#
# Usage: tests/e2e/run_review_e2e.sh [output_dir]
# Env: CLAUDE_BIN (Claude Code 2.1+), EGM_PLUGIN_DIR (test a local checkout).
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
out="${1:-$(mktemp -d)}"
claude="${CLAUDE_BIN:-claude}"

mkdir -p "$out"
"$here/setup_project.sh" "$out/project" >/dev/null

plugin_args=()
if [ -n "${EGM_PLUGIN_DIR:-}" ]; then plugin_args=(--plugin-dir "$EGM_PLUGIN_DIR"); fi

prompt='/egm:egm-review-loop TargetFile=docs/designs/url_shortener.md
SemanticTarget=full file
Reviewers=[design_critic, zoom_out]
Standards={design_critic: feature-spec-standard, zoom_out: zoom-out-standard}
GoldfishContext=[docs/designs/url_shortener.md]

This is a non-interactive test run with no user present. Run one review
iteration, save goldfish_review_report.md in the working directory, then stop
at the first decision gate without applying fixes or editing the target file.'

(cd "$out/project" && "$claude" -p "$prompt" ${plugin_args[@]+"${plugin_args[@]}"} \
  --output-format stream-json --verbose \
  --permission-mode acceptEdits \
  --allowedTools "Read Grep Glob Agent Write Edit Bash(git:*) Bash(ls:*) Bash(wc:*)" \
  > "$out/transcript.jsonl")

echo "transcript: $out/transcript.jsonl"
python3 "$here/check_review_run.py" "$out/transcript.jsonl" "$out/project"
