#!/usr/bin/env bash
# Free, offline checks for the test harness: no network, no model calls.
# This is the no-mistakes Test command (.no-mistakes.yaml). The paid E2E runs
# in tests/e2e/ stay manual.
#
# Usage: tests/offline/check.sh
set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"

echo "== bash syntax"
for f in tests/*/*.sh; do
  bash -n "$f"
  echo "ok  $f"
done

echo "== python syntax and import"
python3 -I -B - tests/*/*.py <<'EOF'
import importlib.util, pathlib, sys
for path in sys.argv[1:]:
  spec = importlib.util.spec_from_file_location(pathlib.Path(path).stem, path)
  spec.loader.exec_module(importlib.util.module_from_spec(spec))
  print(f"ok  {path}")
EOF

echo "== run_metrics.py on a recorded transcript"
fixtures=tests/offline/fixtures
diff -u "$fixtures/session.expected.txt" \
  <(python3 -I -B tests/e2e/run_metrics.py "$fixtures/session")
echo "ok  matches $fixtures/session.expected.txt"
