import os
import re
import time
from typing import Tuple, Dict, Optional

from config import (
    OPENAI_API_KEY,
    DEFAULT_TONE,
    DEFAULT_WORD_COUNT,
    MAX_WORD_COUNT,
    VALID_TONES,
    DEFAULT_MODEL,
)

# --- OpenAI client (Python SDK v1.x) ---
try:
    from openai import OpenAI
    _client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else OpenAI()
except Exception as e:
    _client = None

# Helper: slugify for filenames
_slug_re = re.compile(r"[^a-zA-Z0-9]+")

def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = _slug_re.sub("-", text).strip("-")
    return text or f"article-{int(time.time())}"

# Public API
VALID_TONES = VALID_TONES

SYSTEM_MSG = (
    "You are a helpful writing assistant that crafts well-structured, factual, and engaging articles. "
    "Always include a concise introduction, clear section headings, and a brief conclusion."
)

PROMPT_TEMPLATE = (
    "Write an {tone} article about: '{topic}'.\n"
    "Target length: around {word_count} words.\n"
    "Include these keywords if provided: {keywords}.\n"
    "If outline_first is true, first decide on 3-6 section headings and then write the article with those headings.\n"
    "Use Markdown formatting with H2/H3 for sections."
)


def _validate_inputs(topic: str, tone: str, word_count: int):
    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")
    if tone not in VALID_TONES:
        raise ValueError(f"Unsupported tone '{tone}'. Choose one of: {', '.join(VALID_TONES)}")
    if not isinstance(word_count, int) or word_count <= 0:
        raise ValueError("Word count must be a positive integer.")
    if word_count > MAX_WORD_COUNT:
        raise ValueError(f"Word count too high (>{MAX_WORD_COUNT}).")


def _call_openai(prompt: str, temperature: float, model: str) -> str:
    if _client is None:
        raise RuntimeError("OpenAI client not initialized. Check installation and API key.")
    # Prefer Chat Completions for broad compatibility
    try:
        resp = _client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_MSG},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        # Fallback to Responses API if available
        resp = _client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": SYSTEM_MSG},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return resp.output_text.strip()


def generate_article(
    topic: str,
    tone: str = DEFAULT_TONE,
    word_count: int = DEFAULT_WORD_COUNT,
    keywords: Optional[str] = "",
    temperature: float = 0.7,
    outline_first: bool = True,
    model: Optional[str] = None,
) -> Tuple[str, Dict[str, str]]:
    """Generate an article and return (article_markdown, metadata)."""
    _validate_inputs(topic, tone, int(word_count))

    # Build prompt
    prompt = PROMPT_TEMPLATE.format(
        tone=tone,
        topic=topic.strip(),
        word_count=int(word_count),
        keywords=keywords.strip() or "(none)",
    )
    if outline_first:
        prompt += "\nOutline_first: true"

    chosen_model = model or DEFAULT_MODEL
    content = _call_openai(prompt=prompt, temperature=temperature, model=chosen_model)

    # Light post-processing: make sure headings present
    if "## " not in content:
        content = f"## {topic}\n\n" + content

    meta = {
        "tone": tone,
        "word_count": str(word_count),
        "model": chosen_model,
        "slug": _slugify(topic),
    }
    return content, meta