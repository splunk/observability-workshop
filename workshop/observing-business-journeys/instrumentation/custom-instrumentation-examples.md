# Custom Instrumentation Examples

Use custom instrumentation when the application knows the business context better
than the collector can infer it from service names or routes.

Preferred production attributes:

| Attribute | Example |
|---|---|
| `business.application` | `astronomy-shop` |
| `business.transaction` | `Complete Checkout` |
| `business.capability` | `checkout` |
| `business.criticality` | `critical` |
| `business.owner` | `revenue-operations` |

## Python

```python
from opentelemetry import trace

tracer = trace.get_tracer("checkout")

def checkout(order):
    with tracer.start_as_current_span("checkout.submit") as span:
        span.set_attribute("business.application", "astronomy-shop")
        span.set_attribute("business.transaction", "Complete Checkout")
        span.set_attribute("business.capability", "checkout")
        span.set_attribute("business.criticality", "critical")
        span.set_attribute("business.owner", "revenue-operations")
        span.set_attribute("order.value", order.total)

        return submit_order(order)
```

## Node.js

```javascript
const { trace } = require("@opentelemetry/api");

const tracer = trace.getTracer("cart");

async function addToCart(req, res) {
  await tracer.startActiveSpan("cart.add_item", async (span) => {
    try {
      span.setAttribute("business.application", "astronomy-shop");
      span.setAttribute("business.transaction", "Manage Cart");
      span.setAttribute("business.capability", "cart");
      span.setAttribute("business.criticality", "high");
      span.setAttribute("business.owner", "digital-commerce");
      span.setAttribute("cart.item_count", req.body.quantity);

      await cartService.add(req.body);
      res.status(204).end();
    } catch (err) {
      span.recordException(err);
      throw err;
    } finally {
      span.end();
    }
  });
}
```

## Java

```java
import io.opentelemetry.api.trace.Span;

public CheckoutResult submitOrder(Order order) {
    Span span = Span.current();
    span.setAttribute("business.application", "astronomy-shop");
    span.setAttribute("business.transaction", "Complete Checkout");
    span.setAttribute("business.capability", "checkout");
    span.setAttribute("business.criticality", "critical");
    span.setAttribute("business.owner", "revenue-operations");
    span.setAttribute("order.value", order.total());

    return checkoutService.submit(order);
}
```

## Collector Transform Fallback

Collector transforms are useful when you cannot change application code yet. The
workshop collector rules add the same attributes from route and service context,
but this is less precise than app-owned instrumentation.

Use collector transforms for:

- Legacy services where code changes are slow.
- Temporary workshop or migration bridges.
- Normalizing inconsistent service names.

Use custom app instrumentation for:

- Real transaction names.
- Order value or customer segment context.
- Business owner and criticality metadata.
- Low-cardinality fields that will feed APM MetricSets and ITSI.
