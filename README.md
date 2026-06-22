# neural-foundry

Qwen3-1.7B deployment scaffold for a single RTX 4090 GPU.

This repository keeps only deployment code, configs, smoke tests, and docs. Large runtime assets such as model weights, datasets, checkpoints, LoRA adapters, and logs should stay outside Git, for example under `/data/neural-foundry`.

## What It Provides

- `deploy/vllm/serve-qwen3-1.7b.sh`: starts a vLLM OpenAI-compatible API server.
- `deploy/vllm/docker-compose.yml`: optional Docker Compose deployment.
- `scripts/smoke_chat.py`: sends two Chinese test prompts to the running API.
- `configs/qwen3-1.7b.env.example`: tunable deployment defaults.
- `docs/DEPLOY-CN.md`: Chinese deployment and testing guide for cloud use.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install "vllm>=0.9.0"

bash deploy/vllm/serve-qwen3-1.7b.sh
```

In another terminal:

```bash
python scripts/smoke_chat.py
```

Read [docs/DEPLOY-CN.md](docs/DEPLOY-CN.md) for the full Chinese guide.
