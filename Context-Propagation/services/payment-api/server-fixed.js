import express from 'express';
import amqp from 'amqplib';
import { trace, SpanKind, SpanStatusCode } from '@opentelemetry/api';
import { getActiveTraceIds, injectTraceHeaders } from './shared/propagation.js';

const app = express();
app.use(express.json());

const port = Number(process.env.PORT || 3005);
const rabbitUrl = process.env.RABBITMQ_URL || 'amqp://guest:guest@rabbitmq:5672';
const fulfillmentQueue = process.env.FULFILLMENT_QUEUE || 'cosmic-fulfillment';
const tracer = trace.getTracer('payment-api');

let channel;
let connection;

async function connectRabbit() {
  connection = await amqp.connect(rabbitUrl);
  channel = await connection.createChannel();
  await channel.assertQueue(fulfillmentQueue, { durable: true });
  console.log(`Connected to RabbitMQ, queue: ${fulfillmentQueue}`);
}

/**
 * AMQP headers for fulfillment jobs.
 * Step 09: wrap the return value with injectTraceHeaders() so the worker can continue the trace.
 */
function buildFulfillmentMessageHeaders(order, payment) {
  return injectTraceHeaders({
    'x-order-id': order.orderId,
    'x-payment-id': payment.paymentId,
  });
}

function isMessagingPropagationEnabled() {
  return tracer.startActiveSpan('health.propagation_probe', (span) => {
    try {
      const headers = buildFulfillmentMessageHeaders(
        { orderId: 'probe' },
        { paymentId: 'probe' },
      );
      return Boolean(headers.traceparent);
    } finally {
      span.end();
    }
  });
}

app.get('/health', (_req, res) => {
  res.json({
    status: 'ok',
    service: 'payment-api',
    stage: 'payment',
    rabbitmq: Boolean(channel),
    propagation: isMessagingPropagationEnabled(),
  });
});

app.post('/payments', async (req, res) => {
  const order = req.body ?? {};

  if (!order.orderId || !order.customerEmail) {
    res.status(400).json({ error: 'Invalid payment payload' });
    return;
  }

  tracer.startActiveSpan(
    'payment.process_payment',
    { kind: SpanKind.SERVER },
    async (span) => {
      try {
        span.setAttribute('order.id', order.orderId);
        span.setAttribute('order.total', order.total ?? 0);

        const payment = {
          paymentId: `PAY-${Date.now()}`,
          orderId: order.orderId,
          amount: order.total,
          status: 'authorized',
          method: 'stellar-credits',
          processedAt: new Date().toISOString(),
        };

        await tracer.startActiveSpan('payment.authorize', async (authSpan) => {
          await sleep(100);
          authSpan.setAttribute('payment.amount', payment.amount);
          authSpan.end();
        });

        const fulfillmentJob = {
          ...order,
          paymentId: payment.paymentId,
          paymentStatus: payment.status,
        };

        await tracer.startActiveSpan(
          'payment.enqueue_fulfillment',
          { kind: SpanKind.PRODUCER },
          async (publishSpan) => {
            try {
              publishSpan.setAttribute('messaging.system', 'rabbitmq');
              publishSpan.setAttribute('messaging.destination.name', fulfillmentQueue);
              publishSpan.setAttribute('messaging.operation', 'publish');

              const headers = buildFulfillmentMessageHeaders(order, payment);

              channel.sendToQueue(
                fulfillmentQueue,
                Buffer.from(JSON.stringify(fulfillmentJob)),
                {
                  persistent: true,
                  contentType: 'application/json',
                  headers,
                },
              );

              publishSpan.setAttribute(
                'messaging.context_propagated',
                isMessagingPropagationEnabled(),
              );
            } finally {
              publishSpan.end();
            }
          },
        );

        const traceIds = getActiveTraceIds();
        res.status(202).json({
          message: 'Payment authorized — fulfillment queued',
          payment,
          traceHint: traceIds,
        });
      } catch (error) {
        span.recordException(error);
        span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
        res.status(500).json({ error: 'Payment processing failed' });
      } finally {
        span.end();
      }
    },
  );
});

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function start() {
  await connectRabbit();
  app.listen(port, () => {
    console.log(`payment-api listening on port ${port}`);
    console.log(
      `RabbitMQ context propagation: ${isMessagingPropagationEnabled() ? 'ENABLED' : 'DISABLED (workshop broken state)'}`,
    );
  });
}

start().catch((error) => {
  console.error('Failed to start payment-api', error);
  process.exit(1);
});

process.on('SIGTERM', async () => {
  await channel?.close().catch(() => {});
  await connection?.close().catch(() => {});
  process.exit(0);
});
