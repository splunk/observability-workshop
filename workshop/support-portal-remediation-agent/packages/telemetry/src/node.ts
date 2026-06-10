import { SpanStatusCode, trace } from "@opentelemetry/api";
import { deploymentEnvironment, serviceNamespace } from "./config";

export type NodeTelemetryConfig = {
  serviceName: string;
  endpoint?: string;
};

export function buildNodeTelemetryConfig(config: NodeTelemetryConfig) {
  return {
    serviceName: config.serviceName,
    serviceNamespace,
    deploymentEnvironment,
    otlpEndpoint: config.endpoint ?? process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? "http://localhost:14318"
  };
}

export function telemetryLogLabel(serviceName: string) {
  return `[telemetry:${serviceName}]`;
}

export function annotateCurrentSpan(attributes: Record<string, string | number | boolean | string[]>) {
  const span = trace.getActiveSpan();
  if (!span) {
    return;
  }

  for (const [key, value] of Object.entries(attributes)) {
    span.setAttribute(key, value);
  }
}

export function annotateServerEntrySpan(config: {
  method: string;
  route?: string;
  transaction?: string;
  attributes?: Record<string, string | number | boolean | string[]>;
}) {
  const span = trace.getActiveSpan();
  if (!span) {
    return;
  }

  const route = config.route?.trim();
  if (route) {
    span.setAttribute("http.route", route);
    span.updateName(`${config.method} ${route}`);
  }

  if (config.transaction) {
    span.setAttribute("app.business_transaction", config.transaction);
  }

  if (config.attributes) {
    annotateCurrentSpan(config.attributes);
  }
}

export async function runInSpan<T>(
  name: string,
  attributes: Record<string, string | number | boolean | string[]> | undefined,
  fn: () => Promise<T>
) {
  const tracer = trace.getTracer("ibobs-demo");
  return tracer.startActiveSpan(name, async (span) => {
    if (attributes) {
      annotateCurrentSpan(attributes);
    }

    try {
      const result = await fn();
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error) {
      span.recordException(error as Error);
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: error instanceof Error ? error.message : "Unknown span failure"
      });
      throw error;
    } finally {
      span.end();
    }
  });
}
