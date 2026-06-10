# 5. Tokenomics And Environment Cost Signals

## Goal

Use AI telemetry to answer an operator question:

```text
Which lab environment and request pattern consumed the most tokens, and why?
```

## Tokenomics Fields

Every app request should be filterable by:

```text
service.name
deployment.environment
```

`deployment.environment` comes from `OTEL_RESOURCE_ATTRIBUTES` and is the standard environment filter for this lab. Do not add department, chargeback, or other custom resource attributes unless the instructor explicitly provides them.

Token metrics come from Splunk zero-code OpenAI/OpenAI Agents instrumentation. Depending on package versions, your tenant may show names such as `gen_ai.client.token.usage`, `gen_ai.usage.input_tokens`, or `gen_ai.usage.output_tokens`. Use the token metric names visible in your Splunk tenant.

## Step 1: Run A Baseline Conversation

Send two turns in the ShopMate assistant.

```text
Turn 1: Find a waterproof jacket under $200 for a weekend hiking trip.
Turn 2: Compare the top two options and check if medium is in stock.
```

Validate:

- token counts exist
- `deployment.environment` is present
- the trace is under `service.name=shopmate-ai` or the lab-provided ShopMate service name

## Step 2: Run A Token Surge Conversation

Send a longer fictional retail conversation.

```text
Turn 1: Build a complete race-weekend gear kit for two runners with different budgets.
Turn 2: Compare road shoes, trail shoes, shorts, and hydration pack options.
Turn 3: Add delivery timing constraints, pickup options, and return policy requirements.
Turn 4: Rewrite the recommendation as a detailed email to a running club coach.
Turn 5: Summarize the decision in five bullets and include estimated savings.
```

Expected result:

- token totals increase
- the conversation is more expensive than the baseline
- traces show larger prompt or completion token values

## Step 3: Run The Expensive Agent Request

Run a deliberately difficult request:

```text
Find waterproof trail running shoes under $40, available today, with carbon plate support, in every color, and explain all alternatives in detail.
```

Validate:

- the request returns instead of running indefinitely
- the trace shows OpenAI Agents SDK activity
- the trace shows NIM-backed LLM spans
- token totals are higher than the baseline
- explicit loop attributes might not exist, so use repeated agent/NIM spans, latency, and token totals as the evidence

## Step 4: Find Your Highest-Token Environment View

In Splunk Observability Cloud:

1. Filter by `service.name=shopmate-ai` or the lab-provided ShopMate service name.
2. Filter by `deployment.environment=<your student id>`.
3. Find token usage for your environment.
4. Split prompt tokens and completion tokens if both are available.
5. Compare baseline, token surge, and expensive prompts.
6. Open a high-token trace.

Ask:

- Which request window used the most tokens?
- Which span or model call used the most tokens?
- Did prompt tokens or completion tokens dominate?
- Did an agent call NIM more than expected?
- Did the high-token window line up with repeated agent or NIM activity?

## Step 5: Class Token Usage Challenge

Now answer the class-wide question.

Group by:

```text
deployment.environment
service.name
model
```

Find:

- highest total token environment
- highest average tokens per request window
- largest single trace or model call
- whether high usage came from normal use, token surge, repeated agent work, or retries

## Step 6: Write Your Finding

Use this format:

```text
Top environment:
Top request window or trace:
Prompt tokens vs completion tokens:
Evidence from trace:
Evidence from metrics:
Likely cause:
Recommended guardrail or operational action:
```

Examples of good recommendations:

- set a max iteration count for agent loops
- set a token budget per request
- cache repeated tool results
- fail fast on impossible catalog constraints
- review prompts that produce unusually high completion tokens

!!! success "Checkpoint"
    You can defend your answer with trace evidence, token metrics, and the standard environment filter.

## Knowledge Check

??? question "Why is request count not enough for AI cost analysis?"
    One request can use many more tokens than another. Cost analysis needs prompt tokens, completion tokens, model name, environment, and trace context.

??? question "What makes the agent-loop scenario financially important?"
    It turns an application logic problem into measurable AI spend. Without trace and token attributes, it may look like ordinary model usage.

??? question "What should you check before adding business cost tags?"
    Confirm the lab or production owner explicitly defines the attribute names and cardinality limits. Extra dimensions can make metrics harder to find or cause metric drops.
