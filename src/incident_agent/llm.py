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

            incident_id = (
                prompt.split("incident ")[1]
                .split(".")[0]
            )

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