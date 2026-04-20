"""
Single entry point for all Claude calls.
Change MODEL here to affect every agent at once.
"""
import os
import anthropic

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "800"))

_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client


def call_claude(system: str, user: str, max_tokens: int = MAX_TOKENS) -> str:
    response = get_client().messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text.strip()
