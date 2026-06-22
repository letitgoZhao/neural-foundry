# Qwen3-1.7B 仙宫云部署指南

本文档用于在仙宫云的一张 RTX 4090 GPU 机器上，用 vLLM 部署 `Qwen/Qwen3-1.7B`，并通过 OpenAI-compatible Chat Completions API 做基本测试。

## 1. 目录约定

Git 仓库只保存代码、配置和文档。模型权重、缓存、训练数据、运行日志、LoRA adapter 等大文件放到机器持久盘：

```text
/data/neural-foundry/
  hf-cache/
  datasets/
  runs/
  artifacts/
  logs/
```

首次部署前创建缓存目录：

```bash
sudo mkdir -p /data/neural-foundry/hf-cache
sudo chown -R "$USER:$USER" /data/neural-foundry
```

## 2. Python/vLLM 部署

进入仓库后执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install "vllm>=0.9.0"
```

启动服务：

```bash
bash deploy/vllm/serve-qwen3-1.7b.sh
```

默认服务地址是：

```text
http://<机器公网IP>:8000/v1
```

如果 Hugging Face 下载较慢，可以改用 ModelScope：

```bash
source .venv/bin/activate
pip install modelscope
VLLM_USE_MODELSCOPE=true bash deploy/vllm/serve-qwen3-1.7b.sh
```

## 3. Docker Compose 备选方案

如果仙宫云镜像已经装好 NVIDIA Container Toolkit，可以直接用容器：

```bash
docker compose \
  --env-file configs/qwen3-1.7b.env.example \
  -f deploy/vllm/docker-compose.yml \
  up
```

停止服务：

```bash
docker compose \
  --env-file configs/qwen3-1.7b.env.example \
  -f deploy/vllm/docker-compose.yml \
  down
```

## 4. 测试服务

在另一个终端运行：

```bash
python scripts/smoke_chat.py
```

它会发送两个默认 prompt：

```text
请用三句话介绍 vLLM，并说明它为什么适合部署 Qwen3-1.7B。
```

```text
写一个 Python 函数，输入整数 n，返回斐波那契数列前 n 项，并解释边界情况。
```

也可以用 curl 手动测试：

```bash
curl http://127.0.0.1:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-1.7B",
    "messages": [
      {"role": "user", "content": "请用三句话介绍 vLLM，并说明它为什么适合部署 Qwen3-1.7B。"}
    ],
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "presence_penalty": 1.5,
    "max_tokens": 512,
    "chat_template_kwargs": {"enable_thinking": false}
  }'
```

## 5. 常见调整

如果显存占用太保守，可以把 `configs/qwen3-1.7b.env.example` 里的 `MAX_MODEL_LEN` 从 `8192` 调到 `16384` 或 `32768`。

如果服务启动时 OOM，先降低：

```bash
MAX_MODEL_LEN=4096 GPU_MEMORY_UTILIZATION=0.70 bash deploy/vllm/serve-qwen3-1.7b.sh
```

如果只想做普通快速问答，不想输出思考内容，测试请求里保留：

```json
"chat_template_kwargs": {"enable_thinking": false}
```

如果后续要做 LoRA/QLoRA 微调，建议继续沿用同一个基座模型名 `Qwen/Qwen3-1.7B`，训练输出放在：

```text
/data/neural-foundry/artifacts/adapters/qwen3-1.7b/
```
