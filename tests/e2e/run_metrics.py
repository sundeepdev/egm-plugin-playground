#!/usr/bin/env python3
"""Tokens, wall time, subagents, and reviewer tool use for one EGM session.

Splits the session into brainstorm, draft, and review phases at the user turns
that invoked each skill, and sums usage across the main transcript and every
subagent transcript (deduped by message id). Feeds docs/egm-runs.md.

Usage: run_metrics.py ~/.claude/projects/<project-slug>
"""

import collections
import datetime as dt
import glob
import json
import pathlib
import sys

# Phase -> command names that start it (upstream folder and frontmatter names).
PHASES = (
    ("brainstorm", ("egm-brainstorm", "egm_brainstorm")),
    ("draft", ("egm-draft", "egm_draft")),
    ("review", ("egm-review", "egm_review")),
)


def timestamp(event):
  return dt.datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))


def read_events(path):
  with open(path, encoding="utf-8") as f:
    for line in f:
      try:
        yield json.loads(line)
      except json.JSONDecodeError:
        continue


def phase_starts(main_transcript):
  """First user turn that invoked each phase's skill, sorted by time."""
  starts = {}
  for e in read_events(main_transcript):
    content = e.get("message", {}).get("content")
    if e.get("type") != "user" or not isinstance(content, str):
      continue
    for phase, names in PHASES:
      if phase not in starts and any(
          f"<command-name>/egm:{n}<" in content or f"<command-name>/{n}<" in content
          for n in names):
        starts[phase] = timestamp(e)
  return sorted((t, phase) for phase, t in starts.items())


def summarize(project_dir):
  main = max(glob.glob(f"{project_dir}/*.jsonl"),
             key=lambda p: pathlib.Path(p).stat().st_size)
  starts = phase_starts(main)

  def phase_at(t):
    current = None
    for start, phase in starts:
      if t >= start:
        current = phase
    return current

  agent_types = {}
  for meta in sorted(glob.glob(f"{project_dir}/*/subagents/*.meta.json")):
    with open(meta, encoding="utf-8") as f:
      agent_types[pathlib.Path(meta).name.split(".")[0]] = json.load(f).get("agentType")

  stats, seen = {}, set()
  tools, spawns = collections.defaultdict(set), collections.Counter()
  # Sorted so output order is the same on every filesystem.
  for path in [main] + sorted(glob.glob(f"{project_dir}/*/subagents/*.jsonl")):
    is_sub = "/subagents/" in path
    agent_id = pathlib.Path(path).name.split(".")[0]
    for e in read_events(path):
      if "timestamp" not in e:
        continue
      t = timestamp(e)
      message = e.get("message", {})
      if isinstance(message, dict) and isinstance(message.get("content"), list):
        for block in message["content"]:
          if block.get("type") != "tool_use":
            continue
          if block["name"] in ("Agent", "Task"):
            spawns[block["input"].get("subagent_type")] += 1
          if is_sub:
            tools[agent_types.get(agent_id, "?")].add(block["name"])
      phase = phase_at(t)
      if phase is None:
        continue
      s = stats.setdefault(phase, {"in": 0, "cr": 0, "cw": 0, "out": 0,
                                   "first": t, "last": t, "sub": set()})
      s["first"], s["last"] = min(s["first"], t), max(s["last"], t)
      if is_sub:
        s["sub"].add(path)
      usage = message.get("usage") if isinstance(message, dict) else None
      # Streaming writes one entry per content block, all with the same usage.
      if e.get("type") == "assistant" and usage and (path, message.get("id")) not in seen:
        seen.add((path, message.get("id")))
        s["in"] += usage.get("input_tokens", 0)
        s["out"] += usage.get("output_tokens", 0)
        s["cr"] += usage.get("cache_read_input_tokens", 0)
        s["cw"] += usage.get("cache_creation_input_tokens", 0)
  return stats, spawns, tools


def row(label, minutes, subagents, s):
  return (f"{label:10} {minutes:5.1f} min | subagents {subagents:2} | "
          f"uncached in {(s['in'] + s['cw']) / 1e3:6.0f}k | "
          f"cache read {s['cr'] / 1e6:5.2f}M | out {s['out'] / 1e3:5.0f}k")


def main():
  stats, spawns, tools = summarize(sys.argv[1])
  total = {"in": 0, "cr": 0, "cw": 0, "out": 0}
  total_min = total_sub = 0
  for phase, _ in PHASES:
    s = stats.get(phase)
    if not s:
      continue
    minutes = (s["last"] - s["first"]).total_seconds() / 60
    print(row(phase, minutes, len(s["sub"]), s))
    for k in total:
      total[k] += s[k]
    total_min += minutes
    total_sub += len(s["sub"])
  print(row("TOTAL", total_min, total_sub, total))
  print("spawns:", dict(spawns))
  print("subagent tools:", {k: sorted(v) for k, v in tools.items()})


if __name__ == "__main__":
  main()
