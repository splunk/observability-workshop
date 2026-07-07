import express from 'express';
import amqp from 'amqplib';
import { context, trace, SpanKind, SpanStatusCode } from '@opentelemetry/api';
import { extractTraceContext } from './shared/propagation.js';

const rabbitUrl = process.env.RABBITMQ_URL || 'amqp://guest:guest@rabbitmq:5672';
const fulfillmentQueue = process.env.FULFILLMENT_QUEUE || 'cosmic-fulfillment';
const healthPort = Number(process.env.PORT || 3006);
const tracer = trace.getTracer('fulfillment-worker');

const app = express();

function isMessagingPropagationEnabled() {
  return tracer.startActiveSpan('health.propagation_probe', (outer) => {
    try {
      const fakeTraceId = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
      const parent = extractTraceContext({
        traceparent: `00-${fakeTraceId}-bbbbbbbbbbbbbbbb-01`,
      });

      let linked = false;
      context.with(parent, () => {
        const inner = trace.getActiveSpan();
        linked = inner?.spanContext()?.traceId === fakeTraceId;
      });
      return linked;
    } finally {
      outer.end();
    }
  });
}

app.get('/health', (_req, res) => {
  res.json({
    status: 'ok',
    service: 'fulfillment-worker',
    stage: 'fulfillment',
    propagation: isMessagingPropagationEnabled(),
  });
});

app.listen(healthPort, () => {
  console.log(`fulfillment-worker health endpoint on port ${healthPort}`);
});

async function processFulfillment(job, msg) {
  const parentContext = extractTraceContext(msg.properties.headers ?? {});

  return context.with(parentContext, () =>
    tracer.startActiveSpan(
      'fulfillment.process_job',
      {
        kind: SpanKind.CONSUMER,
        attributes: {
          'messaging.system': 'rabbitmq',
          'messaging.destination.name': fulfillmentQueue,
          'messaging.operation': 'process',
          'order.id': job.orderId,
          'payment.id': job.paymentId,
          'messaging.context_propagated': isMessagingPropagationEnabled(),
        },
      },
      async (span) => {
        try {
          await tracer.startActiveSpan('fulfillment.validate_inventory', async (s) => {
            await sleep(120);
            s.setAttribute('order.product_id', job.productId);
            s.end();
          });

          await tracer.startActiveSpan('fulfillment.prepare_shipment', async (s) => {
            await sleep(180);
            s.setAttribute('order.total', job.total);
            s.end();
          });

          await tracer.startActiveSpan('fulfillment.send_confirmation', async (s) => {
            await sleep(80);
            s.setAttribute('customer.email_domain', job.customerEmail?.split('@')[1] ?? 'unknown');
            s.end();
          });

          console.log(
            `Fulfilled order ${job.orderId} (payment ${job.paymentId}) for ${job.productName}`,
          );
          span.setStatus({ code: SpanStatusCode.OK });
        } catch (error) {
          span.recordException(error);
          span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
          throw error;
        } finally {
          span.end();
        }
      },
    ),
  );
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function startConsumer() {
  const connection = await amqp.connect(rabbitUrl);
  const channel = await connection.createChannel();
  await channel.assertQueue(fulfillmentQueue, { durable: true });
  channel.prefetch(1);

  console.log(`Consuming from queue: ${fulfillmentQueue}`);
  console.log(
    `RabbitMQ context propagation: ${isMessagingPropagationEnabled() ? 'ENABLED' : 'DISABLED (workshop broken state)'}`,
  );

  channel.consume(fulfillmentQueue, async (msg) => {
    if (!msg) {
      return;
    }

    try {
      const job = JSON.parse(msg.content.toString());
      await processFulfillment(job, msg);
      channel.ack(msg);
    } catch (error) {
      console.error('Fulfillment processing failed', error);
      channel.nack(msg, false, false);
    }
  });
}

startConsumer().catch((error) => {
  console.error('Failed to start fulfillment-worker', error);
  process.exit(1);
});
