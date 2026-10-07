# AI Integration Incident Agent

## Purpose

The AI Integration Incident Agent is a portfolio project demonstrating how an AI agent can assist with the diagnosis and resolution of integration incidents.

The project uses fictional systems and data and is designed to demonstrate:

* REST API integration
* AI agent orchestration
* Retrieval-Augmented Generation (RAG)
* Tool calling
* Incident diagnosis
* Human-in-the-loop controls
* AI governance
* Auditability

## Fictional Environment

The fictional organisation, AcmeCare, operates a Salesforce-based customer platform integrated with external billing, scheduling and notification systems.

The AI agent receives integration incidents and investigates them using approved tools and knowledge sources.

## Initial Incident Scenarios

### INC-1001 — API Rate Limiting

Customer Sync API is returning HTTP 429 responses.

Severity: High

### INC-1002 — Authentication Failure

Billing API is returning HTTP 401 responses.

Severity: High

### INC-1003 — Data Transformation Failure

Appointment Sync is returning HTTP 400 responses due to a suspected data mapping issue.

Severity: Medium

## Agent Responsibilities

The agent should be able to:

1. Receive an incident.
2. Understand the reported problem.
3. Retrieve relevant integration knowledge.
4. Investigate the incident using approved tools.
5. Determine the likely cause.
6. Recommend an appropriate remediation.
7. Request human approval where required.
8. Record the investigation and actions taken.

## Agent Boundaries

The agent must not have unrestricted access to systems.

Actions that could modify production data, credentials, integration configuration or business processes require appropriate human approval.

All data used by the project is fictional.
