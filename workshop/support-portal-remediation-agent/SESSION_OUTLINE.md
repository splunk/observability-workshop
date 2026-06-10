# IBOBS-2002 Session Plan

## Session Metadata

- Session ID: IBOBS-2002
- Session Title: Automated Resolution, Accelerated Insights: AI Remediation Agents in Splunk Observability Cloud
- Session Type: Interactive Breakout
- Speaker: Marcio Kugler Rodrigues
- Submitter / Co-Presenter: Leila Reyhani

## Positioning

Keep the approved title, but change the interpretation of it.

Do not make this session mean:

- AI adds a summary to observability
- AI speeds up triage in a generic way
- AI is a chatbot layer over dashboards

Make it mean:

"How do you trust, observe, and govern AI remediation agents inside a modern observability practice?"

That keeps the title intact while making the content much sharper and more current.

## Why This Version Works

Recent Splunk direction gives you a more differentiated story than a standard Observability Cloud pitch:

- Splunk RUM
- Digital Experience Analytics
- Session Replay
- Business Transactions and endpoint grouping
- AI Troubleshooting Agent
- Splunk AI Assistant
- Remediation Plan
- Galileo agent monitoring
- new dashboard experience and log-based charting

So the breakout should focus on three ideas:

1. observability is no longer just about finding issues in the backend
2. if AI agents are going to participate in remediation, those agents themselves must be observable, governed, and auditable
3. human-in-the-loop AI handoff is a credible bridge between AI investigation and automated action
4. multiple business transactions and endpoint grouping make the incident feel like a real production system, not a toy demo

This makes the session feel contemporary instead of recycled.

## Core Thesis

The strongest interpretation of the title is:

"Accelerated insights are only useful if they begin with real customer experience, then lead to bounded, explainable action. Automated resolution only works when the remediation agent is monitored as carefully as the system it is trying to fix."

## Session Arc

Use a single, staged incident and run the breakout like an incident room, not a product demo.

Recommended flow for 60 minutes:

### 1. Opening Incident (5 minutes)

Marcio opens with the operational problem:

"Your customers feel the problem before your operators fully understand it. The browser slows down, the session deteriorates, and trust drops before the war room agrees on what changed."

Leila then reframes the audience expectation:

"Now the question is not just whether AI can investigate faster. It is whether you can observe the digital experience, understand the evidence, and trust an AI-driven remediation flow in production."

### 2. Why Traditional Observability Is Not Enough (7 minutes)

Marcio covers the familiar problem space:

- too many signals
- too many handoffs
- high MTTR despite rich telemetry
- dashboards that explain but do not act

Leila introduces the shift:

- AI troubleshooting is one step
- AI remediation is the next step
- agentic systems create a second observability problem: observing the agent

### 3. The Two-Agent Model (8 minutes)

This is the anchor concept for the session.

Agent 1:

- Splunk AI Troubleshooting Agent
- Splunk AI Assistant
- correlates telemetry and change context
- starts from user impact visible in RUM and Digital Experience Analytics when available, then verified through APM and Infrastructure
- explains likely cause and affected workflow
- produces a remediation-oriented evidence package

Agent 2:

- purpose-built remediation agent used in the demo
- has a bounded toolset
- can recommend or execute only approved actions
- is implemented in Python so Galileo can instrument the agent workflow and OpenAI calls
- is itself monitored through Galileo and standard Splunk observability telemetry

This is the point where your talk stops being generic.

### 4. Live Interactive Incident (20 minutes)

Use one deterministic scenario with one main remediation path.

Recommended scenario:

- a critical business flow degrades because the claims knowledge cache volume fills up
- browser users experience elevated latency, hesitation, and failed interactions
- Splunk RUM and Digital Experience Analytics can expose end-user impact first
- business transaction health and service map show the backend path behind the failure
- only one primary business transaction degrades while others remain healthy
- the AI Assistant or Troubleshooting Agent pulls together the evidence
- the detector webhook opens the incident in the orchestrator
- the presenter copies the AI Assistant summary into the orchestrator as a human-in-the-loop step
- the orchestrator enriches missing fields with targeted Splunk API lookups
- the remediation agent proposes a bounded action
- the audience helps decide whether the system should act automatically, ask for approval, or only recommend
- the action is executed
- the team verifies recovery and reviews the audit trail

Marcio role:

- incident commander
- narrates customer impact, telemetry, and operational pressure

Leila role:

- platform / AI operations lead
- narrates agent behavior, policy controls, and trust boundaries

This division will make the interaction feel deliberate rather than two people alternating slides.

### 5. Guardrails and Governance (10 minutes)

Leila should lead this section.

Make this a strength of the talk, not a disclaimer slide.

Cover:

- confidence thresholds
- approval gates
- low-risk vs high-risk actions
- environment scoping
- rollback protection
- auditability
- human override
- validation after action

Strong line:

"The goal is not autonomous everything. The goal is autonomous action where risk is understood, bounded, and observable."

### 6. Close With a Practical Adoption Model (5 minutes)

Marcio closes with the maturity journey:

- Level 1: AI summarizes incidents
- Level 2: AI recommends next actions
- Level 3: AI executes low-risk remediations with approval
- Level 4: AI auto-resolves narrow, repeatable failure modes

End with:

"If your observability platform can describe the incident but cannot help govern the action, your AI remediation story is incomplete."

## Interactive Breakout Design

This needs to feel like an interactive breakout, not a standard breakout with a few questions.

Use three audience interaction moments:

### Interaction 1: What Would You Do?

After the incident appears, ask the audience to choose the first action:

- rollback
- scale
- restart

Then compare their instinct to what the remediation agent proposes.

### Interaction 2: Should the Agent Be Allowed to Execute?

Show the same action under three policy modes:

- recommend only
- approval required
- auto-execute

Ask the room where they would place this incident.

### Interaction 3: What Evidence Do You Need to Trust the Agent?

Before action executes, ask:

"What would you need to see before letting an agent touch production?"

Then reveal the evidence package:

- digital experience impact
- replay of the failing session
- AI Assistant summary
- telemetry correlation
- affected workflow
- host filesystem metric evidence
- confidence band
- validation plan

## Demo App Plan

Build a purpose-built app specifically for this session.

Do not reuse a generic workshop app unless it already supports deterministic incidents and telemetry-rich remediation flows.

### App Components

- SPA web frontend for the user journey
- backend API
- one critical dependency service
- cache-pressure scenario control
- remediation orchestrator service
- remediation agent service
- scenario control service for failure injection and reset
- operator console for presenters

### Recommended Technical Stack

Keep the stack simple and fast to build.

- frontend: React with Vite
- services: Node.js with TypeScript and Fastify or Express
- remediation agent: Python service
- storage: Redis only if needed for state and scenario flags
- telemetry: Splunk Distribution of OpenTelemetry for Node.js and Python plus Splunk RUM for Browser
- deployment: Docker Compose locally, optional Kubernetes only if you need a stronger container story
- LLM provider: ChatGPT API for the remediation agent

Why this stack:

- easy to build quickly
- easy to instrument with Splunk-supported telemetry paths
- simple enough to reset live
- deterministic enough for demos
- aligns the frontend with Splunk RUM and DEA
- aligns the remediation agent with Galileo instrumentation
- uses a reliable hosted model for structured action selection

### Recommended App Story

Build a small "AI Support Assistant" product rather than a plain e-commerce clone.

Why:

- it makes the AI angle feel native
- it gives you a reason to show both customer-facing impact and agent operations
- it avoids feeling like a recycled checkout demo unless you explicitly want a commerce theme

Suggested user flow:

1. user opens a claims portal
2. Splunk RUM starts the browser session and DEA tracks the experience
3. user chooses one of several actions:
   - ask claim status question
   - check policy coverage
   - search claims FAQ
4. frontend calls the backend
5. backend routes to the appropriate transaction path
6. failure scenario introduces latency or errors only in the support-response dependency path
7. customer experience degrades in a visible way for one workflow
8. DEA can show the frustration path when RUM data is available before the backend story is fully explained

If you prefer a more familiar business transaction, use a purchase or checkout flow. The architecture below still applies.

### Concrete Services To Build

Build six services max.

#### 1. `frontend`

Purpose:

- render the user journey
- expose a visible "service degraded" state during the incident
- optionally host the internal operator control page in a hidden route

Code responsibilities:

- one main user flow
- one metrics overlay for demo timing if desired
- browser telemetry with OpenTelemetry

#### 2. `api-gateway`

Purpose:

- main backend for the demo
- entrypoint for user requests
- fan out to downstream services

Endpoints:

- `POST /api/request`
- `GET /api/health`
- `GET /api/config`

Code responsibilities:

- correlation ids
- trace propagation
- span attributes and error handling
- request validation

#### 3. `assistant-service`

Purpose:

- simulate the app's AI-driven business logic
- call the dependency that will fail

Endpoints:

- `POST /assistant/respond`
- `GET /assistant/health`

Code responsibilities:

- call dependency service
- emit spans that look like AI workflow steps
- attach semantic attributes for prompt or task class, token estimates, dependency latency, and final status

#### 4. `knowledge-service`

Purpose:

- act as the latency-sensitive dependency
- be the source of the controlled failure

Endpoints:

- `POST /knowledge/query`
- `GET /knowledge/health`

Failure modes:

- add fixed latency
- raise error rate
- return malformed responses

This should be the main service impacted by the live scenario.

#### 5. `remediation-orchestrator`

Purpose:

- receive incident context shaped by Splunk evidence
- receive detector webhook notifications from Splunk
- accept pasted AI Assistant or Troubleshooting Agent summaries from the operator console
- optionally enrich the incident with additional Splunk API lookups
- package the remediation decision request
- call the remediation agent
- store the proposed action and approval state

Endpoints:

- `POST /webhooks/splunk/detector`
- `POST /remediation/context`
- `POST /remediation/propose`
- `POST /remediation/approve/:actionId`
- `GET /remediation/actions/:actionId`
- `GET /remediation/health`

#### 6. `remediation-agent`

Purpose:

- receive a bounded remediation request
- evaluate a small policy
- propose one or more safe actions
- optionally execute the approved action

Endpoints:

- `POST /agent/evaluate`
- `POST /agent/execute/:actionId`
- `POST /agent/verify/:actionId`
- `GET /agent/health`

Internal modules:

- evidence collector
- policy evaluator
- action planner
- tool executor
- verification runner
- audit recorder

#### 7. `scenario-controller`

Purpose:

- trigger and reset the incident deterministically
- provide a single presenter control surface

Endpoints:

- `POST /scenario/activate/dependency-latency`
- `POST /scenario/activate/dependency-errors`
- `POST /scenario/reset`
- `GET /scenario/state`

Code responsibilities:

- toggle fault flags
- reset service state
- emit custom events for scenario start and reset

#### 8. `operator-console`

Purpose:

- presenter-facing control surface
- activate incident
- paste AI Assistant summary and evidence text
- review proposed action
- approve action
- reset environment

Views:

- scenario control
- evidence intake
- evidence summary
- action approval
- recovery status

### Required Demo Behaviors

- clean baseline state
- one button to trigger the incident
- predictable latency and error degradation
- telemetry visible in Splunk within a short window
- one bounded remediation action for the happy path
- one reset path to restore baseline between rehearsals

### Required Toolset for the Remediation Agent

- clean service cache
- restart service

Only one of these should be used in the main live flow.

Recommended primary live action:

- `clean_claims_knowledge_cache`

Why:

- it is visually understandable
- it is lower risk than restart or scale
- it maps to a default host filesystem utilization signal in Splunk
- it fits a bounded-remediation story well

### Policy Engine Rules

Keep the policy simple and visible on screen.

Inputs:

- confidence band
- environment
- action type
- signal evidence present

Outputs:

- `recommend_only`
- `approval_required`
- `auto_execute`

Default rules:

- production plus a customer-facing remediation action => `approval_required`
- low confidence => `recommend_only`
- non-production and high confidence for a known-safe action => `auto_execute`

### Evidence Intake Model

Use two evidence-ingestion modes.

Primary demo mode:

- Splunk detector webhook opens the incident in the orchestrator
- presenter copies the Splunk AI Assistant or Troubleshooting Agent summary into the operator console
- orchestrator parses the pasted summary and combines it with detector context, targeted Splunk API enrichment, and known scenario metadata

Secondary or future mode:

- orchestrator calls Splunk APIs to enrich detector context automatically

Why the primary mode is recommended:

- easier to demonstrate visually
- easier to explain to customers
- shows a realistic human-in-the-loop trust boundary
- avoids overcommitting to API coverage before the event

Hybrid recommendation:

- treat the pasted AI Assistant summary as the narrative context
- treat Splunk API enrichment as the structured context layer
- use both before creating the final `EvidenceBundle`

### Additional Data To Request From Splunk APIs

If you implement enrichment, keep it narrow and decision-oriented.

Recommended data:

- detector name, condition, severity, dimensions, trigger time
- affected business transaction
- affected services and suspect service path
- current latency and error rate for the business transaction
- representative trace or span context for the failing path
- service map neighborhood for affected-path evidence
- RUM and DEA summary metrics for impacted sessions
- session replay identifier or link if available

Use orchestrator-owned metadata for:

- known scenario state
- expected action target
- known-safe remediation actions

Do not depend on the orchestrator pulling every part of the story from Splunk APIs. The AI Assistant summary should fill the human-readable gap, and the APIs should fill the structured-data gap.

### Human-in-the-Loop Handoff

This should be part of the official demo story.

Flow:

1. Splunk detector fires and opens the incident in the orchestrator
2. presenters investigate in Splunk
3. Splunk AI Assistant summarizes likely cause and action context
4. presenter copies that summary into the operator console
5. orchestrator queries Splunk APIs for any missing structured evidence needed for policy and action selection
6. orchestrator converts the pasted summary plus alert metadata and API-enriched fields into an `EvidenceBundle`
7. orchestrator decides whether the incident is eligible for automated remediation
8. if eligible, orchestrator calls the remediation agent

This creates a credible bridge from AI investigation to bounded automated action.

### LLM Usage Model

Keep the LLM role narrow.

ChatGPT is used in the remediation agent to:

- interpret the normalized `EvidenceBundle`
- rank the allowed actions
- produce a short reasoning summary
- return structured JSON for the proposed action

The orchestrator remains deterministic and policy-driven.

ChatGPT should not:

- invent new tools
- bypass policy
- decide whether an incident class is automation-eligible without orchestrator checks

### Verification Logic

The remediation agent should not stop at action execution.

After action:

- poll `GET /api/health`
- verify latency drops below threshold
- verify error rate drops below threshold
- confirm downstream health checks
- emit `validation_passed` or `validation_failed`

This is critical because the validation step is what makes the remediation story credible.

### Telemetry Requirements

Instrument customer-facing and backend paths with OpenTelemetry, and instrument the remediation agent with Galileo metadata.

Frontend telemetry should use Splunk RUM with Digital Experience Analytics enabled. If Session Replay is available in the demo environment, use it to show the degraded user journey before pivoting into backend analysis.

Track:

- browser navigation and fetch performance
- page load and route transitions
- JavaScript errors
- DEA frustration signals and key user interactions
- traces across the business flow
- service latency and error metrics
- host filesystem utilization metrics
- agent task execution spans
- tool calls
- tool latency
- token usage
- action status
- post-remediation verification

Feature-specific highlights:

- RUM and DEA for customer impact
- optional Session Replay for one concrete failing user journey if available
- multiple business transactions with one affected and two healthy
- endpoint grouping and operation grouping for clean URL views
- service map for app and remediation topology
- AI Troubleshooting Agent for evidence synthesis
- Galileo for remediation-agent visibility
- new dashboard experience for a unified operator view

Add these attributes wherever possible:

- `incident.id`
- `scenario.id`
- `action.id`
- `action.type`
- `action.policy_mode`
- `agent.confidence_band`
- `agent.reasoning_summary`
- `agent.tool_name`
- `agent.tool_result`
- `validation.status`

### Minimal Event Contract

Define a small event shape so dashboards and detectors stay stable.

Custom events:

- `scenario_activated`
- `incident_opened`
- `action_proposed`
- `action_approved`
- `action_executed`
- `validation_passed`
- `validation_failed`

Suggested fields:

- `timestamp`
- `incident_id`
- `scenario_id`
- `service`
- `severity`
- `action_id`
- `action_type`
- `policy_mode`
- `confidence_band`
- `result`

### Suggested Repository Layout

Use one monorepo.

```text
ciscolive26/
  apps/
    frontend/
    api-gateway/
    assistant-service/
    knowledge-service/
    remediation-orchestrator/
    remediation-agent/
    scenario-controller/
    operator-console/
  packages/
    telemetry/
    shared-types/
    policy-engine/
    evidence-parser/
    demo-scenarios/
  infra/
    docker/
    otel-collector/
  docs/
    demo-runbook/
    deck-assets/
```

### Shared Types To Define

Create a small shared type library.

Core types:

- `Incident`
- `BrowserExperienceSummary`
- `ScenarioState`
- `EvidenceBundle`
- `AssistantEvidenceInput`
- `ProposedAction`
- `PolicyDecision`
- `VerificationResult`
- `AgentExecutionTrace`

Most important shape:

```ts
type ProposedAction = {
  actionId: string;
  incidentId: string;
  type: "clean_claims_knowledge_cache" | "restart_service";
  target: string;
  confidenceBand: "low" | "medium" | "high";
  policyMode: "recommend_only" | "approval_required" | "auto_execute";
  reasoningSummary: string;
  validationPlan: string[];
  status: "proposed" | "approved" | "executed" | "validated" | "rejected";
};
```

Supporting shape:

```ts
type AssistantEvidenceInput = {
  source: "splunk_ai_assistant" | "splunk_troubleshooting_agent";
  rawText: string;
  pastedBy: string;
  pastedAt: string;
  detectorId?: string;
  incidentId?: string;
};
```

### Code Workstreams

Build in this order:

1. baseline SPA and healthy user flow
2. Splunk RUM plus DEA instrumentation
3. fault injection in `knowledge-service`
4. backend instrumentation and business transaction shaping
5. Splunk detector webhook to orchestrator
6. scenario controller and reset logic
7. operator console with evidence paste flow
8. targeted Splunk API enrichment in orchestrator
9. remediation orchestrator and Python remediation agent
10. policy engine, evidence parser, and action receipt
11. verification runner
12. Splunk dashboards, service map, and detectors

### Non-Negotiable Demo Features

These are worth building even if everything else is simplified:

- one-click incident trigger
- one-click reset
- visible digital experience degradation in RUM/DEA
- one available session replay example for the failing journey
- at least three named business transactions
- grouped endpoints instead of noisy raw URLs
- detector webhook creating the incident in the orchestrator
- pasted AI Assistant summary flowing into the orchestrator
- targeted Splunk API enrichment filling missing fields for the final `EvidenceBundle`
- deterministic remediation proposal
- visible approval gate
- visible validation result
- visible agent telemetry

### Features To Avoid

Do not spend time on:

- natural-language agent sophistication
- multi-step autonomous planning
- multiple failure scenarios in the main path
- Kubernetes-only deployment unless required
- complex authentication flows

The point is not to build a smart product. The point is to build a reliable stage system.

## Splunk Assets Required

Prepare these before building the final deck:

- service health dashboard
- business impact dashboard
- remediation agent monitoring dashboard
- detectors for latency, error rate, and failed remediation
- saved views for the live scenario
- one remediation plan artifact
- one "action receipt" visual that shows:
  - observed signals
  - inferred cause
  - proposed action
  - policy mode
  - execution result
  - validation result

## Slide Plan

Keep the title exactly as approved.

Suggested deck:

1. Approved title slide
2. The incident begins
3. Why teams still stall between insight and action
4. What "AI remediation agents" should mean in this session
5. The two-agent model
6. Observing the remediation agent itself
7. Architecture and telemetry flow
8. Demo setup
9. Incident detection
10. Troubleshooting Agent evidence package
11. Audience decision point
12. Remediation action and policy gate
13. Validation and recovery
14. Auditability and trust
15. Adoption roadmap
16. Key takeaways
17. Q&A

## Presenter Split

Do not alternate randomly.

Use clear ownership:

### Marcio

- opening hook
- operational pain and incident framing
- customer and business impact
- telemetry narrative during the live incident
- closing maturity model

### Leila

- AI troubleshooting and remediation framing
- trust model
- policy controls
- agent observability
- governance and safe autonomy section

### Shared Moments

- demo handoff
- audience interaction
- final takeaways

## Success Criteria

By the end of the session, attendees should be able to say:

- I understand the difference between AI-assisted investigation and AI-governed remediation
- I understand why the remediation agent itself must be observable
- I have a model for when to allow automatic action versus approval-based action
- I saw a realistic path using Splunk Observability Cloud, not a generic AI pitch

## Deliverables To Build Next

To make this successful, create these assets in order:

1. 150-word Cisco Live session abstract refresh for speaker intro and collateral
2. final storyline and talk track
3. demo app architecture and service contract
4. telemetry plan for RUM, DEA, Session Replay, APM, and Galileo agent monitoring
5. repo scaffold and shared types
6. webhook and evidence-intake contract
7. Splunk dashboard and detector checklist
8. full slide outline with speaker notes
9. audience polling questions
10. live demo runbook
11. fallback screenshots and backup video

## Research Anchors

Use these public sources to keep the story aligned with current positioning:

- https://help.splunk.com/en/splunk-observability-cloud/monitor-end-user-experience/digital-experience-analytics/set-up-digital-experience-analytics
- https://www.splunk.com/en_us/blog/observability/ai-troubleshooting-agent-in-splunk-observability-cloud
- https://www.splunk.com/en_us/blog/observability/splunk-observability-ai-agent-monitoring-innovations.html
- https://help.splunk.com/en/appdynamics-on-premises/observability-for-ai/25.11.0/splunk-appdynamics-observability-for-ai/ai-agent-monitoring
- https://www.splunk.com/en_us/products/splunk-ai-assistant-in-observability-cloud.html
