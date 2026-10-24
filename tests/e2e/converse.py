#!/usr/bin/env python3
"""Drive a multi-turn headless Claude Code session in an EGM test project.

Each call sends one user message, resuming the session recorded in
<project>/.e2e/session, appends the raw stream-json events to
<project>/.e2e/transcript.jsonl, and prints what a user would see: the
assistant's reply, any AskUserQuestion prompts, subagent spawns, files
written, and permission denials.

Create the project with setup_project.sh, which installs the official EGM
plugin into it.

Usage:
  converse.py <project_dir> <message>         # continue (or start) a session
  converse.py <project_dir> --new <message>   # start a fresh session
Env: CLAUDE_BIN (Claude Code 2.1+), EGM_PLUGIN_DIR (test a local checkout).
"""

import json
import os
import pathlib
import subprocess
import sys

ALLOWED_TOOLS = "Read Grep Glob Agent Write Edit AskUserQuestion Bash(git:*) Bash(ls:*)"


def main():
  args = sys.argv[1:]
  project = pathlib.Path(args.pop(0)).resolve()
  new = args and args[0] == "--new"
  if new:
    args.pop(0)
  message = " ".join(args)

  state = project / ".e2e"
  state.mkdir(exist_ok=True)
  session_file = state / "session"
  cmd = [os.environ.get("CLAUDE_BIN", "claude"), "-p", message,
         "--output-format", "stream-json", "--verbose",
         "--permission-mode", "acceptEdits", "--allowedTools", ALLOWED_TOOLS]
  if os.environ.get("EGM_PLUGIN_DIR"):
    cmd += ["--plugin-dir", os.environ["EGM_PLUGIN_DIR"]]
  if session_file.exists() and not new:
    cmd += ["--resume", session_file.read_text().strip()]

  proc = subprocess.run(cmd, cwd=project, capture_output=True, text=True)
  lines = [l for l in proc.stdout.splitlines() if l.startswith("{")]
  with open(state / "transcript.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps({"type": "e2e_user_turn", "message": message}) + "\n")
    f.writelines(l + "\n" for l in lines)

  for line in lines:
    e = json.loads(line)
    if e.get("session_id"):
      session_file.write_text(e["session_id"])
    if e.get("type") != "assistant":
      continue
    sub = e.get("parent_tool_use_id")
    for block in e["message"].get("content", []):
      kind = block.get("type")
      if kind == "text" and not sub:
        print(block["text"].strip(), "\n")
      elif kind == "tool_use":
        name, inp = block["name"], block["input"]
        if name in ("Agent", "Task"):
          print(f"[{'sub' if sub else 'main'} spawn] {inp.get('subagent_type')}"
                f" ({inp.get('description', '')})")
        elif name == "AskUserQuestion":
          for q in inp.get("questions", []):
            opts = " | ".join(o["label"] for o in q.get("options", []))
            print(f"[AskUserQuestion] {q['question']}\n    options: {opts}")
        elif name in ("Write", "Edit"):
          print(f"[{'sub' if sub else 'main'} {name}] {inp.get('file_path')}")

  result = next((json.loads(l) for l in reversed(lines)
                 if json.loads(l).get("type") == "result"), {})
  for d in result.get("permission_denials", []):
    print(f"[denied] {d.get('tool_name')}: {str(d.get('tool_input'))[:150]}")
  if result.get("is_error") or proc.returncode:
    print(f"[error] {result.get('result') or proc.stderr[-500:]}")
  print(f"[turn cost ${result.get('total_cost_usd', 0):.2f}]")


if __name__ == "__main__":
  main()
