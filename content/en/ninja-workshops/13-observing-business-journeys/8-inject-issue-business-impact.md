---
title: 8. Inject an Issue
weight: 8
time: 20 minutes
---

Astronomy Shop includes built-in feature flags that simulate failures. Use them to create a controlled incident and verify the Observability Cloud to ITSI flow.

## Scenario 1: Checkout Impact

Enable a payment failure:

```bash
cd workshop/observing-business-journeys
./scripts/set-flag.sh checkout
```

Expected behavior:

- Checkout requests begin failing.
- APM shows errors around `checkout` and `payment`.
- The checkout detector fires in Observability Cloud.
- Splunk platform receives an alert event.
- ITSI opens or updates an episode for **Complete Checkout**.
- The glass table shows revenue impact on **Astronomy Shop Revenue**.

## Scenario 2: Cart Impact

Enable a cart failure:

```bash
./scripts/set-flag.sh cart
```

Expected behavior:

- Cart operations fail.
- APM highlights the `cart` service and its dependency on `valkey-cart`.
- ITSI marks **Manage Cart** unhealthy.
- **Complete Checkout** may also degrade if its dependency on cart is weighted heavily.

## Scenario 3: Catalog Impact

Enable a product catalog failure:

```bash
./scripts/set-flag.sh catalog
```

Expected behavior:

- Product detail or browse flows fail.
- APM points to `product-catalog`.
- ITSI marks **Browse Catalog** unhealthy.
- The top-level business service may degrade without becoming critical if checkout is still healthy.

## Clear the Scenario

Return all workshop flags to healthy:

```bash
./scripts/set-flag.sh healthy
```

Confirm:

```bash
./scripts/status.sh
```

## ITSI-Only Demo Path

If the Observability Cloud detector has not fired yet, push the equivalent alert event to Splunk platform so students can still see ITSI update:

```bash
export SPLUNK_HEC_URL=https://<splunk-host>:8088
export SPLUNK_HEC_TOKEN=<hec-token>
export SPLUNK_HEC_INDEX=o11y_alerts
export SPLUNK_HEC_INSECURE=true

./scripts/push-demo-events.sh trigger checkout
```

After students review the ITSI episode and glass table, clear it:

```bash
./scripts/push-demo-events.sh clear checkout
```

## Incident Review

In the incident notes, capture:

- Which business transaction was impacted?
- Which detector fired first?
- Which technical service was the likely root cause?
- What did ITSI show that APM alone did not?
- What did APM show that ITSI alone did not?
- What service dependency or KPI weighting would you change before using this model in production?
