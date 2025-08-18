import os

# --- Environment ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# --- Defaults ---
VALID_TONES = ["informative", "formal", "casual", "persuasive", "analytical", "narrative"]
DEFAULT_TONE = "informative"
DEFAULT_WORD_COUNT = 400
MAX_WORD_COUNT = 2000

# Prefer a widely-available, reasonably priced model; change as needed
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")