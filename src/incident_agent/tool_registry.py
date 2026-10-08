from src.incident_agent.tools import (
    get_incident,
    search_logs,
    get_api_metrics,
    get_recent_changes,
)


TOOLS = {
    "get_incident": {
        "function": get_incident,
        "description": (
            "Retrieve details for a specific integration incident. "
            "This is a read-only investigation tool."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "incident_id": {
                    "type": "string",
                    "description": "The unique incident ID, for example INC-1001.",
                }
            },
            "required": ["incident_id"],
        },
        "permission": "read_only",
        "risk_level": "low",
    },

    "search_logs": {
        "function": search_logs,
        "description": (
            "Search integration logs for a specific system. "
            "This is a read-only investigation tool."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "system": {
                    "type": "string",
                    "description": "The integration system to search.",
                }
            },
            "required": ["system"],
        },
        "permission": "read_only",
        "risk_level": "low",
    },

    "get_api_metrics": {
        "function": get_api_metrics,
        "description": (
            "Retrieve API performance metrics for a specific system. "
            "This is a read-only investigation tool."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "system": {
                    "type": "string",
                    "description": "The integration system to retrieve metrics for.",
                }
            },
            "required": ["system"],
        },
        "permission": "read_only",
        "risk_level": "low",
    },

    "get_recent_changes": {
        "function": get_recent_changes,
        "description": (
            "Retrieve recent configuration, deployment, or mapping "
            "changes for a specific system. "
            "This is a read-only investigation tool."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "system": {
                    "type": "string",
                    "description": "The integration system to investigate.",
                }
            },
            "required": ["system"],
        },
        "permission": "read_only",
        "risk_level": "low",
    },
}