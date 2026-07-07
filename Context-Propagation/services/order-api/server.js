import express from 'express';
import { trace, SpanKind, SpanStatusCode } from '@opentelemetry/api';
import { getActiveTraceIds } from './shared/propagation.js';

const app = express();
app.use(express.json());

const port = Number(process.env.PORT || 3001);
const catalogUrl = process.env.CATALOG_API_URL || 'http://catalog-api:3002';
const tracer = trace.getTracer('order-api');

app.get('/health', (_req, res) => {
  res.json({
    status: 'ok',
    service: 'order-api',
    stage: 'order',
  });
});

app.post('/api/orders', async (req, res) => {
  const { productId, quantity = 1, customerEmail } = req.body ?? {};

  if (!productId || !customerEmail) {
    res.status(400).json({ error: 'productId and customerEmail are required' });
    return;
  }

  tracer.startActiveSpan(
    'order.create_order',
    { kind: SpanKind.SERVER },
    async (span) => {
      try {
        span.setAttribute('order.product_id', productId);
        span.setAttribute('order.quantity', Number(quantity));

        const productResponse = await tracer.startActiveSpan(
          'order.validate_product',
          { kind: SpanKind.CLIENT },
          async (catalogSpan) => {
            try {
              const response = await fetch(`${catalogUrl}/products/${productId}`);
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

        const { product } = await productResponse.json();
        const order = {
          orderId: `ORD-${Date.now()}`,
          productId,
          productName: product.name,
          quantity: Number(quantity),
          total: Number((product.price * Number(quantity)).toFixed(2)),
          customerEmail,
          createdAt: new Date().toISOString(),
        };

        const traceIds = getActiveTraceIds();
        order.requestTraceId = traceIds.traceId;

        span.setAttribute('order.id', order.orderId);
        span.setAttribute('order.total', order.total);

        res.status(201).json({
          message: 'Order created',
          order,
          traceHint: traceIds,
        });
      } catch (error) {
        span.recordException(error);
        span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
        res.status(500).json({ error: 'Failed to create order' });
      } finally {
        span.end();
      }
    },
  );
});

app.listen(port, () => {
  console.log(`order-api listening on port ${port}`);
});
