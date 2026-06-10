import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { isSpanContextValid, trace } from "@opentelemetry/api";
import pino from "pino";
import { deploymentEnvironment, serviceNamespace } from "./config";

function repoRoot() {
  return resolve(dirname(fileURLToPath(import.meta.url)), "../../..");
}

export function resolveLogDirectory() {
  return process.env.IBOBS_LOG_DIR ?? resolve(repoRoot(), "var/log");
}

export function resolveLogFile(serviceName: string) {
  const safeServiceName = serviceName.replace(/[^a-z0-9-_]+/gi, "-").toLowerCase();
  return resolve(resolveLogDirectory(), `${safeServiceName}.log`);
}

function activeTraceContext() {
  const span = trace.getActiveSpan();
  if (!span) {
    return {};
  }

  const spanContext = span.spanContext();
  if (!isSpanContextValid(spanContext)) {
    return {};
  }

  return {
    trace_id: spanContext.traceId,
    span_id: spanContext.spanId,
    trace_flags: spanContext.traceFlags.toString(16).padStart(2, "0")
  };
}

export function createServiceLogger(serviceName: string) {
  const logFile = resolveLogFile(serviceName);
  mkdirSync(dirname(logFile), { recursive: true });

  return pino(
    {
      level: process.env.LOG_LEVEL ?? "info",
      base: undefined,
      messageKey: "message",
      timestamp: pino.stdTimeFunctions.isoTime,
      mixin() {
        return {
          "service.name": serviceName,
          "service.namespace": serviceNamespace,
          "deployment.environment": deploymentEnvironment,
          ...activeTraceContext()
        };
      }
    },
    pino.transport({
      targets: [
        {
          target: "pino/file",
          level: process.env.LOG_LEVEL ?? "info",
          options: { destination: 1, mkdir: true }
        },
        {
          target: "pino/file",
          level: process.env.LOG_LEVEL ?? "info",
          options: { destination: logFile, mkdir: true }
        }
      ]
    })
  );
}
