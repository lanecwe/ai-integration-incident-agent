import inspect
from src.incident_agent.llm_factory import create_llm
from src.incident_agent.tool_registry import TOOLS
from src.incident_agent.diagnosis import diagnose_incident


MAX_STEPS = 10


def investigate_incident(incident_id: str) -> dict:
    """
    Investigate an incident using an agentic tool-calling loop.
    """

    llm = create_llm()
    print(f"\nLLM client: {type(llm).__name__}")

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

        
        tool_descriptions = []

        for name, definition in TOOLS.items():
            function = definition["function"]
            signature = inspect.signature(function)

            arguments = ", ".join(signature.parameters.keys())

            tool_descriptions.append(
                f"- {name} (arguments: {arguments})"
            )

        prompt += (
            "\nAvailable tools and their exact signatures:\n"
            + "\n".join(tool_descriptions)
            + "\nUse only the listed arguments for each tool.\n"
        )

        # Display the prompt sent to the LLM.
        print(f"\n--- PROMPT (Step {step + 1}) ---")
        print(prompt)

        # Ask the LLM what to do next.
        tool_request = llm.generate(prompt)

        # Display the parsed response returned by the LLM.
        print("\n--- LLM OUTPUT ---")
        print(tool_request)

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
        if tool_name in tools_used:
            raise ValueError(
                f"Tool '{tool_name}' has already been executed. "
                f"Choose a different tool or finish the investigation."
            )

        # Execute the tool.
        tool = TOOLS[tool_name]
        tool_function = tool["function"]

        # Validate arguments against the actual Python function signature.
        signature = inspect.signature(tool_function)
        allowed_arguments = set(signature.parameters.keys())
        provided_arguments = set(arguments.keys())

        unexpected_arguments = provided_arguments - allowed_arguments
        missing_arguments = {
            name
            for name, parameter in signature.parameters.items()
            if parameter.default is inspect.Parameter.empty
            and name not in provided_arguments
        }

        if unexpected_arguments:
            raise ValueError(
                f"Invalid arguments for {tool_name}: "
                f"unexpected {sorted(unexpected_arguments)}. "
                f"Allowed arguments: {sorted(allowed_arguments)}"
            )

        if missing_arguments:
            raise ValueError(
                f"Invalid arguments for {tool_name}: "
                f"missing {sorted(missing_arguments)}"
            )

        result = tool_function(**arguments)

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