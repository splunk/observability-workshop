# SignalFlow Examples

These examples are starting points for Splunk Observability Cloud charts or detectors after you create Monitoring MetricSets for `business.transaction`, `business.capability`, and `business.criticality`.

Metric and dimension names can vary based on MetricSet configuration. Confirm names in Metric Finder before creating detectors.

## Checkout Request Rate

```python
requests = data('service.request.count',
  filter=filter('business_transaction', 'Complete Checkout')
).sum().publish(label='checkout requests')
```

## Checkout p99 Latency

```python
latency = data('service.request.duration.ns.p99',
  filter=filter('business_transaction', 'Complete Checkout')
).mean().scale(0.000001).publish(label='checkout p99 ms')
```

## Checkout Error Count

```python
errors = data('service.request.count',
  filter=filter('business_transaction', 'Complete Checkout') and filter('sf_error', 'true')
).sum().publish(label='checkout errors')
```

## Capability Split

```python
latency = data('service.request.duration.ns.p99').mean(by=['business_capability']).scale(0.000001)
latency.publish(label='p99 latency by capability')
```
