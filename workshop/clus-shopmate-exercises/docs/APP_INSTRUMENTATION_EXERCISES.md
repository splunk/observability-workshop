# App Instrumentation Exercises

## Purpose

This document defines the application instrumentation learning track for the
ShopMate Sports workshop.

Students should not only scrape GPU/NIM metrics. They should also learn how an
AI application is connected to Splunk Observability Cloud so traces, GenAI
metrics, token usage, latency, and chargeback context can be analyzed with
infrastructure telemetry.

Current implementation decision:

- use Splunk-supported zero-code OpenAI and OpenAI Agents instrumentation
- keep NIM as the OpenAI-compatible model backend
- keep the app multi-agent with OpenAI Agents SDK
- add simple custom OpenTelemetry spans for the ShopMate workflow and each agent step
- do not emit custom app metrics, JSONL telemetry, `conversation.id`, or `scenario.name` in the first build
- attach student, department, namespace, and chargeback context with `OTEL_RESOURCE_ATTRIBUTES`

## Current Splunk AI Agent Monitoring Direction

Use Splunk AI Agent Monitoring for the `shopmate-ai` service.

Preferred path for the lab:

- Python app
- OpenAI Agents SDK for multi-agent orchestration
- NIM exposed as an OpenAI-compatible `/v1` endpoint
- Splunk zero-code OpenAI instrumentation
- Splunk zero-code OpenAI Agents instrumentation
- student collector as the OTLP destination

Why zero-code instrumentation:

- students learn the Splunk-supported path first
- it avoids custom monitoring code in the application
- it shows what is available out of the box for OpenAI-compatible agent apps
- it keeps the lab focused on setup, validation, correlation, and analysis
- it supports business grouping through resource attributes such as `student.id`, `department.name`, and `chargeback.account`

Custom code-based spans are included only where zero-code instrumentation needs
application context. The custom spans identify the retail workflow, the agent
step, and a short safe preview of the final response. Zero-code instrumentation
still provides the SDK, model, token, latency, and GenAI metric details.

The custom spans intentionally use `shopmate.*` attributes rather than
`gen_ai.*` semantic attributes. This keeps Splunk AI Agent Monitoring's Agent
Flow focused on the zero-code OpenAI Agents SDK spans and prevents duplicate
agent nodes.

## What The Multi-Agent App Does

ShopMate Sports is a fictional retail assistant. It is not an observability
assistant.

Agent pattern:

- `ShoppingAssistantAgent`: receives the shopper request and coordinates the answer.
- `CatalogAgent`: helps with product search and product comparisons.
- `InventoryAgent`: reviews stock and availability from catalog data.
- `PolicyAgent`: handles return, shipping, promotion, and fit-policy questions when the demo catalog has enough information.
- `CheckoutAgent`: summarizes cart and checkout considerations without creating real orders.
- `CostAgent`: explains relative agent/LLM work for tokenomics discussion.
- NIM model: runs the specialist agents through an OpenAI-compatible API.
- Custom coordinator span: records the grounded final response that the shopper sees.

The app does not substitute deterministic local chat responses. If NIM is not
configured or the Agents SDK call fails, `/api/chat` returns an error so the
missing model path is obvious during validation.

## Required Packages

The app package set should include:

```text
openai
openai-agents
splunk-opentelemetry
splunk-otel-instrumentation-openai
splunk-otel-instrumentation-openai-agents
```

The active requirements file is:

```text
shopmate-sports/requirements.txt
```

## Required Environment Variables

Each student app should run with these telemetry settings:

```text
OTEL_SERVICE_NAME=shopmate-ai
OTEL_EXPORTER_OTLP_ENDPOINT=http://student-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_RESOURCE_ATTRIBUTES=student.id=student-01,team.name=team-a,department.name=marketing,department.cost_center=cc-4100,chargeback.account=cb-student-01,k8s.namespace.name=student-01,deployment.environment=student-01,k8s.cluster.name=clus-ltrobs-2001-student-01
OTEL_INSTRUMENTATION_GENAI_EMITTERS=span_metric
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY
OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta
```

Each student app should run with these model settings:

```text
NIM_BASE_URL=http://nim-service.nim-system.svc.cluster.local:8000/v1
NIM_API_KEY=<provided-by-instructor>
NIM_MODEL=<provided-by-instructor>
SHOPMATE_AGENT_MAX_TURNS=6
```

The important mapping is:

- `OTEL_SERVICE_NAME` becomes `service.name` in Splunk APM and trace search.
- `OTEL_EXPORTER_OTLP_ENDPOINT` points the app at the student's collector.
- `OTEL_RESOURCE_ATTRIBUTES` supplies student, department, namespace, cluster, and chargeback dimensions.
- `OTEL_INSTRUMENTATION_GENAI_EMITTERS=span_metric` asks the GenAI instrumentation to emit spans and metrics.
- `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY` captures safe synthetic prompts and responses on spans where supported.
- `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta` keeps metrics compatible with the collector/export path used in the lab.
- `NIM_BASE_URL` is the OpenAI-compatible NIM base URL, not the full `/chat/completions` URL.

Only fictional retail prompts should be used. Do not enter real personal,
payment, health, customer, or confidential data.

## Student Exercise Flow

### Exercise 1: Start With Zero-Code Instrumentation

Goal:

- run the app with `opentelemetry-instrument` and no custom monitoring code

Steps:

1. Confirm the student collector is running.
2. Export the required OTEL variables.
3. Export the NIM variables.
4. Start the app with `opentelemetry-instrument python shopmate-sports/server.py`.
5. Open the ShopMate Sports website.
6. Send one simple shopping prompt.

Validation:

- Splunk shows `service.name=shopmate-ai`.
- Trace search can filter by `student.id`.
- Trace search can filter by `department.name`.
- Trace search can filter by `chargeback.account`.
- The app response comes from NIM when `nim_enabled=true` is returned by the API.

### Exercise 2: Validate Resource Attributes

Goal:

- prove that chargeback and student isolation come from `OTEL_RESOURCE_ATTRIBUTES`

Steps:

1. Open one trace for `service.name=shopmate-ai`.
2. Inspect resource attributes.
3. Confirm the student namespace and department are attached.
4. Change only `department.name` and `chargeback.account` in a test deployment.
5. Send another prompt.
6. Confirm the new values appear in Splunk.

Validation:

- traces and metrics can be grouped by `student.id`
- traces and metrics can be grouped by `department.name`
- traces and metrics can be grouped by `department.cost_center`
- traces and metrics can be grouped by `chargeback.account`

### Exercise 3: Validate OpenAI Agents SDK Telemetry

Goal:

- see the multi-agent path without manually creating spans

Steps:

1. Send a product-comparison prompt.
2. Open the trace in Splunk.
3. Look for spans or events produced by OpenAI Agents SDK instrumentation.
4. Identify where the request reached the model backend.
5. Compare the app request duration with the LLM call duration.

Example prompt:

```text
Compare trail running shoes and soccer cleats for someone training on wet grass twice a week.
```

Validation:

- agent or workflow activity is visible where supported by the installed Splunk instrumentation
- OpenAI-compatible model calls are visible
- model name is populated
- prompt/response content is visible only when capture is enabled and supported

### Exercise 4: Understand Custom Workflow Spans

Goal:

- explain why a small amount of custom instrumentation can make an agent trace easier to read

What to look for:

- `shopmate.workflow`: one span for the whole shopper request
- `shopmate.agent.CatalogAgent`: product search and tradeoffs
- `shopmate.agent.InventoryAgent`: inventory and pickup or delivery context
- `shopmate.agent.PolicyAgent`: returns, fit, shipping, and policy context
- `shopmate.agent.CheckoutAgent`: demo cart and checkout caveats
- `shopmate.agent.CostAgent`: tokenomics context for the workshop
- `shopmate.agent.ShoppingAssistantAgent`: final coordinator response

Simple explanation:

Zero-code instrumentation sees the libraries. It should populate the Agent Flow
with OpenAI Agents SDK activity, NIM model calls, tool calls, tokens, and
latency. It does not always know what the app developer meant by a business
workflow.

The custom spans add that missing business context. They do not replace
zero-code instrumentation and they are not marked as GenAI agent spans. They
give the trace waterfall a readable backbone so students can say, "This user
request became one ShopMate workflow, which called these app steps, which then
called NIM."

Validation:

- the trace has one `shopmate.workflow` span for the request
- each expected `shopmate.agent.*` span appears under the workflow
- the final response preview is attached to `shopmate.workflow`
- the Agent Flow uses the zero-code OpenAI Agents SDK spans instead of duplicating the custom `shopmate.agent.*` spans
- the OpenAI/NIM spans still appear inside or near the custom app steps
- no real personal, payment, health, customer, or confidential data is present in custom attributes

### Exercise 5: Validate Token Metrics

Goal:

- find prompt, completion, and total token usage from zero-code instrumentation

Steps:

1. Send one short prompt.
2. Send one long comparison prompt.
3. Find GenAI token metrics in Splunk.
4. Compare token usage between the two requests.
5. Group the metric by `department.name` or `student.id`.

Example long prompt:

```text
Build a detailed shopping plan for a family of four preparing for a rainy weekend soccer tournament, including shoes, recovery gear, hydration, and budget tradeoffs.
```

Validation:

- token usage increases for the longer request
- token usage can be grouped by student and department resource attributes
- the token metric and trace point to the same `service.name`

### Exercise 6: Correlate App, NIM, And GPU Telemetry

Goal:

- connect user-visible latency to model-serving and GPU pressure

Compare:

```text
shopmate-ai trace duration
OpenAI/NIM call duration
num_requests_running
num_requests_waiting
time_to_first_token_seconds
DCGM_FI_DEV_GPU_UTIL
DCGM_FI_DEV_FB_USED
```

Validation:

- students can explain whether latency came from the app, NIM queueing, or GPU pressure
- traces use the student attributes while shared GPU/NIM metrics show the platform pressure
- the instructor can explain how this maps to a real Cisco AI POD design

### Exercise 7: Tokenomics Challenge

Goal:

- answer a business chargeback question using only zero-code telemetry and resource attributes

Challenge:

```text
Which department and student generated the most token usage during the free conversation exercise?
```

Steps:

1. Instructor assigns each student a department and chargeback account.
2. Students run a free multi-turn retail conversation.
3. Students include at least one long comparison prompt.
4. Students do not use real customer or payment data.
5. Students build a Splunk chart grouped by `department.name`.
6. Students build a Splunk chart grouped by `student.id`.
7. Students inspect traces for one high-token request.

Validation:

- the highest-token department is identifiable
- the highest-token student is identifiable
- the analysis uses resource attributes, not custom app telemetry
- students can explain whether high spend came from request count, prompt length, or response length

## Reset And Troubleshooting

Reset one student app deployment:

```bash
kubectl -n student-01 rollout restart deployment/shopmate-ai
```

Delete and recreate one student app deployment:

```bash
kubectl -n student-01 delete deployment shopmate-ai
kubectl -n student-01 delete service shopmate-ai
```

Inspect app logs:

```bash
kubectl -n student-01 logs deploy/shopmate-ai --tail=100
```

Inspect collector logs:

```bash
kubectl -n student-01 logs deploy/student-collector --tail=100
```

Check environment variables inside the pod:

```bash
kubectl -n student-01 exec deploy/shopmate-ai -- env | sort
```

Common issues:

- no traces: check `OTEL_EXPORTER_OTLP_ENDPOINT`, collector service name, and collector logs
- no token metrics: check package installation, `OTEL_INSTRUMENTATION_GENAI_EMITTERS=span_metric`, `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta`, and collector `send_otlp_histograms: true`
- no prompt content: check `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY`
- flat agent trace: check for `shopmate.workflow` and `shopmate.agent.*` custom spans
- no student grouping: check `OTEL_RESOURCE_ATTRIBUTES`
- app falls back instead of NIM: check `NIM_BASE_URL`, `NIM_API_KEY`, and `NIM_MODEL`

## Definition Of Done

App instrumentation is ready when:

- `shopmate-ai` traces reach Splunk
- OpenAI-compatible NIM calls are visible through zero-code instrumentation
- OpenAI Agents SDK activity is visible where supported
- `shopmate.workflow` and `shopmate.agent.*` spans make the multi-agent flow readable
- token metrics are visible
- prompt capture works with safe synthetic prompts
- traces and metrics are filterable by `student.id`
- traces and metrics are groupable by `department.name` and `chargeback.account`
- app traces can be correlated with NIM and GPU metrics
