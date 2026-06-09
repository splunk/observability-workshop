---
title: 5. Build Token Cost Signals
weight: 5
---

Once token metrics carry owner dimensions, Metric Finder and dashboard charts can answer
tokenomics questions directly.

## Validate Custom Metrics

{{% notice title="Exercise" style="green" icon="running" %}}

Confirm that the custom metrics are arriving:

1. Open **Metric Finder**.
2. Search for `ai.tokens.input`.
3. Select the metric and group by `ai.team`.
4. Repeat for `ai.tokens.output`, `ai.tokens.total`, and
   `ai.request.estimated_cost_usd`.
5. Filter to your `deployment.environment` or `k8s.cluster.name`.
6. Confirm that the team, tenant, workload, cost center, and model dimensions appear.

<!-- TODO screenshot: Metric Finder showing ai.tokens.total grouped by ai.team and filtered to the workshop environment. -->
![Metric Finder token total grouped by team](images/metric-finder-token-total-by-team.png)

{{% /notice %}}

## SignalFlow Building Blocks

Use these charts as the first row of the dashboard:

```python
# Total token rate by team.
data('ai.tokens.total',
     filter=filter('deployment.environment', 'ai-tokenomics-workshop')).sum(by=['ai.team']).publish(label='Tokens')
```

```python
# Estimated request cost by team and model.
data('ai.request.estimated_cost_usd',
     filter=filter('deployment.environment', 'ai-tokenomics-workshop')).sum(by=['ai.team', 'gen_ai.request.model']).publish(label='Estimated cost')
```

```python
# Cost per request by workload.
cost = data('ai.request.estimated_cost_usd').sum(by=['ai.workload.name'])
requests = data('ai.request.count').sum(by=['ai.workload.name'])
(cost / requests).publish(label='Cost per request')
```

The companion file `workshop/ai-tokenomics-chargeback/dashboards/signalflow-examples.md`
contains more examples for dashboard charts and detectors.

## Tokenomics Views

Build charts that answer these questions:

| Question | Metric pattern |
| --- | --- |
| Which teams use the most tokens? | `ai.tokens.total` by `ai.team` |
| Which tenants drive output-heavy responses? | `ai.tokens.output` by `ai.tenant.id` |
| Which model is most expensive? | `ai.request.estimated_cost_usd` by `gen_ai.request.model` |
| Which workload has high cost per request? | cost divided by `ai.request.count` |
| Which requests have large context windows? | input tokens divided by request count |

{{% notice title="Exercise" style="green" icon="running" %}}

Create a draft dashboard named `AI Tokenomics and Chargeback - Workshop`:

1. Add a dashboard variable for `deployment.environment`.
2. Add a dashboard variable for `ai.team`.
3. Add a dashboard variable for `gen_ai.request.model`.
4. Add a single value chart for total estimated cost.
5. Add a stacked area chart for total tokens by team.
6. Add a table chart for cost by team, tenant, workload, and model.
7. Add a chart for cost per request by workload.

<!-- TODO screenshot: Draft tokenomics dashboard with cost, tokens by team, cost table, and cost per request charts. -->
![Draft tokenomics dashboard](images/tokenomics-dashboard-draft.png)

{{% /notice %}}
