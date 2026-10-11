import os
from dotenv import load_dotenv

load_dotenv()

def get_llm_provider() -> str:
    """Return the configured LLM provider, defaulting to mock."""
    return os.getenv("LLM_PROVIDER", "mock").strip().lower()


def get_gemini_api_key() -> str | None:
    """Return the Gemini API key, if configured."""
    value = os.getenv("GEMINI_API_KEY", "").strip()
    return value or None


def get_gemini_model() -> str:
    """Return the configured Gemini model name."""
    return os.getenv("GEMINI_MODEL", "").strip() or "gemini-3-flash-preview"
