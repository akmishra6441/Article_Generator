import pytest
from generator import generate_article
from config import DEFAULT_TONE

class DummyResp:
    def __init__(self, text):
        self.text = text


def test_empty_topic_raises_value_error(monkeypatch):
    with pytest.raises(ValueError):
        generate_article(topic="", tone=DEFAULT_TONE, word_count=200)


def test_invalid_tone_raises_value_error(monkeypatch):
    with pytest.raises(ValueError):
        generate_article(topic="AI in Education", tone="funny-but-unsupported", word_count=200)


def test_basic_generation_smoke(monkeypatch):
    # Monkeypatch the OpenAI call to avoid real API usage
    from generator import _call_openai

    def fake_call(prompt, temperature, model):
        return "## AI in Education\n\nThis is a test article with headings and structure."

    monkeypatch.setattr("generator._call_openai", fake_call)

    article, meta = generate_article(topic="AI in Education", tone=DEFAULT_TONE, word_count=200)
    assert "##" in article
    assert meta["tone"] == DEFAULT_TONE