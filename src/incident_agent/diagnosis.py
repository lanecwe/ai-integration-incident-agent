def diagnose_incident(evidence: dict) -> dict:
    """
    Analyse collected incident evidence and produce a diagnosis.

    This is currently deterministic.
    A real LLM will replace this logic later.
    """

    incident = evidence.get("get_incident", {})
    logs = evidence.get("search_logs", [])
    metrics = evidence.get("get_api_metrics", {})

    error_code = incident.get("error_code")
    system = incident.get("system")

    # Analyse HTTP 429 incidents.
    if error_code == "429":

        rate_limit = metrics.get("rate_limit")
        requests = metrics.get("requests_last_hour")

        rate_limit_exceeded = (
            rate_limit is not None
            and requests is not None
            and requests > rate_limit
        )

        has_rate_limit_errors = any(
            "429" in log.get("message", "")
            or "rate limit" in log.get("message", "").lower()
            for log in logs
        )

        if rate_limit_exceeded and has_rate_limit_errors:

            return {
                "root_cause": (
                    f"{system} exceeded the downstream API rate limit."
                ),
                "evidence": [
                    f"Requests last hour: {requests}",
                    f"Configured rate limit: {rate_limit}",
                    "Logs show HTTP 429 responses.",
                    "Logs show requests being rejected due to rate limiting.",
                ],
                "impact": (
                    "Customer synchronisation requests are being rejected."
                ),
                "recommendation": (
                    "Reduce request rate and consider throttling, "
                    "batching, or exponential backoff."
                ),
                "confidence": "HIGH",
                "human_approval_required": True,
            }

    # Fallback diagnosis.
    return {
        "root_cause": "Insufficient evidence to determine root cause.",
        "evidence": [],
        "impact": "Unknown",
        "recommendation": (
            "Collect additional logs, metrics, and recent change information."
        ),
        "confidence": "LOW",
        "human_approval_required": True,
    }