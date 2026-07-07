import express from 'express';
import { trace, SpanKind, SpanStatusCode } from '@opentelemetry/api';

const app = express();
app.use(express.json());

const port = Number(process.env.PORT || 3007);
const catalogUrl = process.env.CATALOG_API_URL || 'http://catalog-api:3002';
const gatewayUrl = process.env.GATEWAY_URL || 'http://gateway:80';
const paymentGatewayUrl = process.env.PAYMENT_GATEWAY_URL || 'http://payment-gateway:3004';
const tracer = trace.getTracer('frontend-api');

function forwardTraceHeaders(incoming) {
  return {
    traceparent: incoming.traceparent ?? '',
    tracestate: incoming.tracestate ?? '',
    baggage: incoming.baggage ?? '',
  };
}

app.get('/health', (_req, res) => {
  res.json({
    status: 'ok',
    service: 'frontend-api',
    stage: 'bff',
  });
});

app.get('/api/catalog', async (req, res) => {
  tracer.startActiveSpan(
    'frontend-api.fetch_catalog',
    { kind: SpanKind.SERVER },
    async (span) => {
      try {
        span.setAttribute('http.route', '/api/catalog');
        span.setAttribute('upstream.catalog', catalogUrl);

        const response = await tracer.startActiveSpan(
          'frontend-api.catalog_upstream',
          { kind: SpanKind.CLIENT },
          async (upstreamSpan) => {
            try {
              const upstream = await fetch(`${catalogUrl}/products`, {
                headers: forwardTraceHeaders(req.headers),
              });
              upstreamSpan.setAttribute('http.status_code', upstream.status);
              return upstream;
            } finally {
              upstreamSpan.end();
            }
          },
        );

        const data = await response.json();
        res.status(response.status).json(data);
      } catch (error) {
        span.recordException(error);
        span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
        res.status(502).json({ error: 'Catalog service unavailable' });
      } finally {
        span.end();
      }
    },
  );
});

app.post('/api/purchases', async (req, res) => {
  const { productId, quantity = 1, customerEmail } = req.body ?? {};

  if (!productId || !customerEmail) {
    res.status(400).json({ error: 'productId and customerEmail are required' });
    return;
  }

  tracer.startActiveSpan(
    'frontend-api.purchase_checkout',
    { kind: SpanKind.SERVER },
    async (span) => {
      try {
        span.setAttribute('purchase.product_id', productId);
        span.setAttribute('purchase.quantity', Number(quantity));
        span.setAttribute('http.route', '/api/purchases');

        const productResponse = await tracer.startActiveSpan(
          'frontend-api.validate_product',
          { kind: SpanKind.CLIENT },
          async (catalogSpan) => {
            try {
              const response = await fetch(`${catalogUrl}/products/${productId}`, {
                headers: forwardTraceHeaders(req.headers),
              });
              catalogSpan.setAttribute('http.status_code', response.status);
              return response;
            } finally {
              catalogSpan.end();
            }
          },
        );

        if (!productResponse.ok) {
          res.status(404).json({ error: 'Product not found' });
          return;
        }

        const orderResponse = await tracer.startActiveSpan(
          'frontend-api.submit_order',
          { kind: SpanKind.CLIENT },
          async (orderSpan) => {
            try {
              orderSpan.setAttribute('upstream.gateway', gatewayUrl);
              const response = await fetch(`${gatewayUrl}/api/orders`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  ...forwardTraceHeaders(req.headers),
                },
                body: JSON.stringify({
                  productId,
                  quantity,
                  customerEmail,
                }),
              });
              orderSpan.setAttribute('http.status_code', response.status);
              return response;
            } finally {
              orderSpan.end();
            }
          },
        );

        const orderBody = await orderResponse.json();
        if (!orderResponse.ok) {
          res.status(orderResponse.status).json(orderBody);
          return;
        }

        const order = orderBody.order;
        span.setAttribute('order.id', order.orderId);
        span.setAttribute('order.total', order.total);

        const paymentResponse = await tracer.startActiveSpan(
          'frontend-api.submit_payment',
          { kind: SpanKind.CLIENT },
          async (paymentSpan) => {
            try {
              paymentSpan.setAttribute('upstream.payment_gateway', paymentGatewayUrl);
              paymentSpan.setAttribute('payment.order_id', order.orderId);

              const response = await fetch(`${paymentGatewayUrl}/payments`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  ...forwardTraceHeaders(req.headers),
                },
                body: JSON.stringify(order),
              });
              paymentSpan.setAttribute('http.status_code', response.status);
              return response;
            } finally {
              paymentSpan.end();
            }
          },
        );

        const paymentBody = await paymentResponse.json();
        if (!paymentResponse.ok) {
          res.status(paymentResponse.status).json(paymentBody);
          return;
        }

        res.status(202).json({
          message: 'Purchase complete — order placed and payment submitted for fulfillment',
          order,
          payment: paymentBody.payment,
        });
      } catch (error) {
        span.recordException(error);
        span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
        res.status(500).json({ error: 'Purchase failed' });
      } finally {
        span.end();
      }
    },
  );
});

app.listen(port, () => {
  console.log(`frontend-api listening on port ${port}`);
  console.log(`  catalog path:  ${catalogUrl}`);
  console.log(`  order path:    ${gatewayUrl}/api/orders (edge gateway)`);
  console.log(`  payment path:  ${paymentGatewayUrl}/payments (payment gateway)`);
});
