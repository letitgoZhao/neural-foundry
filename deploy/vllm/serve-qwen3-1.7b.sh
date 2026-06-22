#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT_DIR/configs/qwen3-1.7b.env.example}"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  set -a
  source "$ENV_FILE"
  set +a
fi

MODEL_ID="${MODEL_ID:-Qwen/Qwen3-1.7B}"
SERVED_MODEL_NAME="${SERVED_MODEL_NAME:-$MODEL_ID}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
MAX_MODEL_LEN="${MAX_MODEL_LEN:-8192}"
GPU_MEMORY_UTILIZATION="${GPU_MEMORY_UTILIZATION:-0.75}"
HF_HOME="${HF_HOME:-/data/neural-foundry/hf-cache}"
VLLM_USE_MODELSCOPE="${VLLM_USE_MODELSCOPE:-false}"
ENABLE_REASONING="${ENABLE_REASONING:-1}"
REASONING_PARSER="${REASONING_PARSER:-qwen3}"

export HF_HOME
export VLLM_USE_MODELSCOPE
mkdir -p "$HF_HOME"

if ! command -v vllm >/dev/null 2>&1; then
  echo "vllm is not installed. Install it with: pip install 'vllm>=0.9.0'" >&2
  exit 127
fi

cmd=(
  vllm serve "$MODEL_ID"
  --served-model-name "$SERVED_MODEL_NAME"
  --host "$HOST"
  --port "$PORT"
  --max-model-len "$MAX_MODEL_LEN"
  --gpu-memory-utilization "$GPU_MEMORY_UTILIZATION"
)

if [[ "$ENABLE_REASONING" == "1" || "$ENABLE_REASONING" == "true" ]]; then
  # Default reasoning args: --enable-reasoning --reasoning-parser qwen3
  cmd+=(--enable-reasoning --reasoning-parser "$REASONING_PARSER")
fi

echo "Starting vLLM:"
printf ' %q' "${cmd[@]}"
echo

exec "${cmd[@]}"
