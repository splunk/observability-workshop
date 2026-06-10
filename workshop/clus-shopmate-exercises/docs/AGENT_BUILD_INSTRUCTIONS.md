# Agent Build Instructions

This file is written for AI agents and human contributors who will generate the lab artifacts for this project.

## Mission

Create the source content for a realistic Cisco Live instructor-led lab:

- Session code: `CLUS-LTROBS-2001`
- Title: `From Deployment to Deep Insights: Mastering AI/ML with Cisco AI Pods & Splunk`
- Duration: `4 hours`
- Format: `Instructor-led lab`

The resulting content should be sufficient to produce a full lab package without requiring the original requester to restate the concept.

This project uses a Cisco AI POD-inspired shared GPU environment with an instrumented AI app. Do not assume access to real Cisco AI POD hardware.

## Build Order

Create deliverables in this order:

1. planning contract
2. agentic app plan
3. topology and scenario guide
4. infrastructure setup guide
5. observability validation guide
6. attendee lab guide
7. instructor guide
8. slide outline
9. optional datagen spec

This order is intentional. The scenario and topology definition should drive the rest of the content.

## Source-of-Truth Rules

Follow these rules while creating artifacts:

- Use the session code and title exactly as written
- Treat this project as an operational lab, not a keynote or breakout talk
- Assume a shared pre-staged Kubernetes GPU environment unless concrete instructions say otherwise
- Assume students deploy namespace-scoped collectors for application telemetry
- Do not have every student deploy a full cluster-wide collector with DaemonSet and clusterReceiver enabled
- Prefer realistic workflows over ambitious but fragile setup tasks
- Include validation checkpoints and expected results in every hands-on module
- Keep content self-contained and executable by instructors
- Be explicit when content refers to simulated telemetry rather than physical hardware
- Separate infrastructure monitoring claims from AI Agent Monitoring claims
- Include tokenomics and chargeback as first-class observability topics

## Required Learning Flow

Every artifact should reinforce this sequence:

1. orient the attendee to the environment
2. validate access and baseline health
3. confirm telemetry visibility in Splunk
4. build or inspect observability views
5. investigate a guided operational issue
6. summarize deeper insights and recommendations

The preferred environment model is a multi-tenant LLM inference platform with a simple multi-agent app, correlated application traces, GPU/NIM telemetry, Kubernetes metadata, token usage, and chargeback metrics.

## Suggested Lab Modules

Agents should use these as the default module structure unless better environment details become available:

### Module 0: Introduction and environment orientation

Attendee outcome:

- understand the lab goal, tools, and topology

### Module 1: Validate the AI/ML environment

Attendee outcome:

- identify key components and confirm GPU, NIM, app, and telemetry readiness

### Module 2: Verify telemetry in Splunk

Attendee outcome:

- deploy a namespace-scoped collector and confirm app telemetry is available for analysis

### Module 3: Build operational visibility

Attendee outcome:

- use Splunk searches, filters, or dashboards to understand system behavior

### Module 4: Investigate a performance or health scenario

Attendee outcome:

- perform guided troubleshooting using correlated data

### Module 5: Derive deeper insights

Attendee outcome:

- move from raw telemetry to operational and chargeback recommendations

### Module 6: Tokenomics challenge

Attendee outcome:

- identify which student spent the most tokens and explain why using Splunk evidence

## Agentic App Guidance

When generating app-related artifacts, assume the primary workload is `shopmate-ai`, a simple multi-agent retail shopping assistant. The app should feel like a real e-commerce AI feature; instrumentation is the workshop skill, not the app domain.

Required agents:

- `ShoppingAssistantAgent`
- `CatalogAgent`
- `InventoryAgent`
- `CheckoutAgent`
- `PolicyAgent`
- `CostAgent`

Required use cases:

- baseline shopping request
- promo campaign
- expensive personalization request
- token surge
- bounded `CatalogAgent` loop causing token burn
- most expensive student leaderboard
- missing chargeback tags
- retry storm if time permits

Required telemetry:

- traces for each agent and tool step
- custom token metrics
- estimated cost metrics
- agent loop detection and max-iteration guardrail attributes
- chargeback validity metrics
- structured logs for failures and scenario activation

Collector guidance:

- instructor owns Kubernetes metrics and authoritative platform baseline collection
- student owns a namespace collector for app telemetry
- student app exports OTLP to the student collector
- student collector exports directly to Splunk Observability Cloud
- student collector scrapes shared DCGM/NIM endpoints for the hands-on GPU/NIM exercise
- do not have students collect Kubernetes metrics; correlate with instructor-collected Kubernetes metrics by namespace/pod/service attributes

## Datagen Guidance

When generating datagen-related artifacts, treat datagen as optional support for Cisco-specific hardware, network, or storage dashboard compatibility. The primary workload is now the instrumented app.

If datagen is used, assume the primary simulated workload is:

- a multi-tenant LLM inference environment

Recommended logical services:

- `customer-support-assistant`
- `document-summarizer`
- `code-assistant`
- optional background workload: `nightly-embedding-batch`

Recommended scenario set:

1. normal operations
2. traffic surge causing latency increase
3. noisy neighbor causing GPU imbalance
4. storage slowdown affecting responsiveness
5. service restart causing errors

The datagen should produce causally related telemetry rather than random values.

## Writing Standards

When generating attendee instructions:

- use numbered steps
- use direct action verbs
- include expected results after each exercise
- include short validation guidance when something could go wrong
- avoid large unexplained jumps between steps

When generating instructor notes:

- include module timing
- include the teaching point for each exercise
- include what a successful result looks like
- include recovery guidance for common issues

When generating datagen specs:

- define metric families and resource attributes explicitly
- state which dashboard or concept each metric family supports
- note any assumptions that require validation in Splunk

## Constraints

Do not assume attendees will:

- deploy a full AI cluster from scratch
- manually configure a large number of infrastructure primitives
- spend significant time on complex installation tasks

Do assume attendees can:

- access a browser-based lab environment
- log in to Splunk and related interfaces
- run guided searches
- inspect dashboards and data
- answer structured analysis questions

Do not assume the project can automatically populate every built-in dashboard chart without validation. Treat dashboard population as an iterative compatibility target.

## Placeholder Policy

Use placeholders when exact technical details are not yet known, but do so explicitly.

Examples:

- `<SPLUNK_URL>`
- `<LAB_USERNAME>`
- `<WORKLOAD_NAME>`
- `<INDEX_NAME>`
- `<OTLP_ENDPOINT>`
- `<K8S_CLUSTER_NAME>`

Never hide missing information inside vague wording. If a detail is not yet known, mark it clearly as a placeholder.

## Deliverable Expectations

By default, generated markdown files should be:

- cleanly structured
- easy to scan in a live lab
- suitable for later conversion into slides, PDFs, or wikis

Where useful, include links to the external references captured in [`docs/REFERENCE_NOTES.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/REFERENCE_NOTES.md).

## Definition of Done

The project is in good shape when:

- an instructor could run the lab using the instructor guide
- an attendee could follow the lab guide without constant rescue
- the content clearly teaches a repeatable operational workflow
- the artifacts are coherent and consistent with each other
- the shared GPU/NIM/app environment strategy is clearly documented
- the agentic app has a concrete implementation contract
- tokenomics and chargeback exercises are testable
- any optional datagen scope is explicitly marked as optional
