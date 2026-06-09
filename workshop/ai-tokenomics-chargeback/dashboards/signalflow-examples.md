# SignalFlow Examples

These snippets are starting points for workshop dashboards and detectors. Replace
`ai-tokenomics-workshop` with your environment or dashboard variable.

## Dashboard Charts

Total tokens by team:

```python
data('ai.tokens.total',
     filter=filter('deployment.environment', 'ai-tokenomics-workshop')).sum(by=['ai.team']).publish(label='Tokens by team')
```

Estimated cost by team and model:

```python
data('ai.request.estimated_cost_usd',
     filter=filter('deployment.environment', 'ai-tokenomics-workshop')).sum(by=['ai.team', 'gen_ai.request.model']).publish(label='Cost by team and model')
```

Cost per request by workload:

```python
cost = data('ai.request.estimated_cost_usd',
            filter=filter('deployment.environment', 'ai-tokenomics-workshop')).sum(by=['ai.workload.name'])
requests = data('ai.request.count',
                filter=filter('deployment.environment', 'ai-tokenomics-workshop')).sum(by=['ai.workload.name'])
(cost / requests).publish(label='Cost per request')
```

Input tokens per request by model:

```python
tokens = data('ai.tokens.input',
              filter=filter('deployment.environment', 'ai-tokenomics-workshop')).sum(by=['gen_ai.request.model'])
requests = data('ai.request.count',
                filter=filter('deployment.environment', 'ai-tokenomics-workshop')).sum(by=['gen_ai.request.model'])
(tokens / requests).publish(label='Input tokens per request')
```

GPU utilization by node:

```python
data('DCGM_FI_DEV_GPU_UTIL').mean(by=['k8s.node.name']).publish(label='GPU utilization')
```

GPU power by node:

```python
data('DCGM_FI_DEV_POWER_USAGE').mean(by=['k8s.node.name']).publish(label='GPU power')
```

## Detector Starting Points

Unknown attribution:

```python
data('ai.request.estimated_cost_usd',
     filter=filter('ai.team', 'unknown')).sum().publish(label='Unknown team cost')
```

Cost per request regression:

```python
cost = data('ai.request.estimated_cost_usd').sum(by=['ai.workload.name'])
requests = data('ai.request.count').sum(by=['ai.workload.name'])
(cost / requests).publish(label='Cost per request')
```

Context window explosion:

```python
tokens = data('ai.tokens.input').sum(by=['ai.workload.name'])
requests = data('ai.request.count').sum(by=['ai.workload.name'])
(tokens / requests).publish(label='Input tokens per request')
```

Tenant misuse:

```python
data('ai.request.estimated_cost_usd').sum(by=['ai.tenant.id']).publish(label='Cost by tenant')
```

GPU idle waste:

```python
data('DCGM_FI_DEV_GPU_UTIL').mean(by=['k8s.node.name']).publish(label='GPU utilization')
```

Use the detector UI to set thresholds, duration, severity, notifications, and runbook
links that match your lab.
