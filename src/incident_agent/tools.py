import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "incidents.json"


def get_incident(incident_id: str) -> dict:
    """
    Retrieve a fictional integration incident by incident ID.

    This is a read-only investigation tool.
    """

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        incidents = json.load(file)

    for incident in incidents:
        if incident["incident_id"] == incident_id:
            return incident

    return {
        "error": f"Incident {incident_id} not found"
    }

def search_logs(system: str) -> list:
    """
    Search fictional integration logs for a specific system.

    This is a read-only investigation tool.
    """

    logs_file = DATA_FILE.parent / "logs.json"

    with open(logs_file, "r", encoding="utf-8") as file:
        logs = json.load(file)

    return [
        log
        for log in logs
        if log["system"].lower() == system.lower()
    ]

def get_api_metrics(system: str) -> dict:
    """
    Retrieve fictional API performance metrics for a specific system.

    This is a read-only investigation tool.
    """

    metrics_file = DATA_FILE.parent / "metrics.json"

    with open(metrics_file, "r", encoding="utf-8") as file:
        metrics = json.load(file)

    for metric in metrics:
        if metric["system"].lower() == system.lower():
            return metric

    return {
        "error": f"No metrics found for {system}"
    }

def get_recent_changes(system: str) -> list:
    """
    Retrieve recent fictional changes for a specific system.

    This is a read-only investigation tool.
    """

    changes_file = DATA_FILE.parent / "changes.json"

    with open(changes_file, "r", encoding="utf-8") as file:
        changes = json.load(file)

    return [
        change
        for change in changes
        if change["system"].lower() == system.lower()
    ]