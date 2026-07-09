import { context, propagation, trace } from '@opentelemetry/api';

/**
 * Inject W3C trace context into a carrier (HTTP headers or AMQP message headers).
 */
export function injectTraceHeaders(existingHeaders = {}) {
  const carrier = { ...existingHeaders };
  propagation.inject(context.active(), carrier, {
    set: (obj, key, value) => {
      obj[key] = value;
    },
  });
  return carrier;
}

/**
 * Extract W3C trace context from a carrier (HTTP headers or AMQP message headers).
 */
export function extractTraceContext(headers = {}) {
  return propagation.extract(context.active(), headers, {
    get: (carrier, key) => {
      const value = carrier[key];
      if (value === undefined || value === null) {
        return undefined;
      }
      return Array.isArray(value) ? value : [String(value)];
    },
    keys: (carrier) => Object.keys(carrier ?? {}),
  });
}

export function getActiveTraceIds() {
  const span = trace.getActiveSpan();
  if (!span) {
    return { traceId: null, spanId: null };
  }
  const ctx = span.spanContext();
  return { traceId: ctx.traceId, spanId: ctx.spanId };
}
