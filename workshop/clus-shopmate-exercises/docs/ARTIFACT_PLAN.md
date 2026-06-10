# Artifact Plan

This file defines the artifacts that should be created for the lab project and the purpose of each artifact.

## Required Deliverables

### 0. Reference Notes

Suggested path:

- `docs/REFERENCE_NOTES.md`

Purpose:

- capture the external sources and research findings that shape the project
- record feasibility conclusions and boundaries for the current app-first approach and optional datagen work

Required sections:

- source links
- feasibility summary
- dashboard validation notes
- infrastructure monitoring vs AI Agent Monitoring distinction
- Cisco AI POD similarity and difference notes

### 1. Lab Guide

Suggested path:

- `deliverables/lab-guide.md`

Purpose:

- primary attendee-facing document
- step-by-step hands-on instructions
- objectives, tasks, expected results, checkpoints, and wrap-up questions

Required sections:

- title and session metadata
- lab overview
- learning objectives
- prerequisites and assumptions
- topology / environment overview
- module-by-module instructions
- validation checkpoints
- summary and key takeaways

### 2. Instructor Guide

Suggested path:

- `deliverables/instructor-guide.md`

Purpose:

- help instructors run the 4-hour lab consistently
- provide timing, talking points, checkpoints, and recovery guidance

Required sections:

- session overview
- instructor prep checklist
- timing plan
- module-by-module facilitation notes
- common failure modes
- attendee support guidance
- debrief points

### 3. Slide Deck Outline

Suggested path:

- `deliverables/slide-outline.md`

Purpose:

- define the slide flow for lab intro, module transitions, and wrap-up
- support creation of presentation slides later

Required sections:

- slide number
- slide title
- speaker intent
- key bullets
- visual suggestion

### 4. Topology and Scenario Guide

Suggested path:

- `deliverables/topology-and-scenarios.md`

Purpose:

- describe the environment, components, data flows, and operational scenarios used in the lab

Required sections:

- environment overview
- system components
- telemetry sources
- sample AI/ML workload description
- troubleshooting scenarios
- expected observations

### 5. Build Notes

Suggested path:

- `deliverables/build-notes.md`

Purpose:

- record open assumptions, decisions, placeholders, and future details that need real environment data

Required sections:

- assumptions
- unresolved environment details
- content decisions
- future enrichment ideas

### 6. Datagen Specification

Suggested path:

- `deliverables/datagen-spec.md`

Purpose:

- define the implementation contract for the telemetry simulator
- provide a concrete handoff for AI agents or developers writing the datagen

Required sections:

- simulated topology
- workloads and services
- metric families
- dimensions and resource attributes
- scenario injections
- export method
- validation checklist

### 7. Agentic App Plan

Suggested path:

- `docs/AGENTIC_APP_PLAN.md`

Purpose:

- define the custom workload used in the lab
- specify the multi-agent pattern, API contract, telemetry contract, and tokenomics scenarios
- provide implementation guidance for AI agents writing the app

Required sections:

- app concept
- multi-agent pattern
- required services
- traces, metrics, and logs
- tokenomics use cases
- minimum viable app
- definition of done

### 8. Planning Contract

Suggested path:

- `PLANNING.md`

Purpose:

- act as the execution plan for finishing and testing the project
- split work across multiple AI agents
- define shared API, metric, and validation contracts

Required sections:

- goal
- architecture
- app behavior
- tokenomics story
- lab flow
- parallel workstreams
- shared contracts
- implementation order
- validation checklist

### 9. Student Collector Plan

Suggested path:

- `docs/STUDENT_COLLECTOR_PLAN.md`

Purpose:

- define how each student deploys a collector without duplicating cluster and GPU telemetry
- document the split between instructor infrastructure collector and student app collector
- provide the collector deployment exercise for the attendee lab

Required sections:

- collector responsibilities
- namespace-scoped collector architecture
- direct-to-Splunk vs gateway export options
- student app configuration
- workshop exercises
- GPU instrumentation boundary

### 10. GPU and NIM Metric Strategy

Suggested path:

- `docs/GPU_NIM_METRIC_STRATEGY.md`

Purpose:

- define the default GPU/NIM metric allowlist
- explain why the workshop-compatible list is preferred
- document any fallback reduced list and tradeoffs
- identify which Cisco AI POD dashboard areas are intentionally out of scope

### 11. App Instrumentation Exercises

Suggested path:

- `docs/APP_INSTRUMENTATION_EXERCISES.md`

Purpose:

- define how students instrument `shopmate-ai`
- align the lab with Splunk AI Agent Monitoring concepts
- document GenAI workflow, agent invocation, LLM invocation, tokenomics, and chargeback exercises

Required sections:

- instrumentation approach
- required packages
- required environment variables
- student exercises
- AI Agent Monitoring validation
- optional evaluation scope

### 12. Agent Flow Example

Suggested path:

- `docs/AGENT_FLOW_EXAMPLE.md`

Purpose:

- document the concrete `shopmate-ai` agent workflow
- show the expected trace shape
- define prompt capture guardrails
- explain how the same flow maps to a real Cisco AI POD

Required sections:

- example prompt
- sequence diagram
- expected spans
- required attributes
- prompt capture decision
- real Cisco AI POD mapping

### 13. Build Ready Checklist

Suggested path:

- `docs/BUILD_READY_CHECKLIST.md`

Purpose:

- define implementation workstreams
- define build order
- define first end-to-end validation
- make the project ready for multiple implementation agents

Required sections:

- app build
- app instrumentation build
- student collector build
- instructor infrastructure build
- scenario build
- lab content build
- first end-to-end test

### 14. Instructor Lab Setup Agent

Suggested path:

- `docs/INSTRUCTOR_LAB_SETUP_AGENT.md`

Purpose:

- give one implementation agent complete ownership of instructor-side lab setup
- define infrastructure outputs, validation scripts, student namespace setup, and teardown
- prevent student exercises from being blocked by cluster, GPU, NIM, RBAC, or secret setup

Required sections:

- mission
- assumptions
- required outputs
- platform setup
- instructor collector
- student namespaces
- student collector template
- app deployment template
- laptop access
- validation script
- teardown
- success criteria

### 15. Accounts And Access Plan

Suggested path:

- `docs/ACCOUNTS_AND_ACCESS_PLAN.md`

Purpose:

- define all accounts, credentials, tokens, and student access requirements
- make clear which accounts are instructor-owned and which, if any, students need
- prevent account setup from consuming lab time

Required sections:

- account summary
- instructor-owned accounts
- student requirements
- Kubernetes access model
- Splunk access model
- NVIDIA/NIM access
- secrets
- roster
- pre-lab checklist
- day-of distribution
- post-lab cleanup

### 16. Minikube macOS Test Plan

Suggested path:

- `docs/MINIKUBE_MACOS_TEST_PLAN.md`

Purpose:

- make the workshop testable locally on macOS before EKS/GPU access exists
- define fake NIM and fake DCGM services
- validate app instrumentation and collector configuration in Kubernetes

Required sections:

- local architecture
- macOS prerequisites
- fake NIM
- fake DCGM exporter
- student collector config
- validation flow
- what Minikube proves
- what Minikube does not prove

## Optional Deliverables

These are helpful if time permits:

- `deliverables/lab-handout.md`
- `deliverables/diagram-spec.md`
- `deliverables/demo-script.md`
- `deliverables/quiz-checkpoints.md`
- `deliverables/agent-monitoring-extension.md`
- `app/`
- `infra/`
- `observability/`
- `scenarios/`
- `validation/`

## Quality Bar

Every deliverable should:

- reference the exact session code and title
- align to the instructor-led lab format
- use consistent terminology
- include realistic operational detail
- avoid unsupported claims about exact product behavior unless verified
- be explicit about what is simulated versus what is collected from real systems

## Content Constraints

The lab must be centered on teaching attendees how to do something concrete. The core action loop is:

1. access the environment
2. verify what is running
3. observe telemetry in Splunk
4. investigate behavior
5. derive insight

Anything that does not support that loop is secondary.

## Datagen Constraints

The app and telemetry implementation should:

- produce readable multi-agent traces
- emit token and estimated cost metrics by student, team, namespace, and chargeback account
- support token surge, bounded agent-loop token burn, and missing chargeback tag scenarios
- make the final "which student spent the most tokens" exercise deterministic enough for a live lab

The optional datagen should:

- prioritize realistic and correlated metric behavior
- target the telemetry contract required by Splunk experiences
- avoid pretending to be a full physical Cisco AI POD deployment
- support baseline and incident-driven exercises
