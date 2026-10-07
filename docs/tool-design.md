# Tool Design

The AI Integration Incident Agent interacts with external systems through explicitly defined tools.

The agent does not receive unrestricted access to systems or databases.

## Read-Only Tools

### get_incident

Retrieves the details of an incident.

**Input**

* incident_id

**Output**

* incident ID
* severity
* affected system
* error code
* error message
* timestamp
* incident status

**Risk:** Low

**Human approval:** Not required

---

### search_logs

Searches fictional integration logs for an incident, system or error.

**Input**

* system
* time range
* optional error code

**Output**

* matching log entries
* timestamps
* error messages
* request identifiers

**Risk:** Low

**Human approval:** Not required

---

### get_api_metrics

Retrieves fictional API health and traffic metrics.

**Input**

* system
* time range

**Output**

* request volume
* error rate
* response time
* HTTP status distribution

**Risk:** Low

**Human approval:** Not required

---

### get_recent_changes

Retrieves recent fictional deployments or configuration changes.

**Input**

* system
* time range

**Output**

* deployment ID
* timestamp
* change description
* deployment status

**Risk:** Low

**Human approval:** Not required

---

### search_knowledge

Searches integration runbooks and technical documentation.

**Input**

* natural language query

**Output**

* relevant documentation passages
* source document
* relevance score

**Risk:** Low

**Human approval:** Not required

---

## Write Tools

Write tools can modify systems and therefore require additional controls.

### restart_integration

Restarts a fictional integration process.

**Risk:** Medium

**Human approval:** Required

---

### update_configuration

Changes a fictional integration configuration.

**Risk:** High

**Human approval:** Required

---

## Security Principle

The agent should operate using the minimum permissions required to perform its task.

Read-only investigation should normally be performed autonomously.

Actions that modify systems, configuration, credentials or business data require explicit human approval.
