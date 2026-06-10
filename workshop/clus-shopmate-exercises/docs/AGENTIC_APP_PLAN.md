# Agentic App Plan

## Purpose

The lab needs a real-world AI workload that students can instrument. The app should not be about observability, telemetry, infrastructure, or troubleshooting. Those are the skills students learn around the app.

The recommended app is `shopmate-ai`, a retail shopping assistant for a fictional online store.

`shopmate-ai` is a teaching workload. It behaves like a realistic e-commerce AI feature, produces GPU-backed inference demand through NVIDIA NIM, and gives students a clean target for application tracing, tokenomics, and chargeback.

## Simple Runtime Model

The instructor runs the shared platform:

1. Kubernetes cluster with GPU nodes.
2. NVIDIA GPU Operator.
3. NVIDIA NIM model endpoint.
4. Splunk OpenTelemetry Collector.
5. `shopmate-ai` application.

Students run requests against the app and configure or validate instrumentation. They do not need to build the full cluster during the 4-hour lab.

In simple terms:

```text
Student request -> Retail AI app -> NIM model on GPU -> App response
                         |
                         v
                 traces, metrics, logs
                         |
                         v
              Splunk Observability Cloud
```

## App Concept

Students act as users or tenants of a retail AI service. They ask the app for help with shopping, products, orders, and returns.

Example prompts:

- "Find a waterproof running shoe under $120."
- "Compare these two headphones and recommend one for travel."
- "Create a cart for a week of healthy breakfast items under $50."
- "Where is my order and should I expect a delay?"
- "Can I return a jacket after 45 days if the tags are removed?"
- "Build a gift bundle for a 10-year-old who likes science."

This gives the workshop a believable business app while still exercising AI infrastructure.

## Multi-Agent Pattern

Use a simple supervisor pattern.

Agents:

1. `ShoppingAssistantAgent` receives the customer request and coordinates the answer.
2. `CatalogAgent` searches products, compares items, and suggests alternatives.
3. `PolicyAgent` answers return, warranty, shipping, and promotion questions.

Keep the agent pattern simple. The goal is to create a believable multi-agent
retail workflow that can be observed through Splunk-supported zero-code
instrumentation.

## Required Services

### API service

Recommended implementation:

- Python standard library HTTP service or FastAPI if later needed
- `opentelemetry-instrument` startup
- Splunk zero-code OpenAI and OpenAI Agents instrumentation
- OpenAI Agents SDK
- OpenAI-compatible client pointed at NVIDIA NIM
- small in-memory or JSON product catalog

Required endpoints:

- `GET /healthz`
- `POST /api/chat`

Do not add app-side usage ledgers, Prometheus app metrics, or custom monitoring
scenario endpoints in the first zero-code build.

### Load generator

Recommended implementation:

- Python CLI or Kubernetes Job
- accepts `student_id`, `team`, `namespace`, `profile`, and `duration`
- sends realistic retail prompts to the app

Required profiles:

- `baseline-shopping`
- `promo-campaign`
- `token-surge`
- `agent-loop-token-burn`
- `retry-storm`
- `missing-chargeback-tags`

### Student UI

Minimum viable option:

- FastAPI Swagger UI

Preferred option if time permits:

- simple Streamlit or static web UI with a chat box, sample retail prompts, and a usage table

Do not block the workshop on a polished UI.

## Business Tools

The app should include deterministic tools so traces show useful work before and after the NIM call.

Tools:

- `search_catalog(query, filters)`
- `get_product(product_id)`
- `check_inventory(product_id, location)`
- `estimate_delivery(product_id, zip_code)`
- `apply_promotion(cart, promo_code)`
- `create_mock_order(cart, student_id)`
- `lookup_order(order_id)`
- `lookup_policy(policy_type)`

These tools can return static JSON data. They do not need external dependencies.

## Telemetry Requirements

Students are learning to instrument the app, so the app must produce traces, metrics, and logs. The app topic is retail; the instrumentation topic is the lab.

Use Splunk-supported zero-code OpenAI/OpenAI Agents instrumentation for the primary lab path. The app should use OpenAI Agents SDK with NIM as an OpenAI-compatible backend so GenAI workflow, agent, tool, and LLM telemetry is captured without custom monitoring code.

For the lab, the app should capture safe synthetic prompt and response content so students can see the complete agent flow. Use only fictional retail prompts. Do not capture real customer, payment, personal, health, or confidential data.

Recommended lab setting:

```text
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY
```

If a specific AI Agent Monitoring view requires event-based conversation detail, the instructor can test `SPAN_AND_EVENT` before the lab. Do not enable it by default until payload size and privacy behavior are validated.

### Traces

The first build must not create custom monitoring spans. Every `POST /api/chat`
request should be traced by OpenTelemetry Python auto instrumentation, Splunk
OpenAI instrumentation, and Splunk OpenAI Agents instrumentation.

Expected trace data:

- HTTP/server spans for the ShopMate request path.
- OpenAI Agents SDK spans for `ShoppingAssistantAgent`, `CatalogAgent`, and `PolicyAgent` where supported.
- OpenAI client spans for the NIM OpenAI-compatible chat completion.
- safe prompt/response content where supported and enabled with `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY`.

Required resource attributes:

- `student.id`
- `team.name`
- `department.name`
- `department.cost_center`
- `k8s.namespace.name`
- `service.name`
- `deployment.environment`
- `k8s.cluster.name`
- `chargeback.account`

Do not rely on custom `conversation.id`, `scenario.name`, loop, cost, or retail
attributes in the zero-code build. Those can be documented as a future
production extension after the supported zero-code path is validated.

### Metrics

Do not emit custom monitoring metrics in the first zero-code build. Use Splunk zero-code GenAI metrics and resource attributes first.

Expected metric families come from Splunk zero-code GenAI instrumentation. Exact
metric names depend on the installed instrumentation version and OpenTelemetry
semantic convention level, but they should represent request duration and token
usage for OpenAI-compatible calls.

Required dimensions come from resource attributes:

- `student.id`
- `team.name`
- `department.name`
- `department.cost_center`
- `k8s.namespace.name`
- `service.name`
- `ai.model.name`
- `ai.agent.name`
- `chargeback.account`

### Logs

The first build does not emit custom monitoring logs. Normal application logs
are acceptable for troubleshooting:

- request start and finish
- NIM errors
- tool failures

## Tokenomics Use Cases

### Use Case 1: Baseline retail AI usage

Students send normal shopping requests and verify that each request produces:

- prompt token count
- completion token count
- total token count
- estimated cost
- chargeback account

Teaching point: business AI features need cost attribution by user, tenant, namespace, team, or application owner.

### Use Case 2: Promo campaign token surge

Instructor triggers a simulated promotional campaign.

Expected behavior:

- more shopping requests
- longer product comparison prompts
- higher completion token limits
- increased token throughput
- higher estimated AI cost
- possible higher NIM queue depth or latency

Teaching point: a business event can increase GPU and AI platform pressure even if the application is healthy.

### Use Case 3: Expensive personalization

Some students use prompts that ask for bundles, comparisons, and long explanations.

Expected behavior:

- fewer requests can still create high token spend
- traces show larger prompts and completions
- token charts show that request count and cost are not the same thing

Teaching point: chargeback must account for tokens, not only request volume.

### Use Case 4: Most expensive department and student

Students use Splunk to answer:

"Which department and student spent the most tokens during the retail promotion or free conversation, and what caused it?"

Required analysis:

- rank token usage metrics by `department.name`
- rank token usage metrics by `student.id`
- compare prompt vs completion tokens
- inspect traces for expensive requests
- identify whether spend came from promo campaign traffic, expensive personalization, retries, or normal usage

Teaching point: AI cost can be explained when traces and metrics carry business identity.

### Use Case 5: Agent loop token burn

The instructor triggers a bounded runaway-agent scenario.

Example prompt:

```text
Find waterproof trail running shoes under $40, available today, with carbon plate support, in every color, and explain all alternatives in detail.
```

Expected behavior in the zero-code build:

- the prompt usually produces a larger response and higher token usage than a simple request
- OpenAI Agents and NIM spans show the model-serving path where supported
- the exercise is analyzed by token usage and latency, not custom loop attributes

Teaching point: high AI spend can come from application orchestration defects, not only high user demand or GPU capacity issues.

### Use Case 6: Missing chargeback context

The instructor can demonstrate what happens when `chargeback.account` is absent
from `OTEL_RESOURCE_ATTRIBUTES` in a controlled test deployment.

Expected behavior:

- traces and token metrics still arrive
- chargeback grouping is incomplete
- the class can compare a correctly tagged student deployment with an untagged deployment

Teaching point: AI chargeback fails when telemetry does not include business context.

## Lab Fit

The app supports the full 4-hour flow:

1. validate the shared GPU and NIM platform
2. deploy or validate the retail AI app
3. instrument the app with OpenTelemetry
4. confirm traces and token metrics in Splunk
5. run a free multi-turn retail conversation
6. run retail traffic scenarios
7. correlate app behavior with GPU and NIM behavior
8. perform chargeback analysis
9. identify the most expensive department and student

## Implementation Boundaries

- Keep the business app simple and believable.
- Use NIM for final customer-facing responses.
- Use deterministic tools for catalog, inventory, order, promotion, and policy lookups.
- Do not make the app an observability assistant.
- Do not require external SaaS agent frameworks.
- Do not require a real Cisco AI POD.
- Prefer working instrumentation over complex app features.

## Minimum Viable App

The minimum build for same-day testing is:

- Python service with `POST /api/chat`
- OpenAI Agents SDK supervisor plus catalog and policy agents
- NIM call using OpenAI-compatible API
- fake NIM mode for local tests
- Splunk zero-code OpenAI and OpenAI Agents instrumentation
- chargeback and student context supplied through `OTEL_RESOURCE_ATTRIBUTES`
- one load generator profile for baseline shopping
- one load generator profile for promo campaign or token surge
- one expensive-prompt profile for token surge analysis

## Definition of Done

The app is ready for lab validation when:

- one student can send a retail shopping request and receive a NIM-backed answer
- traces appear in Splunk from zero-code OpenAI/OpenAI Agents instrumentation
- token metrics appear in Splunk with `student.id` and `chargeback.account`
- GPU and NIM metrics can be viewed alongside app traces
- promo campaign or token surge creates a visible metric and trace difference
- app deployment works in Kubernetes with documented commands
