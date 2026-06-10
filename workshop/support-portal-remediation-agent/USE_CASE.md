# IBOBS-2002 Use Case

## Title

Automated Resolution, Accelerated Insights: AI Remediation Agents in Splunk Observability Cloud

## Use Case Summary

A company launches an AI-powered claims portal to improve customer experience, reduce pressure on human agents, and scale digital service. The portal becomes a high-value customer touchpoint, which means performance or reliability issues immediately affect customer trust.

During a peak usage period, the cache volume used by the claims knowledge service fills up. The AI claim status experience slows down and can partially fail because retrieval work now waits on a pressured filesystem. Splunk RUM and Digital Experience Analytics can show the customer impact, while APM service health and host filesystem metrics provide the reliable proof path for the lab. A separate remediation orchestrator receives the detector alert, accepts a human-in-the-loop summary from Splunk AI Assistant or Troubleshooting Agent, enriches missing structured fields through targeted Splunk API lookups, and then passes a bounded evidence package to the remediation agent. The team applies policy, approves the action, validates recovery, and preserves a clear audit trail.

This use case demonstrates how customers can move from observability as explanation to observability-informed action, without giving up trust, governance, or control.

## Business Problem

Customer-facing AI services create a new operational challenge:

- customers expect fast, accurate, always-on digital experiences
- AI workflows depend on multiple services, tools, models, and data sources
- when these systems degrade, trust drops quickly
- browser friction and abandoned sessions appear before many teams understand the backend cause
- teams often detect the problem, but still lose time deciding what action is safe

The issue is no longer only incident detection. The issue is how to convert evidence into a trustworthy remediation decision fast enough to protect the customer experience.

## Customer Scenario

A customer opens an AI claims portal to resolve a product issue. The request enters a backend workflow that depends on a knowledge or retrieval service. A full cache volume in that dependency introduces latency and intermittent failures.

The portal supports multiple business transactions, for example:

- `AI Claim Status`
- `Policy Coverage Lookup`
- `Claims FAQ Search`

In this use case, only `AI Claim Status` is materially impacted. The other transactions remain healthy, which helps demonstrate how Splunk business transactions, endpoint grouping, and service views can isolate the affected workflow without making the whole application look broken.

From the customer point of view:

- answers take too long
- some requests fail
- the browser session shows frustration signals
- confidence in the digital support experience falls quickly

From the operations point of view:

- RUM and Digital Experience Analytics show the failing customer journey when browser data is available
- Session Replay can show what the user experienced when enabled in the tenant
- APM shows rising latency and errors on the affected service path
- Infrastructure Monitoring shows filesystem utilization on the knowledge service host or container volume
- business transaction views show one affected workflow while others remain healthy
- the affected path is visible, but action still requires judgment
- the team needs to know not only what is broken, but what should happen next

## Desired Outcome

The desired outcome is not full autonomous remediation.

The desired outcome is:

- rapid detection of customer impact
- visibility into the degraded browser experience
- fast correlation of evidence across the affected system
- a bounded remediation recommendation
- policy-based approval for the action
- validation that the action improved the customer experience
- a complete audit trail of what was proposed, approved, executed, and verified

## Solution Pattern

This use case follows a two-layer model.

### 1. Observability and Evidence Layer

Splunk Observability Cloud:

- detects a degraded user journey through RUM and DEA when configured
- optionally shows the customer journey through Session Replay
- detects service degradation
- maps the issue to a business transaction and backend service path
- uses endpoint and operation grouping to keep URL-level views readable
- surfaces latency and error patterns
- correlates telemetry across the affected flow
- helps identify the likely cause and affected workflow
- provides the evidence needed to support a remediation decision

### 2. Action Layer

A separate remediation orchestrator and remediation agent:

- open a local incident or receive the optional detector webhook from Splunk
- gather structured evidence from Splunk Observability Cloud MCP
- accept optional human-readable investigation notes from the presenter
- enrich missing structured fields from Splunk APIs when needed
- receive the incident context
- evaluate a small set of approved actions
- propose a bounded remediation
- wait for policy-driven approval when required
- execute the approved action
- validate whether the system recovered

This use case does not assume that Splunk AI Assistant directly invokes the remediation agent. Splunk provides the observability, detection, and investigation context. The action path is handled by a separate remediation flow, with a hybrid handoff that combines Splunk MCP evidence, optional human-readable AI Assistant output, and targeted Splunk API enrichment.

## Example Remediation Path

Primary example:

- the system detects degradation in the AI claim status workflow
- RUM and DEA can show a frustrating browser journey
- APM and Infrastructure provide the required service and filesystem proof
- the operator opens a local incident in the orchestrator
- the orchestrator gathers Splunk Observability Cloud evidence through MCP
- the orchestrator fills missing structured fields from Splunk APIs
- evidence indicates cache filesystem pressure on the knowledge service dependency
- the remediation agent proposes `clean_claims_knowledge_cache`
- the action is marked `approval_required`
- the operator approves the action
- the cache pressure is cleared through the approved remediation tool
- latency and error rates improve
- the action and validation are recorded

This path is easy for customers to understand because it is bounded, visible in standard observability views, and low risk compared with broader automated changes.

## Why This Resonates With Customers

This use case reflects what many customers are facing now:

- AI is moving into the production path
- digital experience failures are immediately visible to users
- browser experience, backend performance, and AI behavior must be understood together
- teams want faster action, but not black-box automation
- governance and trust now shape how far automation can go

The value is not “AI fixed the issue automatically.”

The value is:

- faster movement from insight to action
- a visible human trust checkpoint before automation continues
- fewer blind handoffs during incidents
- better protection of customer trust
- stronger confidence in operational automation

## Key Message

The message for customers is simple:

Observability is no longer just about understanding what happened in the backend. In AI-driven customer environments, it must start with the digital experience and extend all the way to safe, explainable, and validated action.
