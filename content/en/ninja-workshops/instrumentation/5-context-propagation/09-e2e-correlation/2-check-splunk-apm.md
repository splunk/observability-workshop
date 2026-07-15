---
title: Explore APM in Splunk
weight: 2
time: 5 minutes
 
---
 In this step, you will review what the full APM end-to-end correlation looks like in Splunk Observability Cloud.

## Verify in Splunk APM

### Explore Trace

1. From RUM session - Open the trace linked from RUM 
    OR (paste the trace ID from the `traceparent` header or completed purchase request in the UI)

You will see a RUM correlation hyperlink that will take you to the RUM session from previous step.

![trace-aft1](../images/s-trace-aft.png)

### Explore Service Map

1. Navigate to **APM → Service Map**
2. Filter environment: `workshop-context-prop`
3. Confirm all services appear with traffic edges:
   - `frontend-api` → `catalog-api`
   - `frontend-api` → `order-api` (via gateway)
   - `frontend-api` → `payment-gateway` → `payment-api`
   - `payment-api` → `fulfillment-worker` (via RabbitMQ)

This shows the expected E2E correlation across all the service and infrastructure layers.

![servicemap-aft1](../images/servicemap-aft.png)
