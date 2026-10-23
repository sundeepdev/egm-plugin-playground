#!/usr/bin/env python3
"""Tokens, wall time, subagents, and reviewer tool use for one EGM session.

Splits the session into brainstorm, draft, and review phases at the user turns
that invoked each skill, and sums usage across the main transcript and every
subagent transcript (deduped by message id). Feeds docs/egm-runs.md.

Usage: run_metrics.py ~/.claude/projects/<project-slug>
"""

import json,sys,glob,collections,datetime as dt
D=sys.argv[1]
main=max(glob.glob(D+"/*.jsonl"), key=lambda p: len(open(p).read()))
def ts(e): return dt.datetime.fromisoformat(e["timestamp"].replace("Z","+00:00"))
bounds=[]
for l in open(main):
  e=json.loads(l)
  if e.get("type")=="user" and isinstance(e.get("message",{}).get("content"),str):
    c=e["message"]["content"]
    for k,alts in (("brainstorm",("egm-brainstorm","egm_brainstorm")),("draft",("egm-draft","egm_draft")),("review",("egm-review","egm_review"))):
      if any(f"<command-name>/egm:{a}<" in c or f"<command-name>/{a}<" in c for a in alts):
        if not any(k==b[1] for b in bounds): bounds.append((ts(e),k))
bounds.sort()
def phase(t):
  p=None
  for b,k in bounds:
    if t>=b: p=k
  return p
types={}
for m in glob.glob(D+"/*/subagents/*.meta.json"):
  try: types[m.split("/")[-1].split(".")[0]]=json.load(open(m)).get("agentType")
  except: pass
stats={}; seen=set(); tools=collections.defaultdict(set); spawns=collections.Counter()
for f in [main]+glob.glob(D+"/*/subagents/*.jsonl"):
  aid=f.split("/")[-1].split(".")[0]
  for l in open(f):
    try: e=json.loads(l)
    except: continue
    if "timestamp" not in e: continue
    t=ts(e); p=phase(t)
    m=e.get("message",{})
    if isinstance(m,dict) and isinstance(m.get("content"),list):
      for b in m["content"]:
        if b.get("type")=="tool_use":
          if b["name"] in("Agent","Task"): spawns[b["input"].get("subagent_type")]+=1
          if "subagents" in f: tools[types.get(aid,"?")].add(b["name"])
    if p is None: continue
    s=stats.setdefault(p,{"in":0,"cr":0,"cw":0,"out":0,"first":t,"last":t,"sub":set()})
    s["first"]=min(s["first"],t); s["last"]=max(s["last"],t)
    if "subagents" in f: s["sub"].add(f)
    if e.get("type")=="assistant" and isinstance(m,dict) and m.get("usage"):
      key=(f,m.get("id"))
      if key in seen: continue
      seen.add(key); u=m["usage"]
      s["in"]+=u.get("input_tokens",0); s["out"]+=u.get("output_tokens",0)
      s["cr"]+=u.get("cache_read_input_tokens",0); s["cw"]+=u.get("cache_creation_input_tokens",0)
T={"in":0,"cr":0,"cw":0,"out":0,"min":0,"sub":0}
for p in ("brainstorm","draft","review"):
  s=stats.get(p)
  if not s: continue
  dur=(s["last"]-s["first"]).total_seconds()/60
  print(f"{p:10} {dur:5.1f} min | subagents {len(s['sub']):2} | uncached in {(s['in']+s['cw'])/1e3:6.0f}k | cache read {s['cr']/1e6:5.2f}M | out {s['out']/1e3:5.0f}k")
  for k in ("in","cr","cw","out"): T[k]+=s[k]
  T["min"]+=dur; T["sub"]+=len(s["sub"])
print(f"{'TOTAL':10} {T['min']:5.1f} min | subagents {T['sub']:2} | uncached in {(T['in']+T['cw'])/1e3:6.0f}k | cache read {T['cr']/1e6:5.2f}M | out {T['out']/1e3:5.0f}k")
print("spawns:", dict(spawns))
print("subagent tools:", {k:sorted(v) for k,v in tools.items()})
