"""
Single entry point for all Claude calls.
Change MODEL here to affect every agent at once.
"""
from __future__ import annotations
import os
import anthropic

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
MODEL_FAST = os.getenv("CLAUDE_MODEL_FAST", "claude-haiku-4-5-20251001")  # orchestrateur, tâches simples
MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "800"))

_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client


def call_claude(
    system: str,
    user: str,
    max_tokens: int = MAX_TOKENS,
    cache_system: bool = False,
    fast: bool = False,
) -> str:
    model = MODEL_FAST if fast else MODEL
    system_block = (
        [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]
        if cache_system
        else system
    )
    response = get_client().messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_block,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text.strip()
