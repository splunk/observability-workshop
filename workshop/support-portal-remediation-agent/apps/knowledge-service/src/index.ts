import cors from "@fastify/cors";
import { metrics } from "@opentelemetry/api";
import Fastify from "fastify";
import { mkdir, readdir, rm, stat, statfs, writeFile } from "node:fs/promises";
import { join } from "node:path";
import { performance } from "node:perf_hooks";
import { defaultPorts, localServicePort } from "@ibobs/runtime-config";
import { BUSINESS_TRANSACTIONS } from "@ibobs/shared-types";
import {
  annotateServerEntrySpan,
  annotateCurrentSpan,
  buildNodeTelemetryConfig,
  buildTelemetryAttributes,
  createServiceLogger,
  initSplunkNodeTelemetry,
  runInSpan
} from "@ibobs/telemetry";

export const knowledgeService = {
  name: "claims-knowledge",
  supportsTransactions: [
    BUSINESS_TRANSACTIONS.customerSupportResponse,
    BUSINESS_TRANSACTIONS.knowledgeArticleSearch,
    BUSINESS_TRANSACTIONS.legacyCustomerSupportResponse,
    BUSINESS_TRANSACTIONS.legacyKnowledgeArticleSearch
  ],
  telemetry: buildTelemetryAttributes(BUSINESS_TRANSACTIONS.knowledgeArticleSearch),
  failureModes: ["cache-disk-pressure"]
};

type ScenarioMode = "healthy" | "cache-disk-pressure";
type CacheStatus = {
  path: string;
  totalBytes: number;
  freeBytes: number;
  usedBytes: number;
  usedPercent: number;
  filesystemTotalBytes: number;
  filesystemFreeBytes: number;
  filesystemUsedBytes: number;
  filesystemUsedPercent: number;
};

let activeScenario: ScenarioMode = "healthy";
const cacheDirectory =
  process.env.CLAIMS_KNOWLEDGE_CACHE_DIR ??
  process.env.SUPPORT_KNOWLEDGE_CACHE_DIR ??
  "/tmp/ciscolive26-claims-knowledge-cache";
const cacheFillTargetPercent = Number(
  process.env.CLAIMS_KNOWLEDGE_CACHE_FILL_PERCENT ??
    process.env.SUPPORT_KNOWLEDGE_CACHE_FILL_PERCENT ??
    "92"
);
const cacheBlockBytes = Number(
  process.env.CLAIMS_KNOWLEDGE_CACHE_BLOCK_BYTES ??
    process.env.SUPPORT_KNOWLEDGE_CACHE_BLOCK_BYTES ??
    1024 * 1024
);
const cacheQuotaBytes = Number(
  process.env.CLAIMS_KNOWLEDGE_CACHE_QUOTA_BYTES ??
    process.env.SUPPORT_KNOWLEDGE_CACHE_QUOTA_BYTES ??
    128 * 1024 * 1024
);
const cacheMetricMountpoint = process.env.SPLUNK_CACHE_MOUNTPOINT ?? "/var/cache/claims-knowledge";
const evidenceMetricSource = process.env.SPLUNK_EVIDENCE_METRIC_SOURCE ?? "claims-knowledge-evidence";
const cacheUtilizationMetricName =
  process.env.CLAIMS_KNOWLEDGE_CACHE_UTILIZATION_METRIC ?? "claims_knowledge.cache.utilization";
const claimStatusLatencyMetricName =
  process.env.CLAIMS_KNOWLEDGE_CLAIM_STATUS_LATENCY_METRIC ?? "claims_knowledge.claim_status.latency_ms";
const claimStatusTransactions = new Set<string>([
  BUSINESS_TRANSACTIONS.customerSupportResponse,
  BUSINESS_TRANSACTIONS.legacyCustomerSupportResponse
]);
let cacheMetricsRegistered = false;
let directMetricPublisherStarted = false;
let latestCacheStatus: CacheStatus | undefined;
let lastClaimStatusLatencyMs = 0;

function defaultCacheStatusSnapshot(): CacheStatus {
  return {
    path: cacheDirectory,
    totalBytes: cacheQuotaBytes,
    freeBytes: cacheQuotaBytes,
    usedBytes: 0,
    usedPercent: 0,
    filesystemTotalBytes: 0,
    filesystemFreeBytes: 0,
    filesystemUsedBytes: 0,
    filesystemUsedPercent: 0
  };
}

function metricDimensions(extra: Record<string, string> = {}) {
  return {
    "deployment.environment": process.env.DEPLOYMENT_ENVIRONMENT ?? "demo",
    "service.name": knowledgeService.name,
    "service.namespace": process.env.OTEL_SERVICE_NAMESPACE ?? "ibobs2002",
    "service.instance.id": process.env.INSTANCE ?? "student-001",
    "host.name": process.env.INSTANCE ?? "student-001",
    "demo.metric_source": evidenceMetricSource,
    ...extra
  };
}

async function publishSplunkMetricSnapshot(cache: CacheStatus, latencyMs: number) {
  const accessToken = process.env.SPLUNK_ACCESS_TOKEN;
  const realm = process.env.SPLUNK_REALM;
  if (!accessToken || !realm) {
    return;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 1500);
  const timestamp = Date.now();

  try {
    await fetch(process.env.SPLUNK_INGEST_URL ?? `https://ingest.${realm}.signalfx.com/v2/datapoint`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-sf-token": accessToken
      },
      body: JSON.stringify({
        gauge: [
          {
            metric: cacheUtilizationMetricName,
            value: cache.usedPercent,
            timestamp,
            dimensions: metricDimensions({
              mountpoint: cacheMetricMountpoint,
              "cache.path": cacheDirectory
            })
          },
          {
            metric: claimStatusLatencyMetricName,
            value: latencyMs,
            timestamp,
            dimensions: metricDimensions({
              "app.business_transaction": BUSINESS_TRANSACTIONS.customerSupportResponse
            })
          }
        ]
      }),
      signal: controller.signal
    });
  } catch {
    // Metric publication is best-effort; the request path must stay deterministic for the demo.
  } finally {
    clearTimeout(timeout);
  }
}

function publishLatestMetricSnapshot() {
  void publishSplunkMetricSnapshot(latestCacheStatus ?? defaultCacheStatusSnapshot(), lastClaimStatusLatencyMs);
}

function startDirectMetricPublisher() {
  if (directMetricPublisherStarted) {
    return;
  }
  directMetricPublisherStarted = true;
  const interval = setInterval(publishLatestMetricSnapshot, 5000);
  interval.unref?.();
}

async function cachePressureBytes() {
  await mkdir(cacheDirectory, { recursive: true });
  const entries = await readdir(cacheDirectory, { withFileTypes: true });
  const fileSizes = await Promise.all(
    entries
      .filter((entry) => entry.name.startsWith("cache-pressure-") && entry.isFile())
      .map(async (entry) => stat(join(cacheDirectory, entry.name)).then((file) => file.size))
  );
  return fileSizes.reduce((total, size) => total + size, 0);
}

async function cacheStatus() {
  await mkdir(cacheDirectory, { recursive: true });
  const stats = await statfs(cacheDirectory);
  const filesystemTotalBytes = Number(stats.blocks) * Number(stats.bsize);
  const filesystemFreeBytes = Number(stats.bavail) * Number(stats.bsize);
  const filesystemUsedBytes = Math.max(filesystemTotalBytes - filesystemFreeBytes, 0);
  const filesystemUsedPercent =
    filesystemTotalBytes > 0 ? Math.round((filesystemUsedBytes / filesystemTotalBytes) * 1000) / 10 : 0;
  const totalBytes = cacheQuotaBytes > 0 ? cacheQuotaBytes : filesystemTotalBytes;
  const usedBytes = Math.min(await cachePressureBytes(), totalBytes);
  const freeBytes = Math.max(totalBytes - usedBytes, 0);
  const usedPercent = totalBytes > 0 ? Math.round((usedBytes / totalBytes) * 1000) / 10 : 0;

  const status = {
    path: cacheDirectory,
    totalBytes,
    freeBytes,
    usedBytes,
    usedPercent,
    filesystemTotalBytes,
    filesystemFreeBytes,
    filesystemUsedBytes,
    filesystemUsedPercent
  };
  latestCacheStatus = status;
  return status;
}

async function clearDemoCache() {
  await mkdir(cacheDirectory, { recursive: true });
  const entries = await readdir(cacheDirectory, { withFileTypes: true });
  await Promise.all(
    entries
      .filter((entry) => entry.name.startsWith("cache-pressure-"))
      .map((entry) => rm(join(cacheDirectory, entry.name), { recursive: true, force: true }))
  );
}

async function createCachePressure() {
  await clearDemoCache();
  const block = Buffer.alloc(cacheBlockBytes, "x");
  let status = await cacheStatus();
  const maxBlocks = Number(
    process.env.CLAIMS_KNOWLEDGE_CACHE_MAX_BLOCKS ??
      process.env.SUPPORT_KNOWLEDGE_CACHE_MAX_BLOCKS ??
      "2048"
  );
  let blockIndex = 0;

  while (status.usedPercent < cacheFillTargetPercent && blockIndex < maxBlocks) {
    try {
      await writeFile(join(cacheDirectory, `cache-pressure-${String(blockIndex).padStart(4, "0")}.bin`), block);
    } catch (error) {
      if (error && typeof error === "object" && "code" in error && error.code === "ENOSPC") {
        break;
      }
      throw error;
    }
    blockIndex += 1;
    status = await cacheStatus();
  }

  return status;
}

async function maybeDelay(transaction: string) {
  if (activeScenario !== "cache-disk-pressure" || !claimStatusTransactions.has(transaction)) {
    return;
  }

  const status = await cacheStatus();
  const delayMs = status.usedPercent >= 85 ? 2200 : 900;
  await new Promise((resolve) => setTimeout(resolve, delayMs));
}

function knowledgeAttributes(transaction: string) {
  const pressureAffectsTransaction =
    activeScenario === "cache-disk-pressure" && claimStatusTransactions.has(transaction);

  return {
    "app.business_transaction": transaction,
    "app.scenario": activeScenario,
    "app.failure_mode": pressureAffectsTransaction ? "filesystem_pressure" : "none"
  };
}

function registerCacheUtilizationMetric() {
  if (cacheMetricsRegistered) {
    return;
  }
  cacheMetricsRegistered = true;

  const meter = metrics.getMeter("claims-knowledge-cache");
  const utilizationGauge = meter.createObservableGauge(cacheUtilizationMetricName, {
    description: "Synthetic claims knowledge cache quota utilization used by the workshop scenario."
  });
  const latencyGauge = meter.createObservableGauge(claimStatusLatencyMetricName, {
    description: "Last observed claims knowledge latency for the AI Claim Status transaction."
  });

  utilizationGauge.addCallback((observableResult) => {
    const status = latestCacheStatus ?? defaultCacheStatusSnapshot();
    observableResult.observe(status.usedPercent, {
      "deployment.environment": process.env.DEPLOYMENT_ENVIRONMENT ?? "demo",
      "service.name": knowledgeService.name,
      "service.namespace": process.env.OTEL_SERVICE_NAMESPACE ?? "ibobs2002",
      "service.instance.id": process.env.INSTANCE ?? "student-001",
      "host.name": process.env.INSTANCE ?? "student-001",
      mountpoint: cacheMetricMountpoint,
      "cache.path": cacheDirectory,
      "demo.metric_source": evidenceMetricSource
    });
  });
  latencyGauge.addCallback((observableResult) => {
    observableResult.observe(lastClaimStatusLatencyMs, {
      "deployment.environment": process.env.DEPLOYMENT_ENVIRONMENT ?? "demo",
      "service.name": knowledgeService.name,
      "service.namespace": process.env.OTEL_SERVICE_NAMESPACE ?? "ibobs2002",
      "service.instance.id": process.env.INSTANCE ?? "student-001",
      "host.name": process.env.INSTANCE ?? "student-001",
      "app.business_transaction": BUSINESS_TRANSACTIONS.customerSupportResponse,
      "demo.metric_source": evidenceMetricSource
    });
  });
}

export function buildServer() {
  const app = Fastify({ loggerInstance: createServiceLogger(knowledgeService.name) });
  void buildNodeTelemetryConfig({ serviceName: knowledgeService.name });
  registerCacheUtilizationMetric();
  startDirectMetricPublisher();
  void cacheStatus().then(() => publishLatestMetricSnapshot());
  void app.register(cors, { origin: true });
  app.addHook("preHandler", async (request) => {
    const routePath = request.routeOptions.url;
    annotateServerEntrySpan({
      method: request.method,
      route: routePath
    });
    request.log.info(
      {
        http: { method: request.method, url: request.url },
        params: request.params,
        query: request.query,
        body: request.body
      },
      "request received"
    );
  });
  app.addHook("onResponse", async (request, reply) => {
    request.log.info(
      {
        http: { method: request.method, url: request.url, status_code: reply.statusCode }
      },
      "request completed"
    );
  });

  app.get("/knowledge/health", async () => ({ status: "ok", service: knowledgeService.name }));
  app.get("/knowledge/cache/status", async () => cacheStatus());
  app.get("/knowledge/scenario", async () => ({
    activeScenario,
    cache: await cacheStatus()
  }));
  app.post("/knowledge/scenario", async (request) => {
    activeScenario = ((request.body as { mode?: ScenarioMode }).mode ?? "healthy") as ScenarioMode;
    lastClaimStatusLatencyMs = 0;
    const cache =
      activeScenario === "cache-disk-pressure"
        ? await createCachePressure()
        : await clearDemoCache().then(() => cacheStatus());
    publishLatestMetricSnapshot();
    request.log.info({ activeScenario, cache }, "knowledge scenario updated");
    return {
      activeScenario,
      cache
    };
  });
  app.post("/knowledge/query", async (request, reply) => {
    const startedAt = performance.now();
    const transaction = (request.body as { transaction?: string }).transaction ?? BUSINESS_TRANSACTIONS.knowledgeArticleSearch;
    const recordClaimStatusLatency = () => {
      if (claimStatusTransactions.has(transaction)) {
        lastClaimStatusLatencyMs = Math.round((performance.now() - startedAt) * 10) / 10;
      }
    };
    request.log.info({ knowledgeRequest: request.body, transaction, activeScenario }, "knowledge query received");
    const telemetry = {
      ...buildTelemetryAttributes(transaction),
      ...knowledgeAttributes(transaction)
    };
    annotateCurrentSpan(telemetry);
    await runInSpan("knowledge.apply_cache_pressure", telemetry, () => maybeDelay(transaction));

    const cache = await cacheStatus();
    const cacheFullForSupport =
      activeScenario === "cache-disk-pressure" &&
      claimStatusTransactions.has(transaction) &&
      cache.usedPercent >= 98;

    if (cacheFullForSupport) {
      recordClaimStatusLatency();
      publishLatestMetricSnapshot();
      reply.code(503);
      request.log.warn({ transaction, activeScenario, cache }, "knowledge cache volume is full");
      return {
        transaction,
        telemetry,
        scenario: activeScenario,
        error: "Claims knowledge cache volume is full for the AI claim status workflow."
      };
    }

    recordClaimStatusLatency();
    publishLatestMetricSnapshot();
    request.log.info({ transaction, activeScenario, cache }, "knowledge query served");

    return {
      transaction,
      telemetry,
      scenario: activeScenario,
      answer:
        claimStatusTransactions.has(transaction)
          ? "Generated claim status response using the claims knowledge service."
          : "Claims FAQ lookup completed."
    };
  });

  return app;
}

if (process.env.NODE_ENV !== "test") {
  initSplunkNodeTelemetry(knowledgeService.name);
  const port = localServicePort(process.env, "KNOWLEDGE_SERVICE_PORT", defaultPorts.knowledgeService);
  const server = buildServer();
  server.log.info({ knowledgeService, cacheDirectory, cacheQuotaBytes }, "knowledge-service scaffold ready");
  server.listen({ port, host: "0.0.0.0" }).catch((error) => {
    server.log.error(error);
    process.exit(1);
  });
}
