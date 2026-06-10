---
title: 4. Auto and Custom Instrumentation
linkTitle: 4. Instrumentation
weight: 4
---

Splunk RUM gives you useful browser telemetry before you write product-specific instrumentation. DXA becomes more useful when you combine that automatic coverage with a small number of custom workflow spans that describe the actions your team actually cares about.

## Auto-instrumentation examples

The workshop RUM snippet enables browser auto-instrumentation in `SplunkRum.init()`:

```javascript
SplunkRum.init({
  instrumentations: {
    visibility: true,
    interactions: {
      eventNames: SplunkRum.DEFAULT_AUTO_INSTRUMENTED_EVENT_NAMES.concat([
        "change",
        "submit"
      ])
    }
  },
  spaMetrics: true
});
```

With this configuration, the browser agent can collect:

| Automatic signal | Demo action that creates it | How DXA can use it |
| --- | --- | --- |
| Page load timing | Open `http://localhost:8088` | Baseline user experience and page performance. |
| Resource timing | Click **Load recommendations** | Analyze backend or asset latency in RUM. |
| User interaction spans | Click **View product**, **Add to cart**, or **Begin checkout** | Build click-based event definitions. |
| Form and change interactions | Change **Shipping method** or submit checkout | Track checkout form behavior. |
| SPA route changes | Product, cart, checkout, and completion route updates | Define journey steps by URL pattern. |
| JavaScript errors | Click **Trigger JavaScript error** | Segment affected users and inspect sessions. |

Auto-instrumentation is the right starting point because it is broad, consistent, and low-maintenance. It is not a substitute for naming the business actions that matter to your product.

## Custom instrumentation examples

The demo app also contains product-specific custom spans in:

```text
workshop/rum-nginx-session-replay/site/index.html
```

Those spans use the OpenTelemetry API registered by the Splunk RUM browser agent. In a bundled application, the same pattern uses `@opentelemetry/api`:

```javascript
import { trace } from "@opentelemetry/api";

const span = trace.getTracer("checkout").startSpan("checkout.submit", {
  attributes: {
    "workflow.name": "checkout.submit",
    "checkout.cart_items": cartCount,
    "checkout.shipping_method": shippingMethod
  }
});

try {
  submitOrder();
} finally {
  span.end();
}
```

For the CDN-based lab, the demo page reads the registered browser API from the global OpenTelemetry symbol and starts spans only when the API is available:

```javascript
function startCustomWorkflowSpan(name, attributes) {
  var api = window[Symbol.for("opentelemetry.js.api.1")];
  if (!api || !api.trace) {
    return null;
  }

  return api.trace.getTracer("dxa-rum-workshop").startSpan(name, {
    attributes: Object.assign({ "workflow.name": name }, attributes)
  });
}
```

The app uses this helper for:

| Custom span | Trigger | Example attributes |
| --- | --- | --- |
| `product.view` | **View product** | `product.id`, `product.tier` |
| `cart.add` | **Add to cart** | `product.id`, `cart.item_count` |
| `recommendations.load` | **Load recommendations** | `recommendations.source`, `recommendations.count` |
| `checkout.start` | **Begin checkout** | `product.id`, `cart.item_count` |
| `checkout.submit` | **Submit order** | `checkout.shipping_method`, `cart.item_count` |
| `checkout.error` | **Trigger JavaScript error** | `error.demo`, `cart.item_count` |

{{% notice title="Attribute hygiene" style="warning" %}}
Custom spans should use stable, low-cardinality, non-sensitive attributes. Use product IDs, release versions, feature names, and workflow names. Do not put email addresses, free-form support notes, card data, or tokens into span attributes.
{{% /notice %}}

{{< tabs >}}
{{% tab title="Question" %}}
When should you add custom instrumentation instead of relying on automatic RUM spans?
{{% /tab %}}
{{% tab title="Answer" %}}
Add custom spans when the automatic event does not carry enough product meaning. A generic click tells you that a button was clicked; a `checkout.submit` workflow span tells every team that a user attempted to complete checkout and gives you controlled attributes for segmentation and analysis.
{{% /tab %}}
{{< /tabs >}}
