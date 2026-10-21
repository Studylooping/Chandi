#!/bin/bash
# One-time setup of a render environment (CPU). Needs HF_TOKEN with access to ai4bharat/indic-parler-tts.
set -euo pipefail
cd "$(dirname "$0")/.."
VENV=${VENV:-$HOME/chandi-venv}
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu
  "$VENV/bin/pip" install -q git+https://github.com/huggingface/parler-tts.git
  # parler-tts may pull a mismatched torch/torchaudio; pin the CPU pair again
  "$VENV/bin/pip" install -q torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu
  "$VENV/bin/pip" install -q indic_transliteration==2.3.82 pylibrb==0.1.2 soundfile pytest
fi
"$VENV/bin/python" -m chandi.corpus
"$VENV/bin/python" -m chandi.analyze > /dev/null
"$VENV/bin/python" -m pytest -q tests
echo "setup ok: $VENV"
