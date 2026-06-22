from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL_ID = "Qwen/Qwen3-1.7B"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_required_deployment_files_exist():
    required = [
        ".gitignore",
        "README.md",
        "docs/DEPLOY-CN.md",
        "configs/qwen3-1.7b.env.example",
        "deploy/vllm/serve-qwen3-1.7b.sh",
        "deploy/vllm/docker-compose.yml",
        "scripts/smoke_chat.py",
    ]

    missing = [path for path in required if not (ROOT / path).is_file()]

    assert missing == []


def test_vllm_script_targets_qwen3_1_7b():
    script = read("deploy/vllm/serve-qwen3-1.7b.sh")

    assert MODEL_ID in script
    assert "vllm serve" in script
    assert "--host" in script
    assert "--port" in script
    assert "--max-model-len" in script
    assert "--gpu-memory-utilization" in script
    assert "--reasoning-parser qwen3" in script


def test_smoke_client_and_guide_include_test_prompts():
    client = read("scripts/smoke_chat.py")
    guide = read("docs/DEPLOY-CN.md")

    assert MODEL_ID in client
    assert "http://127.0.0.1:8000/v1" in client
    assert "仙宫云" in guide
    assert "请用三句话介绍 vLLM" in guide
    assert "写一个 Python 函数" in guide


def test_large_runtime_artifacts_are_ignored():
    gitignore = read(".gitignore")

    for pattern in [
        ".venv/",
        "models/",
        "datasets/",
        "runs/",
        "artifacts/",
        "logs/",
        "*.safetensors",
        "*.gguf",
    ]:
        assert pattern in gitignore
