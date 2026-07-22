"""
LLM 客户端抽象
==============

支持：
- OpenAI 兼容 API（OpenAI / Together / DeepSeek）
- Anthropic API（Claude 系列）
- Mock 模式（无 API 密钥时使用，确定性随机输出）

所有调用都返回统一的 (text, token_count, latency_ms) 三元组。
"""

from __future__ import annotations

import os
import random
import time
from dataclasses import dataclass
from typing import Protocol


@dataclass
class LLMResponse:
    text: str
    token_count: int
    latency_ms: float


class LLMClient(Protocol):
    def complete(self, prompt: str, system: str = "", max_tokens: int = 512) -> LLMResponse: ...


class MockClient:
    """无密钥时使用的本地随机客户端。"""

    def __init__(self, model_id: str, seed: int = 0) -> None:
        self.model_id = model_id
        self._rng = random.Random(seed)

    def complete(self, prompt: str, system: str = "", max_tokens: int = 512) -> LLMResponse:
        # 用 prompt 长度 + rng 模拟"思考 + 动作"
        start = time.time()
        seed_phrase = prompt[-200:] if len(prompt) > 200 else prompt
        self._rng.seed(hash(seed_phrase) & 0xFFFFFFFF)
        thought = "考虑当前库存、价格与现金流。" if self._rng.random() < 0.7 else "我需要先确认需求。"
        actions = ["restock", "set_price", "wait", "email_supplier"]
        action = self._rng.choice(actions)
        amount = self._rng.randint(1, 20)
        text = (
            f"<think>{thought}</think>\n"
            f"<action>{action}(amount={amount})</action>"
        )
        token_count = len(text.split())
        latency = (time.time() - start) * 1000 + self._rng.randint(50, 200)
        return LLMResponse(text=text, token_count=token_count, latency_ms=latency)


class OpenAIClient:
    """OpenAI 兼容 API 客户端。也兼容 DeepSeek / Together 等供应商。"""

    def __init__(self, model_id: str, api_key: str | None = None, base_url: str | None = None) -> None:
        self.model_id = model_id
        # DeepSeek 默认 base_url；其他 OpenAI 兼容供应商可由环境变量覆盖
        self.api_key = (
            api_key
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("DEEPSEEK_API_KEY")
        )
        if base_url is None:
            base_url = os.environ.get("OPENAI_BASE_URL")
        if "deepseek" in model_id.lower() and base_url is None:
            base_url = "https://api.deepseek.com"
        self.base_url = base_url
        if not self.api_key:
            env_hint = (
                "OPENAI_API_KEY / DEEPSEEK_API_KEY"
                if "deepseek" in model_id.lower()
                else "OPENAI_API_KEY"
            )
            raise ValueError(f"{env_hint} not set")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ImportError("pip install openai") from exc
        self._client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self._is_deepseek = "deepseek" in model_id.lower()
        self._thinking_mode = model_id.lower().endswith("-thinking")

    def complete(self, prompt: str, system: str = "", max_tokens: int = 512) -> LLMResponse:
        start = time.time()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": self.model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        # DeepSeek V4 thinking 模式：通过模型名 -thinking 后缀启用
        # 关闭 thinking：把模型名换成 deepseek-v4-flash 即可
        if self._is_deepseek:
            # V4 Flash 兼容 OpenAI chat.completions；thinking 模式仅在显式
            # 调用 -thinking 模型名时启用。无需额外参数。
            pass

        resp = self._client.chat.completions.create(**kwargs)
        text = resp.choices[0].message.content or ""
        token_count = resp.usage.completion_tokens if resp.usage else len(text.split())
        latency = (time.time() - start) * 1000
        return LLMResponse(text=text, token_count=token_count, latency_ms=latency)

    def health_check(self) -> bool:
        """快速探测 API 凭据是否有效；无效时返回 False。"""
        try:
            self._client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=1,
            )
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"[health] {self.model_id} unreachable: {exc}")
            return False


class AnthropicClient:
    """Anthropic Claude 客户端。"""

    def __init__(self, model_id: str, api_key: str | None = None) -> None:
        self.model_id = model_id
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise ImportError("pip install anthropic") from exc
        self._client = Anthropic(api_key=self.api_key)

    def complete(self, prompt: str, system: str = "", max_tokens: int = 512) -> LLMResponse:
        start = time.time()
        kwargs = {
            "model": self.model_id,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system
        resp = self._client.messages.create(**kwargs)
        text = ""
        for block in resp.content:
            if hasattr(block, "text"):
                text += block.text
        token_count = resp.usage.output_tokens if resp.usage else len(text.split())
        latency = (time.time() - start) * 1000
        return LLMResponse(text=text, token_count=token_count, latency_ms=latency)

    def health_check(self) -> bool:
        """快速探测 API 凭据是否有效。"""
        try:
            self._client.messages.create(
                model=self.model_id,
                max_tokens=1,
                messages=[{"role": "user", "content": "ping"}],
            )
            return True
        except Exception as exc:  # noqa: BLE001
            print(f"[health] {self.model_id} unreachable: {exc}")
            return False


def build_client(model_id: str, seed: int = 0, health_check: bool = True) -> LLMClient:
    """根据模型 ID 选择最合适的客户端；无密钥、缺包或 health check 失败时回退到 Mock。

    health_check=True 时，初始化后会做一次小请求探测 API 凭据是否有效。
    health_check=False 时，仍会启用懒探测：第一次真实调用失败自动切到 Mock。
    """
    model_lower = model_id.lower()
    candidate: LLMClient | None = None
    if "claude" in model_lower:
        try:
            candidate = AnthropicClient(model_id)
        except (ValueError, ImportError) as exc:
            print(f"[warn] falling back to Mock for {model_id}: {exc}")
    if candidate is None and any(k in model_lower for k in ["gpt", "llama", "qwen", "deepseek"]):
        try:
            candidate = OpenAIClient(model_id)
        except (ValueError, ImportError) as exc:
            print(f"[warn] falling back to Mock for {model_id}: {exc}")

    if candidate is None:
        return MockClient(model_id, seed)

    if health_check:
        if getattr(candidate, "health_check", lambda: True)():
            return candidate
        print(f"[warn] {model_id} failed health check, falling back to Mock")
        return MockClient(model_id, seed)

    # 懒探测包装：第一次 complete 失败，自动切到 Mock。
    return _LazyMockFallback(candidate, model_id, seed)


class _LazyMockFallback:
    """把真实客户端的失败透明地转回 Mock 客户端。"""

    def __init__(self, primary: LLMClient, model_id: str, seed: int) -> None:
        self._primary = primary
        self._fallback = MockClient(model_id, seed)
        self._use_fallback = False
        self.model_id = model_id

    def complete(self, prompt: str, system: str = "", max_tokens: int = 512) -> LLMResponse:
        if self._use_fallback:
            return self._fallback.complete(prompt, system, max_tokens)
        try:
            return self._primary.complete(prompt, system, max_tokens)
        except Exception as exc:  # noqa: BLE001
            print(f"[lazy] {self.model_id} failed ({type(exc).__name__}); switching to Mock for this run")
            self._use_fallback = True
            return self._fallback.complete(prompt, system, max_tokens)