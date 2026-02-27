---
title: 2. Generate Traffic
weight: 2
---

## Hit the Frontend

{{% notice title="Exercise" style="green" icon="running" %}}

Use curl to generate traffic:

``` bash
curl -s http://localhost:3000/create-order | python3 -m json.tool
```

{{% /notice %}}

You should see a JSON response like:

``` json
{
  "order": "confirmed",
  "payment": {
    "status": "success",
    "transaction_id": "txn-a1b2c3d4e5f6",
    "amount": 42
  }
}
```

The request flowed through all three services. But right now, nobody is watching.

## Look at the Code

Take a moment to inspect the source code and confirm there is zero instrumentation:

{{% notice title="Exercise" style="green" icon="running" %}}

``` bash
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/frontend/
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/order-processor/
grep -r "opentelemetry\|otel\|tracing\|instrument" ~/workshop/obi/02-obi-docker/payment-service/
```

{{% /notice %}}

All three commands return nothing. There are **zero tracing headers, zero SDKs, zero instrumentation** anywhere in the application code.
