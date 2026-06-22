#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.error
import urllib.request


DEFAULT_PROMPTS = [
    "请用三句话介绍 vLLM，并说明它为什么适合部署 Qwen3-1.7B。",
    "写一个 Python 函数，输入整数 n，返回斐波那契数列前 n 项，并解释边界情况。",
]


def post_chat(base_url: str, model: str, prompt: str, max_tokens: int) -> dict:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 20,
        "max_tokens": max_tokens,
        "presence_penalty": 1.5,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke test a local vLLM chat API.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    parser.add_argument("--model", default="Qwen/Qwen3-1.7B")
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--prompt", action="append", help="Custom prompt; can be used multiple times.")
    args = parser.parse_args()

    prompts = args.prompt or DEFAULT_PROMPTS
    for index, prompt in enumerate(prompts, start=1):
        print(f"\n=== Prompt {index} ===")
        print(prompt)
        try:
            result = post_chat(args.base_url, args.model, prompt, args.max_tokens)
        except urllib.error.URLError as exc:
            print(f"Request failed: {exc}", file=sys.stderr)
            return 1

        message = result["choices"][0]["message"]
        reasoning = message.get("reasoning_content")
        if reasoning:
            print("\n--- reasoning_content ---")
            print(reasoning.strip())
        print("\n--- content ---")
        print(message.get("content", "").strip())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
