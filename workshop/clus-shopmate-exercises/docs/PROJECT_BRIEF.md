# Project Brief

## Project Name

`CLUS-LTROBS-2001 - From Deployment to Deep Insights: Mastering AI/ML with Cisco AI Pods & Splunk`

## Project Type

`4-hour instructor-led lab`

## Core Problem

Many AI/ML environments can be deployed, but far fewer can be operated with end-to-end visibility. Teams struggle to correlate infrastructure, platform, and workload behavior when troubleshooting performance, monitoring health, or optimizing expensive AI resources.

## Project Goal

Create a realistic Cisco Live lab package that teaches attendees how to:

- understand the lab topology and Cisco AI POD-inspired AI/ML environment
- validate access to the shared Kubernetes GPU environment
- verify telemetry and operational data in Splunk
- create and interpret observability views
- investigate common AI/ML performance and health scenarios
- derive deeper operational insights from the environment
- analyze AI token usage, estimated cost, and chargeback attribution

## Target Audience

- infrastructure architects
- platform engineers
- site reliability engineers
- observability practitioners
- AI/ML platform operators
- technically oriented Cisco Live attendees

Assume the audience is comfortable with enterprise infrastructure concepts but may have varying depth in Splunk, AI/ML operations, and Cisco AI Pods.

## Learning Model

This is not a greenfield build-from-zero physical AI POD deployment lab.

The correct learning model is:

- the environment is pre-staged for the attendee
- the environment is inspired by Cisco AI POD operating patterns
- the environment uses real Kubernetes, GPU, NIM, app, and OpenTelemetry components where practical
- some Cisco hardware, network, and storage signals may be simulated or omitted
- the lab teaches attendees how to operate and analyze it
- hands-on work focuses on validation, telemetry, observability, troubleshooting, and insight generation

## Lab Promise

By the end of the lab, attendees should be able to use Splunk to monitor and analyze telemetry from a Cisco AI POD-inspired AI/ML environment, correlate GPU infrastructure and agentic application behavior, investigate operational conditions that affect performance and reliability, and produce actionable observations including tokenomics and chargeback findings.

## Tone Requirements

All generated artifacts must be:

- practical
- technical
- instructor-friendly
- credible for Cisco Live
- clear enough for attendees to follow live

Avoid:

- generic AI hype
- excessive product marketing language
- vague claims without steps, validation, or outcomes

## Narrative Arc

The lab should follow a realistic operator workflow:

1. Understand the environment
2. Validate platform and workload readiness
3. Verify data visibility in Splunk
4. Build operational views
5. Investigate a performance or health issue
6. Produce deeper insight and recommendations

## Lab Design Principles

- Optimize for reliable execution in a conference lab environment
- Prefer guided, deterministic tasks over fragile setup work
- Include expected results and validation checkpoints in every module
- Teach a repeatable method, not just a sequence of clicks
- Keep the technical bar credible without making the lab brittle
- Simulate the telemetry contract rather than the physical hardware
- Use internally consistent and causally related data rather than random values

## Assumptions

Unless replaced by actual environment details later, assume:

- no physical Cisco AI POD hardware is available in the lab
- the pilot environment runs on a shared Kubernetes cluster with GPU nodes
- NVIDIA NIM provides the LLM inference endpoint where feasible
- a custom multi-agent retail app creates realistic AI workload and tokenomics data
- a synthetic telemetry generator may still be used later for Cisco-specific UCS, Nexus, or storage dashboard compatibility
- Splunk is already available to attendees
- some data sources may already be connected, but validation is still part of the lab
- attendees have credentials and browser-based access to the required tools

## Technical Strategy

The lab should be built around a multi-tenant LLM inference and agentic retail application, not a generic infrastructure simulator and not an observability-themed chatbot.

Recommended logical services and components:

- `shopmate-ai` FastAPI application
- `ShoppingAssistantAgent`
- `CatalogAgent`
- `InventoryAgent`
- `CheckoutAgent`
- `PolicyAgent`
- `CostAgent`
- NVIDIA NIM model endpoint
- optional load generator for baseline shopping, promo campaign, token surge, agent-loop token burn, retry storm, and missing chargeback tags

The environment should emit correlated signals across:

- application and model-serving behavior
- GPU utilization and GPU memory pressure
- host and platform health
- Kubernetes namespace and workload identity
- token usage and estimated cost
- chargeback metadata quality
- agent loop detection and guardrail behavior
- optional storage and network behavior if synthetic metrics are added

## Monitoring Scope

This project should explicitly distinguish between:

- `AI Infrastructure Monitoring`
- `AI Agent Monitoring`

AI Infrastructure Monitoring is a primary lab focus.

AI Agent Monitoring and application observability are now part of the core lab story through the custom app. Infrastructure metrics alone are not sufficient; the app must emit traces, span attributes, token metrics, and chargeback dimensions.

## Validation Expectations

The project can credibly teach Cisco AI POD monitoring concepts, but exact parity with a real Cisco AI POD should not be assumed without validation.

Use this phrasing consistently in artifacts:

- the lab is Cisco AI POD-inspired and uses real GPU, Kubernetes, NIM, and app telemetry where practical
- Cisco UCS, Nexus, and enterprise storage behavior is not equivalent to a physical AI POD unless those integrations are actually deployed
- any synthetic Cisco-specific metrics are intended to populate built-in dashboards as closely as possible
- full dashboard parity must be validated in a real Splunk Observability environment

## Primary Outputs

This project should produce at minimum:

- lab overview
- learning objectives
- lab topology description
- attendee lab guide
- instructor notes
- scenario descriptions
- slide deck outline
- artifact generation plan
- agentic app design and implementation guidance
- tokenomics and chargeback exercise design
- optional datagen design and implementation guidance
- validation notes for dashboard population
