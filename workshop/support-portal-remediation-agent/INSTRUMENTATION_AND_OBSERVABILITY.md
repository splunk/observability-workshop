# Instrumentation and Observability Plan

## Goal

Instrument the app like a real production system, not a toy demo.

The observability design should make it easy to explain:

- what the user experienced
- which business transaction degraded
- which service path is responsible
- why default host, APM, and RUM signals support the remediation decision
- how the remediation agent was monitored

## Telemetry Layers

### 1. Frontend

Use:

- Splunk RUM for Browser
- Digital Experience Analytics
- Session Replay if available in the target tenant

Instrument:

- initial page load
- route transitions
- fetch/XHR calls
- JavaScript errors
- custom actions:
  - `claims.query_submitted`
  - `claims.response_rendered`
  - `case.lookup_requested`
  - `article.search_requested`
  - `claims.retry_clicked`

Business attributes to attach where possible:

- `app.business_transaction`
- `app.customer_journey`
- `app.feature_area`
- `scenario.id`
- `session.segment`

### 2. Backend application services

Use:

- Splunk Distribution of OpenTelemetry for Node.js
- auto-instrumentation for HTTP and framework layers
- manual spans for business steps

Service naming:

- `claims-portal-api`
- `claims-assistant`
- `claims-policy-service`
- `claims-knowledge`
- `remediation-orchestrator`
- `remediation-agent`
- `scenario-controller`

Resource attributes:

- `service.name`
- `service.namespace=ibobs2002`
- `deployment.environment=demo`
- `service.version`

Manual spans to add:

- `claim.request.validate`
- `claim.request.route`
- `assistant.compose_response`
- `knowledge.fetch_context`
- `case.lookup`
- `search.query`
- `remediation.policy_evaluate`
- `remediation.api_enrich`
- `remediation.agent_evaluate`
- `remediation.execute_action`
- `remediation.verify_recovery`

### 3. Remediation agent

Use:

- OpenTelemetry Python
- Galileo instrumentation for agent, tool, and OpenAI model-call monitoring
- OpenAI Chat Completions API via ChatGPT

Capture:

- model name
- tool selection
- tool-call latency
- prompt/response timing
- token usage
- confidence band
- reasoning summary
- final outcome

## Business Attributes

Standardize these low-cardinality attributes for business transactions, dashboards, detector filters, and trace search:

- `app.business_transaction`
- `app.workflow`
- `app.customer_journey`
- `app.feature_area`
- `incident.id`
- `scenario.id`
- `action.id`
- `action.type`
- `action.policy_mode`
- `deployment.environment`
- `service.instance.id`

Low-cardinality rules:

- never put free-form customer input into indexed attributes
- never put case ids or search strings into indexed dimensions
- use enums or small value sets for all dashboard/detector dimensions
- do not create custom application metrics for the incident; use default RUM, APM, and host metrics

## Business Transactions

### Required transactions

- `AI Claim Status`
- `Policy Coverage Lookup`
- `Claims FAQ Search`

### Why multiple transactions

This makes the app look like a real system and lets the demo show:

- one degraded transaction
- two healthy transactions
- a contained affected workflow

### Rule strategy

Preferred rule strategy:

- service rules or global-tag rules using `app.business_transaction`
- endpoint grouping before transaction rules if needed

Recommended naming:

- human-readable names in Splunk UI
- machine-stable lowercase values in telemetry

Example mapping:

- telemetry value: `claim_status_response`
- Splunk display: `AI Claim Status`

## Default Signals

Build the demo from signals Splunk users already expect to find after instrumenting the app and collector.

Primary signals:

- RUM page load, route, and fetch timing
- APM service request count, errors, and duration
- APM traces for the AI claim status path
- host metrics receiver filesystem utilization for the claims knowledge cache volume
- remediation agent spans, tool-call spans, and model-call spans

Use these for:

- transaction latency charts
- transaction error charts
- claims knowledge latency charts
- claims knowledge filesystem pressure detectors
- remediation validation status

## Affected Workflow Modeling

The orchestrator should avoid inventing a separate impact score. The live story should stay grounded in the same evidence the presenter can show in Splunk.

Summarize:

- affected business transaction
- suspect service
- host or container volume under pressure
- confidence band
- proposed action and validation plan

Do not emit custom impact metrics for this. The operator console can display the affected workflow in plain language from the incident evidence.

## Service Map Expectations

The service map should show two logical clusters.

Customer-serving path:

- `claims-portal-api`
- `claims-assistant`
- `claims-policy-service`
- `claims-knowledge`

Remediation path:

- `remediation-orchestrator`
- `remediation-agent`

Action target:

- claims knowledge cache volume cleanup through the remediation agent tool

## Dashboards

Create dashboards in the new dashboard experience where possible.

### 1. Executive Story Dashboard

Charts:

- affected sessions
- DEA frustration signal count
- business transaction status table
- affected workflow
- proposed action
- validation status

### 2. Digital Experience Dashboard

Charts:

- page load or route latency
- fetch latency
- JavaScript error rate
- frustration signals
- top affected sessions
- replay link table or supporting note

### 3. Business Transactions Dashboard

Charts:

- latency by business transaction
- error rate by business transaction
- throughput by business transaction
- transaction health scorecard
- affected versus healthy transaction comparison

### 4. Service Health Dashboard

Charts:

- service RED metrics
- service map
- top slow spans
- suspect dependency latency
- claims knowledge filesystem utilization

### 5. Remediation Dashboard

Charts:

- incidents opened
- proposals created
- approval-required count
- time to proposal
- time to execution
- time to validation
- remediation success rate

### 6. Galileo Agent Monitoring View

Charts:

- model latency
- token usage
- tool-call latency
- tool-call failures
- action recommendation distribution
- confidence band distribution

## Detectors

Primary detectors:

- `AI Claim Status` p95 latency high
- `AI Claim Status` error rate high
- `claims-knowledge` latency high
- remediation validation failed
- remediation duration too long

Secondary detectors:

- DEA frustration spike
- frontend JS error spike
- repeated proposal rejection

Primary webhook trigger:

- business transaction latency or error detector on `AI Claim Status`

## Views To Use Live

- RUM session details
- Session Replay
- business transaction view
- service map
- service view
- trace analyzer
- remediation dashboard
- Galileo project and remediation-agent log stream

## Automation-First Setup

Use code for all supported Splunk objects.

Preferred automation:

- dashboards: Terraform `signalfx` provider or direct API-backed tooling
- dashboard groups: Terraform `signalfx` provider
- detectors: Terraform `signalfx` provider or detector API
- webhook integration and detector recipient configuration: automate if supported in the chosen approach

Known caution:

- current public docs clearly document UI flows for business transaction rules and endpoint grouping
- I did not find a similarly clear public API/Terraform path for those APM rule objects
- treat them as a likely manual or pre-provisioning exception unless tenant-specific validation proves otherwise
