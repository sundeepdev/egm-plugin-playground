#!/usr/bin/env python3
"""Assert that a headless /egm:egm-review-loop run behaved like a Goldfish review.

Reads a `claude -p --output-format stream-json --verbose` transcript and the
project directory the run used. Exits non-zero with one line per failed check.

Usage: check_review_run.py <transcript.jsonl> <project_dir>
"""

import json
import pathlib
import sys

WRITE_TOOLS = {"Write", "Edit", "NotebookEdit", "Bash"}


def main():
  transcript, project = map(pathlib.Path, sys.argv[1:3])
  events = [json.loads(line) for line in transcript.read_text().splitlines()
            if line.startswith("{")]
  failures = []

  def check(ok, message):
    print(("PASS " if ok else "FAIL ") + message)
    if not ok:
      failures.append(message)

  init = next((e for e in events
               if e.get("type") == "system" and e.get("subtype") == "init"), {})
  egm = next((p for p in init.get("plugins", []) if p.get("name") == "egm"), {})
  check(bool(egm), f"egm plugin loaded ({egm.get('source')}, {egm.get('version')})")
  check(not init.get("plugin_errors"), "no plugin load errors")

  # Tool calls made by the main agent (no parent) vs. inside subagents.
  spawns = {}       # tool_use id -> Agent input
  sub_tools = {}    # parent Agent tool_use id -> [tool names]
  for e in events:
    if e.get("type") != "assistant":
      continue
    parent = e.get("parent_tool_use_id")
    for block in e["message"].get("content", []):
      if block.get("type") != "tool_use":
        continue
      if block["name"] in ("Agent", "Task"):
        spawns[block["id"]] = block["input"]
      if parent:
        sub_tools.setdefault(parent, []).append(block["name"])

  goldfish = {i: s for i, s in spawns.items()
              if str(s.get("subagent_type", "")).startswith("egm:egm-")
              and s.get("subagent_type") not in ("egm:egm-synthesizer",
                                                 "egm:egm-bootstrap-orchestrator")}
  check(len(goldfish) >= 2,
        f"at least 2 Goldfish reviewers spawned as egm: agents "
        f"(got {sorted(s['subagent_type'] for s in spawns.values() if 'subagent_type' in s)})")

  prompts = " ".join(str(s.get("prompt", "")) for s in spawns.values())
  check("${CLAUDE_PLUGIN_ROOT}" not in prompts,
        "plugin root expanded in subagent prompts")
  # Goldfish only find their persona and standard if given the absolute root.
  check(bool(egm.get("path")) and egm["path"] in prompts,
        "subagent prompts name the plugin root path")

  writers = {spawns[i].get("subagent_type"): sorted(set(t) & WRITE_TOOLS)
             for i, t in sub_tools.items() if i in goldfish and set(t) & WRITE_TOOLS}
  check(not writers, f"Goldfish reviewers made no write calls {writers or ''}")

  check((project / "goldfish_review_report.md").is_file(),
        "goldfish_review_report.md written in the project")

  result = next((e for e in reversed(events) if e.get("type") == "result"), {})
  print(f"info: cost ${result.get('total_cost_usd', 0):.2f}, "
        f"{result.get('num_turns')} turns, {len(spawns)} subagent spawns")
  sys.exit(1 if failures else 0)


if __name__ == "__main__":
  main()
