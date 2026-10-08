import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from src.incident_agent.tool_registry import TOOLS


app = FastAPI(
    title="AI Integration Incident Agent",
    description="API for investigating integration incidents",
    version="0.1.0",
)


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "incidents.json"


def load_incidents():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "incident-agent",
    }


@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str):
    incidents = load_incidents()

    for incident in incidents:
        if incident["incident_id"] == incident_id:
            return incident

    raise HTTPException(
        status_code=404,
        detail=f"Incident {incident_id} not found",
    )

@app.get("/tools")
def list_tools():
    return {
        name: {
            "description": tool["description"],
            "parameters": tool["parameters"],
            "permission": tool["permission"],
            "risk_level": tool["risk_level"],
        }
        for name, tool in TOOLS.items()
    }