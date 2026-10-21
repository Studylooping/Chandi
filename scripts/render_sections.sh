#!/bin/bash
# Render the given sections (resumable) and publish each finished one to the branch.
#   scripts/render_sections.sh ch2 ch13      (exit 0 only when all are published)
cd "$(dirname "$0")/.."
VENV=${VENV:-$HOME/chandi-venv}
status=0
for s in "$@"; do
  if [ -f "audio/reports/$s.json" ]; then echo "=== $s already published"; continue; fi
  echo "=== $s start $(date -u +%H:%M)"
  if "$VENV/bin/python" -m chandi.audio.recite --engine parler --section "$s" 2>&1 \
       | grep -E --line-buffered "verified|FAILED|Error|Traceback"; then :; fi
  if [ -f "out/${s}_parler-aryan.wav" ]; then
    "$VENV/bin/python" -m chandi.audio.publish --no-readme --sections "$s" 2>&1 | tail -3
  else
    echo "=== $s incomplete (some units failed); rerun to retry"; status=1
  fi
  echo "=== $s done $(date -u +%H:%M)"
done
[ $status -eq 0 ] && echo ALL_DONE
exit $status
