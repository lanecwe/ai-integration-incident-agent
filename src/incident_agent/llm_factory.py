
import logging

from src.incident_agent.config import (
    get_gemini_api_key,
    get_llm_provider,
)
from src.incident_agent.llm import GeminiLLM, MockLLM

logger = logging.getLogger(__name__)



class FallbackLLM:
    """Use Gemini when available; switch to MockLLM if it fails."""

    def __init__(self, primary, fallback):
        self.primary = primary
        self.fallback = fallback
        self.using_fallback = False
        self.fallback_just_activated = False

    def generate(self, prompt: str) -> dict:
        self.fallback_just_activated = False

        if self.using_fallback:
            return self.fallback.generate(prompt)

        try:
            return self.primary.generate(prompt)
        except Exception:
            logger.exception(
                "Primary LLM failed. Switching to MockLLM."
            )
            self.using_fallback = True
            self.fallback_just_activated = True
            return self.fallback.generate(prompt)


def create_llm():
    """Create the configured LLM with MockLLM as the fallback."""

    provider = get_llm_provider()

    if provider == "mock":
        return MockLLM()

    if provider == "gemini":
        if not get_gemini_api_key():
            logger.warning(
                "Gemini API key missing. Using MockLLM."
            )
            return MockLLM()

        try:
            return FallbackLLM(
                primary=GeminiLLM(),
                fallback=MockLLM(),
            )
        except Exception:
            logger.exception(
                "Gemini initialisation failed. Using MockLLM."
            )
            return MockLLM()

    logger.warning(
        "Unsupported LLM provider '%s'. Using MockLLM.",
        provider,
    )
    return MockLLM()
