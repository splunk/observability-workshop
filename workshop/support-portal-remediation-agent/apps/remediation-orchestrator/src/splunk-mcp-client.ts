import {
  BUSINESS_TRANSACTIONS,
  type ApprovalEvidence,
  type DetectorWebhookPayload,
  type EvidenceMetricStatus
} from "@ibobs/shared-types";

type JsonObject = Record<string, unknown>;

export type SplunkMcpConfig = {
  enabled: boolean;
  url: string;
  accessToken: string;
  realm: string;
  authToken?: string;
  tenant?: string;
  timeoutMs: number;
};

export type SplunkMcpResource = {
  type: "alert" | "dependency" | "metric" | "service" | "trace";
  name: string;
  detail?: string;
  url?: string;
};

export type SplunkMcpEvidenceResult = {
  sources: string[];
  warnings: string[];
  affectedServices?: string[];
  suspectService?: string;
  p95LatencyMs?: number;
  errorRate?: number;
  affectedTransactions?: string[];
  recentChange?: string;
  likelyCause?: string;
  confidenceBand?: "low" | "medium" | "high";
  assistantSummary?: string;
  observabilityResources?: SplunkMcpResource[];
  traceIds?: string[];
  approvalEvidence?: ApprovalEvidence;
};

type EvidenceThresholds = {
  filesystemUtilization: number;
  apmLatencyMs: number;
  errorRatePercent: number;
};

type McpTool = {
  name: string;
  description?: string;
  inputSchema?: unknown;
};

type McpScope = {
  detectorId: string;
  detectorName: string;
  incidentId?: string;
  severity: DetectorWebhookPayload["severity"];
  service: string;
  environment: string;
  instance?: string;
  cacheMountpoint: string;
  cacheUtilizationMetric: string;
  claimStatusLatencyMetric: string;
  evidenceMetricSource: string;
  startTime: string;
  endTime: string;
};

type ToolRecord = {
  name: string;
  result: unknown;
  text: string;
};

type SignalflowPurpose = "cache" | "latency";

export function defaultSplunkMcpUrl(realm: string) {
  return `https://api.${realm}.signalfx.com/v2/mcp`;
}

export function parseMcpHttpResponse(text: string) {
  const trimmed = text.trim();
  if (!trimmed) {
    return undefined;
  }

  const dataLines = trimmed
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith("data:"))
    .map((line) => line.slice("data:".length).trim())
    .filter((line) => line && line !== "[DONE]");

  if (dataLines.length > 0) {
    for (let index = dataLines.length - 1; index >= 0; index -= 1) {
      try {
        return JSON.parse(dataLines[index]);
      } catch {
        continue;
      }
    }
  }

  return JSON.parse(trimmed);
}

export class SplunkMcpClient {
  private toolsPromise?: Promise<McpTool[]>;

  constructor(private readonly config: SplunkMcpConfig) {}

  async gatherEvidence(payload: DetectorWebhookPayload): Promise<SplunkMcpEvidenceResult> {
    if (!this.config.enabled) {
      return {
        sources: [],
        warnings: ["Splunk MCP enrichment is disabled."]
      };
    }

    if (!this.config.accessToken) {
      return {
        sources: [],
        warnings: ["SPLUNK_ACCESS_TOKEN not configured; Splunk MCP enrichment is unavailable."]
      };
    }

    const scope = this.buildScope(payload);
    const warnings: string[] = [];
    const tools = await this.listTools(warnings);
    if (tools.length === 0) {
      return {
        sources: [],
        warnings: warnings.length > 0 ? warnings : ["Splunk MCP did not return any tools."]
      };
    }

    const plannedTools = [
      "search_alerts_or_incidents",
      "get_apm_services",
      "get_apm_service_dependencies",
      "get_apm_service_latency",
      "get_apm_service_errors_and_requests",
      "get_apm_exemplar_traces",
      "execute_signalflow_program"
    ];

    const confirmationToolNames = [
      "get_apm_service_latency",
      "execute_signalflow_program"
    ];
    const confirmationRecords = await this.callAvailableTools(confirmationToolNames, tools, scope, warnings);
    const preliminaryEvidence = this.buildEvidenceResult(scope, confirmationRecords, [...warnings]);

    if (
      preliminaryEvidence.confidenceBand === "low" &&
      process.env.SPLUNK_MCP_COLLECT_DETAILS_ON_LOW !== "true"
    ) {
      return preliminaryEvidence;
    }

    const detailToolNames = plannedTools.filter((toolName) => !confirmationToolNames.includes(toolName));
    const detailRecords = await this.callAvailableTools(detailToolNames, tools, scope, warnings, {
      warnOnFailure: false
    });

    return this.buildEvidenceResult(scope, [...confirmationRecords, ...detailRecords], [...warnings]);
  }

  private async callAvailableTools(
    toolNames: string[],
    tools: McpTool[],
    scope: McpScope,
    warnings: string[],
    options: { warnOnFailure?: boolean } = {}
  ) {
    const records = (
      await Promise.all(
        toolNames.map(async (toolName) => {
          const tool = tools.find((candidate) => candidate.name === toolName);
          if (!tool) {
            return null;
          }

          try {
            if (toolName === "execute_signalflow_program") {
              return await Promise.all(
                (["cache", "latency"] as const).map(async (purpose) => {
                  const result = await this.callTool(tool, scope, purpose);
                  return {
                    name: toolName,
                    result,
                    text: stringifyMcpResult(result)
                  };
                })
              );
            }

            const result = await this.callTool(tool, scope);
            return {
              name: toolName,
              result,
              text: stringifyMcpResult(result)
            };
          } catch (error) {
            if (options.warnOnFailure !== false) {
              warnings.push(
                `Splunk MCP tool ${toolName} failed: ${error instanceof Error ? error.message : "unknown error"}.`
              );
            }
            return null;
          }
        })
      )
    )
      .flat()
      .filter((record): record is ToolRecord => Boolean(record));
    return records;
  }

  private buildScope(payload: DetectorWebhookPayload): McpScope {
    const end = new Date();
    const start = new Date(end.getTime() - 15 * 60 * 1000);
    const environment =
      payload.dimensions?.environment ??
      process.env.DEPLOYMENT_ENVIRONMENT ??
      "demo";

    return {
      detectorId: payload.detectorId,
      detectorName: payload.detectorName,
      incidentId: payload.incidentId,
      severity: payload.severity,
      service: payload.dimensions?.service ?? "claims-knowledge",
      environment,
      instance:
        payload.dimensions?.["service.instance.id"] ??
        payload.dimensions?.instance ??
        process.env.INSTANCE ??
        "student-001",
      cacheMountpoint: process.env.SPLUNK_CACHE_MOUNTPOINT ?? "/var/cache/claims-knowledge",
      cacheUtilizationMetric:
        process.env.SPLUNK_CACHE_UTILIZATION_METRIC ??
        process.env.CLAIMS_KNOWLEDGE_CACHE_UTILIZATION_METRIC ??
        "claims_knowledge.cache.utilization",
      claimStatusLatencyMetric:
        process.env.SPLUNK_CLAIM_STATUS_LATENCY_METRIC ??
        process.env.CLAIMS_KNOWLEDGE_CLAIM_STATUS_LATENCY_METRIC ??
        "claims_knowledge.claim_status.latency_ms",
      evidenceMetricSource: process.env.SPLUNK_EVIDENCE_METRIC_SOURCE ?? "claims-knowledge-evidence",
      startTime: start.toISOString(),
      endTime: end.toISOString()
    };
  }

  private async listTools(warnings: string[]) {
    try {
      this.toolsPromise ??= this.callJsonRpc("tools/list", {}).then((response) => {
        const tools = valueAtPath(response, "tools");
        return Array.isArray(tools) ? tools.filter(isMcpTool) : [];
      });
      const tools = await this.toolsPromise;
      return tools;
    } catch (error) {
      this.toolsPromise = undefined;
      warnings.push(`Splunk MCP tools/list failed: ${error instanceof Error ? error.message : "unknown error"}.`);
      return [];
    }
  }

  private async callTool(tool: McpTool, scope: McpScope, signalflowPurpose?: SignalflowPurpose) {
    const args = this.buildToolArguments(tool, scope, signalflowPurpose);
    const response = await this.callJsonRpc("tools/call", {
      name: tool.name,
      arguments: args
    });

    return response;
  }

  private async callJsonRpc(method: string, params: JsonObject) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.config.timeoutMs);

    try {
      const response = await fetch(this.config.url, {
        method: "POST",
        headers: this.buildHeaders(),
        body: JSON.stringify({
          jsonrpc: "2.0",
          id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
          method,
          params
        }),
        signal: controller.signal
      });
      const body = await response.text();

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${body.slice(0, 240)}`);
      }

      const parsed = parseMcpHttpResponse(body);
      if (!parsed || typeof parsed !== "object") {
        throw new Error("empty MCP response");
      }

      const error = (parsed as JsonObject).error;
      if (error) {
        throw new Error(typeof error === "string" ? error : JSON.stringify(error));
      }

      const result = (parsed as JsonObject).result;
      if (result === undefined) {
        return parsed;
      }
      return result;
    } finally {
      clearTimeout(timeout);
    }
  }

  private buildHeaders() {
    const headers: Record<string, string> = {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "x-sf-realm": this.config.realm,
      "x-sf-token": this.config.accessToken
    };

    if (this.config.authToken) {
      headers.authorization = `Bearer ${this.config.authToken}`;
    }

    if (this.config.tenant) {
      headers.splunk_tenant = this.config.tenant;
    }

    return headers;
  }

  private buildToolArguments(tool: McpTool, scope: McpScope, signalflowPurpose?: SignalflowPurpose) {
    const defaults = defaultParamsForTool(tool.name, scope, signalflowPurpose);
    const paramProperties = schemaObjectProperties(valueAtPath(tool.inputSchema, "properties.params"), tool.inputSchema);

    if (!paramProperties) {
      return {
        params: defaults
      };
    }

    const params: JsonObject = {};
    for (const key of Object.keys(paramProperties)) {
      const value = valueForParamKey(key, scope, defaults);
      if (value !== undefined) {
        params[key] = value;
      }
    }

    return {
      params
    };
  }

  private buildEvidenceResult(scope: McpScope, records: ToolRecord[], warnings: string[]): SplunkMcpEvidenceResult {
    const sources = uniqueStrings(records.map((record) => `mcp:${record.name}`));
    if (records.length === 0) {
      return {
        sources,
        warnings: warnings.length > 0 ? warnings : ["Splunk MCP tools were available, but no evidence tools returned data."],
        confidenceBand: "low",
        likelyCause: "Splunk MCP did not return live evidence; keep remediation recommendation-only until signals are verified."
      };
    }

    const combinedText = records.map((record) => record.text).join("\n");
    const affectedServices = uniqueStrings([scope.service, ...extractServiceNames(combinedText)]);
    const traceIds = uniqueStrings(extractTraceIds(combinedText));
    const signalflowLatencyMs = extractSignalflowMetricValue(records, scope.claimStatusLatencyMetric);
    const p95LatencyMs = signalflowLatencyMs ?? extractNumber(records, ["p95", "latency", "duration"]);
    const errorRate = extractNumber(records, ["error", "rate"]);
    const errorRatePercent = errorRate === undefined ? undefined : normalizeErrorRatePercent(errorRate);
    const filesystemUtilization =
      extractSignalflowMetricValue(records, scope.cacheUtilizationMetric, { max: 100 }) ??
      extractSignalflowValue(records);
    const thresholds = evidenceThresholds();
    const filesystemQueried =
      /claims_knowledge\.cache\.utilization|disk\.utilization|filesystem|mountpoint|cache filesystem|cache mount|cache utilization|\/var\/cache\/claims-knowledge/i.test(combinedText) ||
      records.some((record) => record.name === "execute_signalflow_program");
    const filesystemPressureConfirmed =
      filesystemUtilization !== undefined
        ? filesystemUtilization >= thresholds.filesystemUtilization
        : /\b(?:above threshold|elevated|high utilization|filesystem pressure|disk pressure)\b/i.test(combinedText);
    const latencyElevated =
      p95LatencyMs !== undefined
        ? p95LatencyMs >= thresholds.apmLatencyMs
        : /\b(?:latency|duration)[^.\n]*(?:above threshold|elevated|high|slow)\b/i.test(combinedText);
    const errorToolQueried = records.some((record) => record.name === "get_apm_service_errors_and_requests");
    const errorRateElevated =
      errorRatePercent !== undefined
        ? errorRatePercent >= thresholds.errorRatePercent
        : /\b(?:error|failure)[^.\n]*(?:above threshold|elevated|high)\b/i.test(combinedText);

    if (filesystemQueried && !filesystemPressureConfirmed) {
      warnings.push(
        `Splunk MCP queried ${scope.cacheUtilizationMetric} but did not confirm cache utilization above ${thresholds.filesystemUtilization}.`
      );
    }
    if (records.some((record) => record.name === "get_apm_service_latency") && !latencyElevated) {
      warnings.push(
        `Splunk MCP queried ${scope.claimStatusLatencyMetric}/APM latency but did not confirm latency above ${thresholds.apmLatencyMs} ms.`
      );
    }

    const confidenceBand = filesystemPressureConfirmed && latencyElevated
      ? "high"
      : affectedServices.length > 0 && (filesystemPressureConfirmed || latencyElevated)
        ? "medium"
        : "low";
    const resources = buildResources(scope, records, affectedServices, traceIds, filesystemQueried);
    const approvalEvidence = buildApprovalEvidence({
      scope,
      affectedServices,
      records,
      p95LatencyMs,
      latencyElevated,
      errorRatePercent,
      errorToolQueried,
      errorRateElevated,
      filesystemUtilization,
      filesystemPressureConfirmed,
      filesystemQueried,
      thresholds
    });
    const likelyCause =
      confidenceBand === "high"
        ? `${scope.service} cache filesystem pressure is correlated with elevated APM latency for AI Claim Status.`
      : confidenceBand === "medium"
          ? `Splunk MCP returned partial degradation evidence for ${scope.service}, but did not confirm both filesystem pressure and elevated latency.`
          : "Splunk MCP did not confirm filesystem and APM evidence; keep remediation recommendation-only until signals are verified.";

    return {
      sources,
      warnings,
      affectedServices,
      suspectService: affectedServices[0] ?? scope.service,
      p95LatencyMs,
      errorRate,
      affectedTransactions: ["claim_status_response"],
      recentChange: records.some((record) => record.name === "search_alerts_or_incidents")
        ? `Splunk MCP alert search scoped to ${scope.detectorName}.`
        : undefined,
      likelyCause,
      confidenceBand,
      assistantSummary: buildAssistantSummary({
        scope,
        sources,
        affectedServices,
        p95LatencyMs,
        errorRate,
        traceIds,
        filesystemQueried,
        filesystemPressureConfirmed,
        filesystemUtilization,
        latencyElevated,
        confidenceBand
      }),
      observabilityResources: resources,
      traceIds,
      approvalEvidence
    };
  }
}

function defaultParamsForTool(toolName: string, scope: McpScope, signalflowPurpose?: SignalflowPurpose): JsonObject {
  const query = `${scope.detectorName} ${scope.service} ${scope.environment}`;
  const base = {
    environment: scope.environment,
    service: scope.service,
    serviceName: scope.service,
    service_name: scope.service,
    start_time: scope.startTime,
    end_time: scope.endTime,
    startTime: scope.startTime,
    endTime: scope.endTime,
    start: scope.startTime,
    end: scope.endTime,
    limit: 5
  };

  if (toolName === "search_alerts_or_incidents") {
    return {
      ...base,
      query,
      search: query,
      severity: scope.severity,
      detector_id: scope.detectorId,
      incident_id: scope.incidentId
    };
  }

  if (toolName === "execute_signalflow_program") {
    const cacheFilters = [
      `filter('deployment.environment', '${scope.environment}')`,
      `filter('service.name', '${scope.service}')`,
      scope.instance ? `filter('service.instance.id', '${scope.instance}')` : undefined,
      `filter('mountpoint', '${scope.cacheMountpoint}')`,
      `filter('demo.metric_source', '${scope.evidenceMetricSource}')`
    ].filter((filter): filter is string => Boolean(filter));
    const latencyFilters = [
      `filter('deployment.environment', '${scope.environment}')`,
      `filter('service.name', '${scope.service}')`,
      scope.instance ? `filter('service.instance.id', '${scope.instance}')` : undefined,
      "filter('app.business_transaction', 'claim_status_response')",
      `filter('demo.metric_source', '${scope.evidenceMetricSource}')`
    ].filter((filter): filter is string => Boolean(filter));
    const program =
      signalflowPurpose === "latency"
        ? `data('${scope.claimStatusLatencyMetric}', filter=${latencyFilters.join(" and ")}).max(by=['service.name', 'service.instance.id', 'app.business_transaction']).publish(label='claim status latency ms')`
        : `data('${scope.cacheUtilizationMetric}', filter=${cacheFilters.join(" and ")}).max(by=['service.name', 'service.instance.id', 'mountpoint']).publish(label='cache utilization')`;

    return {
      ...base,
      program,
      signalflow: program,
      time_range: {
        start: scope.startTime,
        stop: scope.endTime
      },
      resolution_ms: 30000
    };
  }

  return base;
}

function valueForParamKey(key: string, scope: McpScope, defaults: JsonObject) {
  if (key in defaults) {
    return defaults[key];
  }

  const normalized = key.toLowerCase().replace(/[-_]/g, "");
  if (normalized.includes("environment") || normalized === "env") {
    return scope.environment;
  }
  if (normalized.includes("servicename") || normalized === "service") {
    return scope.service;
  }
  if (normalized.includes("start") || normalized === "from") {
    return scope.startTime;
  }
  if (normalized.includes("end") || normalized === "to") {
    return scope.endTime;
  }
  if (normalized.includes("timerange")) {
    return {
      start: scope.startTime,
      stop: scope.endTime
    };
  }
  if (normalized.includes("resolution")) {
    return 30000;
  }
  if (normalized.includes("limit") || normalized.includes("count")) {
    return 5;
  }
  if (normalized.includes("query") || normalized.includes("search")) {
    return `${scope.detectorName} ${scope.service} ${scope.environment}`;
  }
  if (normalized.includes("program") || normalized.includes("signalflow")) {
    return defaults.program ?? defaults.signalflow;
  }
  if (normalized.includes("severity")) {
    return scope.severity;
  }
  if (normalized.includes("detector")) {
    return scope.detectorId;
  }
  if (normalized.includes("incident")) {
    return scope.incidentId;
  }
  if (normalized.includes("mount")) {
    return scope.cacheMountpoint;
  }
  if (normalized.includes("instance")) {
    return scope.instance;
  }
  if (normalized.includes("exemplartype")) {
    return "lat_buck_";
  }
  if (normalized.includes("minlatency")) {
    return Math.round(evidenceThresholds().apmLatencyMs * 1000);
  }
  if (normalized.includes("tagsordimensions")) {
    const dimensions: Record<string, string[]> = {
      "app.business_transaction": ["claim_status_response"]
    };
    if (scope.instance) {
      dimensions["service.instance.id"] = [scope.instance];
    }
    return dimensions;
  }

  return undefined;
}

function schemaObjectProperties(value: unknown, root?: unknown): JsonObject | undefined {
  if (value && typeof value === "object" && typeof (value as JsonObject).$ref === "string") {
    const ref = (value as JsonObject).$ref as string;
    if (ref.startsWith("#/")) {
      return schemaObjectProperties(valueAtPath(root, ref.slice(2).replaceAll("/", ".")), root);
    }
  }

  if (!value || typeof value !== "object") {
    return undefined;
  }

  const properties = (value as JsonObject).properties;
  return properties && typeof properties === "object" ? (properties as JsonObject) : undefined;
}

function valueAtPath(payload: unknown, path: string) {
  if (!payload || typeof payload !== "object") {
    return undefined;
  }

  return path.split(".").reduce<unknown>((current, segment) => {
    if (!current || typeof current !== "object") {
      return undefined;
    }
    return (current as JsonObject)[segment];
  }, payload);
}

function isMcpTool(value: unknown): value is McpTool {
  return Boolean(value && typeof value === "object" && typeof (value as JsonObject).name === "string");
}

function stringifyMcpResult(result: unknown): string {
  const content = valueAtPath(result, "content");
  if (Array.isArray(content)) {
    return content
      .map((item) => {
        if (item && typeof item === "object" && typeof (item as JsonObject).text === "string") {
          return (item as JsonObject).text;
        }
        return JSON.stringify(item);
      })
      .join("\n");
  }

  return typeof result === "string" ? result : JSON.stringify(result);
}

function extractServiceNames(text: string) {
  return Array.from(text.matchAll(/\b(?:claims|support)-[a-z0-9-]+\b/gi)).map((match) => match[0]);
}

function extractTraceIds(text: string) {
  const labeledTraceIds = Array.from(
    text.matchAll(/\btrace(?:id|_id|Id|ID)?\s*[=:]\s*["']?([0-9a-f]{32})["']?/gi)
  ).map((match) => match[1]);
  const hexTraceIds = Array.from(text.matchAll(/\b(?=[0-9a-f]*[a-f])[0-9a-f]{32}\b/gi)).map((match) => match[0]);
  return [...labeledTraceIds, ...hexTraceIds];
}

function uniqueStrings(values: Array<string | undefined>) {
  return Array.from(new Set(values.filter((value): value is string => Boolean(value)))).slice(0, 12);
}

function extractNumber(records: ToolRecord[], keys: string[]) {
  const normalizedKeys = keys.map((key) => key.toLowerCase());
  for (const record of records) {
    const pairs = collectKeyValuePairs(record.result);
    for (const pair of pairs) {
      const key = pair.key.toLowerCase();
      if (normalizedKeys.every((candidate) => key.includes(candidate))) {
        const numeric = numberValue(pair.value);
        if (numeric !== undefined) {
          return normalizeMetricNumber(key, numeric);
        }
      }
    }
  }

  const text = records.map((record) => record.text).join("\n");
  const label = keys.join("|");
  const match = text.match(new RegExp(`(?:${label})[^0-9]*(\\d+(?:\\.\\d+)?)`, "i"));
  return match?.[1] ? Number(match[1]) : undefined;
}

function collectKeyValuePairs(value: unknown, prefix = ""): Array<{ key: string; value: unknown }> {
  if (!value || typeof value !== "object") {
    return [];
  }

  if (Array.isArray(value)) {
    return value.flatMap((item, index) => collectKeyValuePairs(item, `${prefix}.${index}`));
  }

  return Object.entries(value as JsonObject).flatMap(([key, nestedValue]) => {
    const path = prefix ? `${prefix}.${key}` : key;
    return [{ key: path, value: nestedValue }, ...collectKeyValuePairs(nestedValue, path)];
  });
}

function numberValue(value: unknown) {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value;
  }
  if (typeof value === "string" && value.trim() && !Number.isNaN(Number(value))) {
    return Number(value);
  }
  return undefined;
}

function normalizeMetricNumber(key: string, value: number) {
  if (key.includes("ns") || value > 100_000) {
    return Math.round(value / 1_000_000);
  }
  return value;
}

function evidenceThresholds(): EvidenceThresholds {
  return {
    filesystemUtilization: Number(process.env.FILESYSTEM_UTILIZATION_THRESHOLD ?? 85),
    apmLatencyMs: Number(process.env.APM_LATENCY_THRESHOLD_NS ?? 1_800_000_000) / 1_000_000,
    errorRatePercent: Number(process.env.APM_ERROR_RATE_THRESHOLD_PERCENT ?? 5)
  };
}

function normalizeErrorRatePercent(value: number) {
  return value <= 1 ? value * 100 : value;
}

function roundMetric(value: number | undefined) {
  return value === undefined ? undefined : Math.round(value * 10) / 10;
}

function extractSignalflowMetricValue(
  records: ToolRecord[],
  metricName: string,
  options: { max?: number; mode?: "latest" | "max" } = {}
) {
  const signalflows = records.filter((record) => record.name === "execute_signalflow_program");
  if (signalflows.length === 0) {
    return undefined;
  }

  const values = signalflows.flatMap((signalflow) => signalflowPayloads(signalflow)).flatMap((payload) => {
    if (!payload || typeof payload !== "object") {
      return [];
    }

    const metadata = (payload as JsonObject).metadata;
    const timeseries = (payload as JsonObject).timeseries;
    if (!metadata || typeof metadata !== "object" || !timeseries || typeof timeseries !== "object") {
      return [];
    }

    const matchingIds = new Set(
      Object.entries(metadata as JsonObject)
        .filter(([, value]) => {
          if (!value || typeof value !== "object") {
            return false;
          }
          return (value as JsonObject).sf_originatingMetric === metricName;
        })
        .map(([id]) => id)
    );

    const valuesBySeries = new Map<string, number[]>();
    Object.entries(timeseries as JsonObject)
      .sort(([left], [right]) => Number(left) - Number(right))
      .forEach(([, point]) => {
      if (!point || typeof point !== "object") {
        return;
      }
      for (const [id, rawValue] of Object.entries(point as JsonObject)) {
        if (!matchingIds.has(id)) {
          continue;
        }
        const value = numberValue(rawValue);
        if (
          value === undefined ||
          value < 0 ||
          (options.max !== undefined && value > options.max)
        ) {
          continue;
        }
        const seriesValues = valuesBySeries.get(id) ?? [];
        seriesValues.push(value);
        valuesBySeries.set(id, seriesValues);
      }
    });

    return Array.from(valuesBySeries.values()).flatMap((seriesValues) => {
      if (seriesValues.length === 0) {
        return [];
      }
      return options.mode === "max" ? Math.max(...seriesValues) : seriesValues[seriesValues.length - 1];
    });
  });

  return values.length > 0 ? Math.max(...values) : undefined;
}

function signalflowPayloads(record: ToolRecord): unknown[] {
  const content = valueAtPath(record.result, "content");
  if (Array.isArray(content)) {
    return content.flatMap((item) => {
      if (!item || typeof item !== "object" || typeof (item as JsonObject).text !== "string") {
        return [];
      }
      const text = (item as JsonObject).text as string;
      try {
        return [JSON.parse(text)];
      } catch {
        return [];
      }
    });
  }

  return [record.result];
}

function extractSignalflowValue(records: ToolRecord[]) {
  const signalflow = records.find((record) => record.name === "execute_signalflow_program");
  if (!signalflow) {
    return undefined;
  }

  const pairs = collectKeyValuePairs(signalflow.result);
  const plausibleValues = pairs
    .filter((pair) => !/\b(?:time|timestamp|start|end|count|resolution|rollup)\b/i.test(pair.key))
    .map((pair) => numberValue(pair.value))
    .filter((value): value is number => value !== undefined && value >= 0 && value <= 100);

  if (plausibleValues.length > 0) {
    return Math.max(...plausibleValues);
  }

  const textValues = signalflow.text
    .match(/\b\d+(?:\.\d+)?\b/g)
    ?.map((value) => Number(value))
    .filter((value) => Number.isFinite(value) && value >= 0 && value <= 100);

  return textValues && textValues.length > 0 ? Math.max(...textValues) : undefined;
}

function buildResources(
  scope: McpScope,
  records: ToolRecord[],
  services: string[],
  traceIds: string[],
  filesystemQueried: boolean
): SplunkMcpResource[] {
  const resources: SplunkMcpResource[] = services.map((service) => ({
    type: "service",
    name: service,
    detail: `APM service in ${scope.environment}`
  }));

  if (records.some((record) => record.name === "get_apm_service_dependencies")) {
    resources.push({
      type: "dependency",
      name: `${scope.service} dependencies`,
      detail: "Returned by Splunk MCP APM dependency lookup."
    });
  }

  if (filesystemQueried) {
    resources.push({
      type: "metric",
      name: scope.cacheUtilizationMetric,
      detail: `Cache mount ${scope.cacheMountpoint}`
    });
    resources.push({
      type: "metric",
      name: scope.claimStatusLatencyMetric,
      detail: "AI Claim Status latency"
    });
  }

  if (records.some((record) => record.name === "search_alerts_or_incidents")) {
    resources.push({
      type: "alert",
      name: scope.detectorName,
      detail: `Detector ${scope.detectorId}`
    });
  }

  for (const traceId of traceIds.slice(0, 5)) {
    resources.push({
      type: "trace",
      name: traceId,
      detail: "APM exemplar trace"
    });
  }

  return resources.slice(0, 16);
}

function evidenceStatus(available: boolean, confirmed: boolean): EvidenceMetricStatus {
  if (!available) {
    return "unavailable";
  }
  return confirmed ? "confirmed" : "not_confirmed";
}

function buildApprovalEvidence(input: {
  scope: McpScope;
  affectedServices: string[];
  records: ToolRecord[];
  p95LatencyMs?: number;
  latencyElevated: boolean;
  errorRatePercent?: number;
  errorToolQueried: boolean;
  errorRateElevated: boolean;
  filesystemUtilization?: number;
  filesystemPressureConfirmed: boolean;
  filesystemQueried: boolean;
  thresholds: EvidenceThresholds;
}): ApprovalEvidence {
  const endpointStatus = evidenceStatus(
    input.p95LatencyMs !== undefined || input.latencyElevated,
    input.latencyElevated
  );
  const filesystemStatus = evidenceStatus(
    input.filesystemUtilization !== undefined || input.filesystemQueried,
    input.filesystemPressureConfirmed
  );
  const errorStatus = input.errorRatePercent !== undefined
    ? evidenceStatus(true, input.errorRateElevated)
    : input.errorToolQueried
      ? "not_confirmed"
      : "unavailable";
  const topologyConfirmed =
    input.records.some((record) => record.name === "get_apm_service_dependencies") ||
    input.affectedServices.some((service) => service === "claims-portal-api" || service === "claims-assistant");
  const remediationSupported = input.latencyElevated && input.filesystemPressureConfirmed;

  return {
    customerImpact: [
      {
        label: "POST /api/support/respond",
        source: "rum",
        metricName: "rum.network_request.duration",
        value: roundMetric(input.p95LatencyMs),
        unit: "ms",
        threshold: input.thresholds.apmLatencyMs,
        status: endpointStatus,
        detail: input.latencyElevated
          ? `Digital Experience network activity for AI Claim Status is slow; correlated backend p95 is ${roundMetric(input.p95LatencyMs) ?? "above threshold"} ms for ${BUSINESS_TRANSACTIONS.customerSupportResponse}.`
          : "Digital Experience network activity is part of the proof path, but the returned evidence did not confirm endpoint latency above threshold."
      }
    ],
    backendImpact: [
      {
        label: `${input.scope.service} p95 latency`,
        source: "apm",
        metricName: input.scope.claimStatusLatencyMetric,
        value: roundMetric(input.p95LatencyMs),
        unit: "ms",
        threshold: input.thresholds.apmLatencyMs,
        status: endpointStatus,
        detail: input.latencyElevated
          ? `APM latency for ${input.scope.service} is above the ${input.thresholds.apmLatencyMs} ms threshold on the claim-status path.`
          : `APM latency for ${input.scope.service} was queried, but it was not above the ${input.thresholds.apmLatencyMs} ms threshold.`
      },
      {
        label: `${input.scope.service} error rate`,
        source: "apm",
        metricName: "service.request.errors",
        value: roundMetric(input.errorRatePercent),
        unit: "%",
        threshold: input.thresholds.errorRatePercent,
        status: errorStatus,
        detail: input.errorRateElevated
          ? `APM errors are also elevated above ${input.thresholds.errorRatePercent}%.`
          : input.errorRatePercent !== undefined
            ? `APM errors/request data returned ${roundMetric(input.errorRatePercent)}%; no elevated errors are apparent.`
            : input.errorToolQueried
              ? "APM errors/request lookup returned no elevated error metric; no apparent errors are part of the incident."
              : "APM errors/request data was not returned by Splunk MCP."
      }
    ],
    infrastructureImpact: [
      {
        label: "Cache filesystem utilization",
        source: "infrastructure",
        metricName: input.scope.cacheUtilizationMetric,
        value: roundMetric(input.filesystemUtilization),
        unit: "%",
        threshold: input.thresholds.filesystemUtilization,
        status: filesystemStatus,
        detail: input.filesystemPressureConfirmed
          ? `Infrastructure evidence shows ${input.scope.cacheMountpoint} at ${roundMetric(input.filesystemUtilization) ?? "above threshold"}%, above the ${input.thresholds.filesystemUtilization}% threshold.`
          : `Infrastructure evidence queried ${input.scope.cacheMountpoint}, but cache filesystem pressure was not confirmed above ${input.thresholds.filesystemUtilization}%.`
      }
    ],
    impactChain: [
      {
        stage: "customer",
        label: "Customer request slows",
        detail: "RUM/network evidence identifies POST /api/support/respond as the customer-visible AI Claim Status request.",
        status: endpointStatus
      },
      {
        stage: "gateway",
        label: "Request traverses app services",
        detail: topologyConfirmed
          ? `APM service/dependency evidence includes ${input.affectedServices.join(", ")}.`
          : "The known route is claims-portal-api to claims-assistant to claims-knowledge; dependency evidence was not returned.",
        status: topologyConfirmed ? "confirmed" : "not_confirmed"
      },
      {
        stage: "dependency",
        label: `${input.scope.service} is slow without clear errors`,
        detail: input.errorRateElevated
          ? `${input.scope.service} latency and error rate are both elevated.`
          : `${input.scope.service} latency is elevated while APM shows no apparent error spike.`,
        status: endpointStatus
      },
      {
        stage: "infrastructure",
        label: "Cache filesystem is full",
        detail: `${input.scope.cacheMountpoint} utilization is the infrastructure signal tied to the slow dependency.`,
        status: filesystemStatus
      },
      {
        stage: "remediation",
        label: "Cache cleanup is supported",
        detail: remediationSupported
          ? "The evidence supports clean_claims_knowledge_cache before operator approval."
          : "Keep the action recommendation-only until both latency and filesystem pressure are confirmed.",
        status: remediationSupported ? "confirmed" : "not_confirmed"
      }
    ]
  };
}

function buildAssistantSummary(input: {
  scope: McpScope;
  sources: string[];
  affectedServices: string[];
  p95LatencyMs?: number;
  errorRate?: number;
  traceIds: string[];
  filesystemQueried: boolean;
  filesystemPressureConfirmed: boolean;
  filesystemUtilization?: number;
  latencyElevated: boolean;
  confidenceBand: "low" | "medium" | "high";
}) {
  const lines = [
    `${input.confidenceBand[0].toUpperCase()}${input.confidenceBand.slice(1)} confidence Splunk MCP evidence for AI Claim Status.`,
    `MCP sources: ${input.sources.join(", ")}.`,
    `Suspect service: ${input.affectedServices[0] ?? input.scope.service}.`
  ];

  if (input.filesystemPressureConfirmed) {
    lines.push(
      `Filesystem signal: ${input.scope.cacheUtilizationMetric} ${input.filesystemUtilization ?? "above threshold"} for ${input.scope.cacheMountpoint}.`
    );
  } else if (input.filesystemQueried) {
    lines.push(`Filesystem signal: ${input.scope.cacheUtilizationMetric} queried for ${input.scope.cacheMountpoint}, but pressure was not confirmed.`);
  }
  if (input.p95LatencyMs !== undefined && input.latencyElevated) {
    lines.push(`Latency evidence: p95 latency ${input.p95LatencyMs} ms.`);
  } else if (input.p95LatencyMs !== undefined) {
    lines.push(`Latency evidence: p95 latency ${input.p95LatencyMs} ms, below the detector threshold.`);
  }
  if (input.errorRate !== undefined) {
    const errorRatePercent = roundMetric(normalizeErrorRatePercent(input.errorRate));
    const errorThreshold = evidenceThresholds().errorRatePercent;
    lines.push(
      errorRatePercent !== undefined && errorRatePercent >= errorThreshold
        ? `Error evidence: APM error rate ${errorRatePercent}%, above the ${errorThreshold}% threshold.`
        : `Error evidence: APM error rate ${errorRatePercent}%; no elevated errors are apparent.`
    );
  }
  if (input.traceIds.length > 0) {
    lines.push(`Trace evidence: ${input.traceIds.slice(0, 3).join(", ")}.`);
  }

  lines.push("Recommended action: clean_claims_knowledge_cache.");
  return lines.join("\n");
}
