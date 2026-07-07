import express from 'express';
import { context, propagation, trace, SpanKind, SpanStatusCode } from '@opentelemetry/api';
import { suppressTracing } from '@opentelemetry/core';

const app = express();
app.use(express.json());

const port = Number(process.env.PORT || 3004);
const paymentApiUrl = process.env.PAYMENT_API_URL || 'http://payment-api:3005';
const tracer = trace.getTracer('payment-gateway');

/**
 * Build headers for the upstream payment-api request.
 * Step 08: add propagation.inject() here so payment-api continues the same trace.
 */
function buildUpstreamHeaders() {
  const headers = {
    'Content-Type': 'application/json',
  };

  // Step 08 — add these lines (see workshop/08-fix-payment-gateway-propagation.md):
  // propagation.inject(context.active(), headers, {
  //   set: (carrier, key, value) => {
  //     carrier[key] = value;
  //   },
  // });

  return headers;
}

function isProxyPropagationEnabled() {
  return tracer.startActiveSpan('health.propagation_probe', (span) => {
    try {
      const headers = buildUpstreamHeaders();
      return Boolean(headers.traceparent);
    } finally {
      span.end();
    }
  });
}

app.get('/health', (_req, res) => {
  res.json({
    status: 'ok',
    service: 'payment-gateway',
    stage: 'proxy',
    propagation: isProxyPropagationEnabled(),
  });
});

app.post('/payments', async (req, res) => {
  tracer.startActiveSpan(
    'payment-gateway.proxy_payment',
    { kind: SpanKind.SERVER },
    async (span) => {
      try {
        span.setAttribute('proxy.upstream', paymentApiUrl);
        span.setAttribute('proxy.trace_headers_forwarded', isProxyPropagationEnabled());

        const upstreamHeaders = buildUpstreamHeaders();
        const body = JSON.stringify(req.body);

        // Workshop broken state: suppresses auto-injected trace headers on upstream fetch.
        // Step 08: remove suppressTracing and use context.active() after adding inject above.
        const upstreamContext = suppressTracing(context.active());

        const upstreamResponse = await context.with(upstreamContext, () =>
          tracer.startActiveSpan(
            'payment-gateway.forward_to_payment_api',
            { kind: SpanKind.CLIENT },
            async (forwardSpan) => {
              try {
                forwardSpan.setAttribute('http.url', `${paymentApiUrl}/payments`);
                const response = await fetch(`${paymentApiUrl}/payments`, {
                  method: 'POST',
                  headers: upstreamHeaders,
                  body,
                });
                forwardSpan.setAttribute('http.status_code', response.status);
                return response;
              } finally {
                forwardSpan.end();
              }
            },
          ),
        );

        const responseBody = await upstreamResponse.text();
        res.status(upstreamResponse.status);
        res.set('Content-Type', upstreamResponse.headers.get('content-type') ?? 'application/json');
        res.send(responseBody);
      } catch (error) {
        span.recordException(error);
        span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
        res.status(502).json({ error: 'Payment service unavailable via gateway' });
      } finally {
        span.end();
      }
    },
  );
});

app.listen(port, () => {
  console.log(`payment-gateway listening on port ${port}`);
  console.log(
    `Trace header forwarding: ${isProxyPropagationEnabled() ? 'ENABLED' : 'DISABLED (workshop broken state)'}`,
  );
});
