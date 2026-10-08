from src.incident_agent.llm import MockLLM
from src.incident_agent.tool_registry import TOOLS
from src.incident_agent.diagnosis import diagnose_incident


MAX_STEPS = 10


def investigate_incident(incident_id: str) -> dict:
    """
    Investigate an incident using an agentic tool-calling loop.
    """

    llm = MockLLM()

    tools_used = []
    evidence = {}

    system = None

    for step in range(MAX_STEPS):

        if not tools_used:

            prompt = f"""
            Investigate integration incident {incident_id}.

            No tools have been used yet.
            Determine what information you need before diagnosing
            the incident.
            """

        else:

            last_tool = tools_used[-1]

            prompt = f"""
            We are investigating incident {incident_id}.

            Affected system: {system}

            Last tool executed: {last_tool}

            Tool result:
            {evidence[last_tool]}

            Review the evidence and determine what should be
            investigated next.

            You may request another tool or finish the investigation.
            """

        # Ask the LLM what to do next.
        tool_request = llm.generate(prompt)

        tool_name = tool_request["action"]
        arguments = tool_request["arguments"]

        # The LLM can decide the investigation is complete.
        if tool_name == "finish":

            diagnosis = diagnose_incident(evidence)

            return {
                "incident_id": incident_id,
                "evidence": evidence,
                "diagnosis": diagnosis,
                "tools_used": tools_used,
                "steps": step + 1,
                "status": "investigation_complete",
            }

        # Validate the requested tool.
        if tool_name not in TOOLS:
            raise ValueError(
                f"Unknown tool requested: {tool_name}"
            )

        # Execute the tool.
        tool = TOOLS[tool_name]

        result = tool["function"](**arguments)

        tools_used.append(tool_name)

        evidence[tool_name] = result

        # Capture the affected system after retrieving the incident.
        if tool_name == "get_incident":
            system = result["system"]

    return {
        "incident_id": incident_id,
        "evidence": evidence,
        "tools_used": tools_used,
        "steps": MAX_STEPS,
        "status": "maximum_steps_reached",
    }