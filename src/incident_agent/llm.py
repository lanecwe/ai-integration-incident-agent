class LLMClient:
    """
    Interface for the language model used by the incident agent.
    """

    def generate(self, prompt: str) -> dict:
        raise NotImplementedError


class MockLLM(LLMClient):
    """
    Fake LLM used to simulate tool selection.

    This will later be replaced by a real LLM.
    """

    def generate(self, prompt: str) -> dict:

        prompt_lower = prompt.lower()

        # First step: retrieve the incident.
        if "no tools have been used" in prompt_lower:

            import re

            match = re.search(
                r"\bincident\s+(INC-\d+)\b",
                prompt,
                re.IGNORECASE,
            )

            incident_id = match.group(1) if match else "INC-1001"

            return {
                "action": "get_incident",
                "arguments": {
                    "incident_id": incident_id
                }
            }

        # After the incident: investigate logs.
        if "last tool executed: get_incident" in prompt_lower:

            system = self._extract_system(prompt)

            return {
                "action": "search_logs",
                "arguments": {
                    "system": system
                }
            }

        # After logs: investigate API metrics.
        if "last tool executed: search_logs" in prompt_lower:

            system = self._extract_system(prompt)

            return {
                "action": "get_api_metrics",
                "arguments": {
                    "system": system
                }
            }

        # After metrics: investigate recent changes.
        if "last tool executed: get_api_metrics" in prompt_lower:

            system = self._extract_system(prompt)

            return {
                "action": "get_recent_changes",
                "arguments": {
                    "system": system
                }
            }

        # After recent changes: finish.
        if "last tool executed: get_recent_changes" in prompt_lower:

            return {
                "action": "finish",
                "arguments": {}
            }

        return {
            "action": "finish",
            "arguments": {}
        }

    @staticmethod
    def _extract_system(prompt: str) -> str:

        marker = "affected system:"

        if marker in prompt.lower():

            value = prompt.lower().split(marker, 1)[1]

            return value.split("\n")[0].strip()

        return "Customer Sync API"


class GeminiLLM(LLMClient):
    """
    Real Gemini LLM for selecting incident investigation tools.
    Returns the same dictionary structure as MockLLM.
    """

    def __init__(self):
        import json

        from google import genai
        from src.incident_agent.config import (
            get_gemini_api_key,
            get_gemini_model,
        )

        api_key = get_gemini_api_key()

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=api_key)
        self.model = get_gemini_model()
        self._json = json

    def generate(self, prompt: str) -> dict:
        instruction = """
You are an AI integration incident investigation agent.

Choose the next action based on the investigation context.
Return only a valid JSON object with this structure:
{
  "action": "tool_name_or_finish",
  "arguments": {}
}

Rules:
- Use only tool names provided in the prompt.
- Use the required arguments for the selected tool.
- Follow the investigation sequence and existing evidence.
- Do not invent tool results.
- If the investigation is complete, return action "finish"
  with empty arguments.
- Return JSON only, without Markdown fences.
- Use only the arguments defined for each tool.
- For get_api_metrics, provide only the "system" argument.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{instruction}\n\nInvestigation context:\n{prompt}",
            config={
                "response_mime_type": "application/json",
            },
        )

        result = self._json.loads(response.text)

        if not isinstance(result, dict):
            raise ValueError("Gemini returned an invalid response")

        if not isinstance(result.get("action"), str):
            raise ValueError("Gemini response is missing a valid action")

        if not isinstance(result.get("arguments"), dict):
            raise ValueError("Gemini response is missing valid arguments")

        return result
