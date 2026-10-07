# Agent Workflow

## Overview

The AI Integration Incident Agent investigates integration incidents using a combination of retrieved knowledge, read-only diagnostic tools and controlled remediation actions.

The agent is designed to investigate dynamically rather than follow a fixed sequence of diagnostic steps.

## Investigation Flow

1. Receive an incident.
2. Retrieve the incident details.
3. Assess the incident severity and affected system.
4. Determine what additional information is required.
5. Search relevant integration knowledge.
6. Call appropriate diagnostic tools.
7. Analyse the returned evidence.
8. Determine whether sufficient evidence exists.
9. If additional evidence is required, perform further investigation.
10. Determine the most likely root cause.
11. Recommend a remediation.
12. Determine whether the remediation requires a change to a system.
13. If the action is read-only or informational, provide the result.
14. If the action modifies a system, require explicit human approval.
15. Execute an approved remediation through a controlled tool.
16. Record the investigation, decision and action in an audit trail.

## Example — HTTP 429 Incident

An incident reports that the Customer Sync API is returning HTTP 429 responses.

The agent may:

1. Retrieve the incident.
2. Search the knowledge base for HTTP 429 and rate-limiting guidance.
3. Retrieve API metrics.
4. Search integration logs.
5. Check recent deployments or configuration changes.
6. Correlate the evidence.
7. Determine the most likely cause.
8. Recommend an appropriate remediation.

The exact sequence of tool calls may vary depending on the evidence returned by each tool.

## Human-in-the-Loop

The agent can investigate incidents autonomously using approved read-only tools.

Actions that modify systems require human approval before execution.

Examples include:

* restarting an integration
* changing configuration
* modifying credentials
* changing integration behaviour

The approval decision is recorded as part of the audit trail.

## Agent Boundary

The agent is responsible for:

* investigation
* evidence gathering
* analysis
* diagnosis
* recommendation

The agent is not granted unrestricted system access.

Tools provide the controlled interface between the AI agent and external systems.
