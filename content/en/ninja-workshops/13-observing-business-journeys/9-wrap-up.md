---
title: 9. Wrap Up
weight: 9
time: 10 minutes
---

You mapped a microservices app to business transactions, enriched OpenTelemetry traces with business context, created Observability Cloud detector routing, and modeled ITSI services that show business impact when a technical issue occurs.

## What You Built

- A local Minikube deployment of the OpenTelemetry Astronomy Shop.
- A Splunk collector pipeline that adds business transaction attributes.
- A business journey map for catalog, cart, checkout, and order confirmation.
- A detector strategy that sends business-aware alerts to Splunk platform.
- An ITSI service model that rolls technical issues up to customer and revenue impact.
- Controlled incident scenarios using Astronomy Shop feature flags.

## Production Checklist

- Replace workshop impact estimates with approved business metrics.
- Agree on business transaction names with service owners and business owners.
- Add business attributes in application instrumentation where possible, using collector rules only where code changes are not practical.
- Keep MetricSet cardinality controlled.
- Version the business transaction map with the application or platform repository.
- Add detector ownership, runbooks, and ITSI aggregation policy ownership.
- Test alert and clear events before relying on ITSI service health in production.

## Cleanup

Remove the local lab:

```bash
cd workshop/observing-business-journeys
./scripts/cleanup.sh
```

If you created temporary detectors, ITSI services, or HEC tokens for the workshop, remove or disable them after class.
