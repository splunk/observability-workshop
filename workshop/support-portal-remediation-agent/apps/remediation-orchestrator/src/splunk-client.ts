import type { ApprovalEvidence, DetectorWebhookPayload, EvidenceBundle } from "@ibobs/shared-types";
import { defaultSplunkMcpUrl, SplunkMcpClient, type SplunkMcpResource } from "./splunk-mcp-client";

export type SplunkEnrichmentResult = {
  apiBacked: boolean;
  sources: string[];
  warnings: string[];
  affectedSessions?: number;
  sessionReplayUrl?: string;
  p95LatencyMs?: number;
  errorRate?: number;
  affectedServices: string[];
  suspectService?: string;
  recentChange?: string;
  affectedTransactions?: string[];
  likelyCause?: string;
  confidenceBand?: "low" | "medium" | "high";
  assistantSummary?: string;
  observabilityResources?: SplunkMcpResource[];
  traceIds?: string[];
  approvalEvidence?: ApprovalEvidence;
};

export class SplunkObservabilityClient {
  private readonly mcpClient: SplunkMcpClient;

  constructor(
    private readonly baseUrl: string,
    private readonly accessToken: string
  ) {
    const realm = process.env.SPLUNK_REALM ?? "us1";
    this.mcpClient = new SplunkMcpClient({
      enabled: process.env.SPLUNK_MCP_ENABLED !== "false",
      url: process.env.SPLUNK_MCP_URL || defaultSplunkMcpUrl(realm),
      accessToken,
      realm,
      authToken: process.env.SPLUNK_MCP_AUTH_TOKEN,
      tenant: process.env.SPLUNK_MCP_TENANT,
      timeoutMs: Number(process.env.SPLUNK_MCP_TIMEOUT_MS ?? 8000)
    });
  }

  async enrichDetector(payload: DetectorWebhookPayload): Promise<SplunkEnrichmentResult> {
    const fallback = this.buildFallback(payload);
    if (!this.accessToken) {
      return fallback;
    }

    const sources: string[] = [];
    const warnings: string[] = [];
    let merged = { ...fallback };

    const mcp = await this.mcpClient.gatherEvidence(payload);
    if (mcp.sources.length > 0) {
      merged = {
        ...merged,
        affectedServices: mcp.affectedServices ?? merged.affectedServices,
        suspectService: mcp.suspectService ?? merged.suspectService,
        p95LatencyMs: mcp.p95LatencyMs ?? merged.p95LatencyMs,
        errorRate: mcp.errorRate ?? merged.errorRate,
        affectedTransactions: mcp.affectedTransactions ?? merged.affectedTransactions,
        recentChange: mcp.recentChange ?? merged.recentChange,
        likelyCause: mcp.likelyCause ?? merged.likelyCause,
        confidenceBand: mcp.confidenceBand ?? merged.confidenceBand,
        assistantSummary: mcp.assistantSummary ?? merged.assistantSummary,
        observabilityResources: mcp.observabilityResources ?? merged.observabilityResources,
        traceIds: mcp.traceIds ?? merged.traceIds,
        approvalEvidence: mcp.approvalEvidence ?? merged.approvalEvidence
      };
      sources.push(...mcp.sources);
    }
    warnings.push(...mcp.warnings);

    if (sources.length > 0 && process.env.SPLUNK_REST_ENRICHMENT_ENABLED !== "true") {
      return {
        ...merged,
        apiBacked: true,
        sources,
        warnings
      };
    }

    const detector = await this.fetchCandidateJson(
      this.resolvePath(process.env.SPLUNK_DETECTOR_ENDPOINT_TEMPLATE, payload),
      warnings
    );
    if (detector) {
      sources.push("detector");
      if (!this.stringFrom(detector, ["recentChange", "recent_change", "event.recentChange"])) {
        warnings.push("Detector API responded, but did not include recent change context.");
      }
      merged = {
        ...merged,
        recentChange: this.stringFrom(detector, ["recentChange", "recent_change", "event.recentChange"]) ?? merged.recentChange
      };
    }

    const impact = await this.fetchCandidateJson(
      this.resolvePath(process.env.SPLUNK_IMPACT_ENDPOINT_TEMPLATE, payload),
      warnings
    );
    if (impact) {
      sources.push("impact");
      merged = {
        ...merged,
        affectedSessions: this.numberFrom(impact, ["affectedSessions", "affected_sessions", "rum.affectedSessions"]) ?? merged.affectedSessions,
        p95LatencyMs: this.numberFrom(impact, ["p95LatencyMs", "latency.p95", "apm.p95LatencyMs"]) ?? merged.p95LatencyMs,
        errorRate: this.numberFrom(impact, ["errorRate", "error_rate", "apm.errorRate"]) ?? merged.errorRate,
        sessionReplayUrl: this.stringFrom(impact, ["sessionReplayUrl", "session_replay_url"]) ?? merged.sessionReplayUrl
      };
    }

    const topology = await this.fetchCandidateJson(
      this.resolvePath(process.env.SPLUNK_TOPOLOGY_ENDPOINT_TEMPLATE, payload),
      warnings
    );
    if (topology) {
      sources.push("topology");
      const topologyServices =
        this.arrayFrom(topology, ["affectedServices", "services", "apm.affectedServices"]) ??
        this.topologyNodeServices(topology);
      const containsDemoService =
        topologyServices?.some(
          (service) =>
            service.startsWith("claims-") ||
            service.startsWith("support-") ||
            service === payload.dimensions?.service
        ) ??
        false;
      if (topologyServices && containsDemoService) {
        merged = {
          ...merged,
          affectedServices: topologyServices,
          suspectService:
            this.stringFrom(topology, ["suspectService", "suspect_service", "apm.suspectService"]) ??
            topologyServices[0] ??
            merged.suspectService,
          affectedTransactions: this.arrayFrom(topology, ["affectedTransactions", "transactions"]) ?? merged.affectedTransactions
        };
      } else {
        warnings.push(
          "Topology API responded, but it did not include demo service names."
        );
      }
    }

    return {
      ...merged,
      apiBacked: sources.length > 0,
      sources,
      warnings
    };
  }

  async explainEvidence(evidence: EvidenceBundle) {
    return {
      businessTransaction: evidence.browserExperience.affectedJourney,
      confidenceBand: evidence.investigation.confidenceBand,
      suspectService: evidence.serviceImpact.suspectService,
      summary: evidence.investigation.likelyCause
    };
  }

  private buildFallback(payload: DetectorWebhookPayload): SplunkEnrichmentResult {
    return {
      apiBacked: false,
      sources: [],
      warnings: this.accessToken
        ? ["Splunk enrichment did not return complete incident context."]
        : ["SPLUNK_ACCESS_TOKEN not configured; live Splunk enrichment is unavailable."],
      affectedServices: payload.dimensions?.service ? [payload.dimensions.service] : ["claims-knowledge"],
      suspectService: payload.dimensions?.service ?? "claims-knowledge",
      affectedTransactions: payload.dimensions?.transaction ? [payload.dimensions.transaction] : undefined
    };
  }

  private resolvePath(template: string | undefined, payload: DetectorWebhookPayload) {
    if (!template) {
      return undefined;
    }

    return template
      .replaceAll("{detectorId}", encodeURIComponent(payload.detectorId))
      .replaceAll("{incidentId}", encodeURIComponent(payload.incidentId ?? ""))
      .replaceAll("{severity}", encodeURIComponent(payload.severity));
  }

  private async fetchCandidateJson(path: string | undefined, warnings: string[]) {
    if (!path) {
      return null;
    }

    const url = path.startsWith("http") ? path : `${this.baseUrl}${path}`;
    try {
      const request = this.buildRequest(url);
      const response = await fetch(url, request);

      if (!response.ok) {
        warnings.push(`Splunk API ${url} returned ${response.status}.`);
        return null;
      }

      return response.json();
    } catch (error) {
      warnings.push(
        `Splunk API ${url} failed: ${error instanceof Error ? error.message : "unknown error"}.`
      );
      return null;
    }
  }

  private buildRequest(url: string) {
    if (url.endsWith("/v2/apm/topology")) {
      const end = new Date();
      const start = new Date(end.getTime() - 15 * 60 * 1000);
      return {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "x-sf-token": this.accessToken
        },
        body: JSON.stringify({
          timeRange: `${start.toISOString().replace(".000", "")}/${end.toISOString().replace(".000", "")}`
        })
      };
    }

    return {
      headers: {
        "content-type": "application/json",
        "x-sf-token": this.accessToken
      }
    };
  }

  private stringFrom(payload: unknown, paths: string[]) {
    for (const path of paths) {
      const value = this.valueAtPath(payload, path);
      if (typeof value === "string" && value.length > 0) {
        return value;
      }
    }

    return undefined;
  }

  private numberFrom(payload: unknown, paths: string[]) {
    for (const path of paths) {
      const value = this.valueAtPath(payload, path);
      if (typeof value === "number") {
        return value;
      }
      if (typeof value === "string" && value.length > 0 && !Number.isNaN(Number(value))) {
        return Number(value);
      }
    }

    return undefined;
  }

  private arrayFrom(payload: unknown, paths: string[]) {
    for (const path of paths) {
      const value = this.valueAtPath(payload, path);
      if (Array.isArray(value)) {
        return value.filter((item): item is string => typeof item === "string");
      }
    }

    return undefined;
  }

  private valueAtPath(payload: unknown, path: string) {
    if (!payload || typeof payload !== "object") {
      return undefined;
    }

    return path.split(".").reduce<unknown>((current, segment) => {
      if (!current || typeof current !== "object") {
        return undefined;
      }
      return (current as Record<string, unknown>)[segment];
    }, payload);
  }

  private topologyNodeServices(payload: unknown) {
    const nodes = this.valueAtPath(payload, "data.nodes");
    if (!Array.isArray(nodes)) {
      return undefined;
    }

    return nodes
      .map((node) =>
        node && typeof node === "object" && typeof (node as Record<string, unknown>).serviceName === "string"
          ? ((node as Record<string, unknown>).serviceName as string)
          : undefined
      )
      .filter((service): service is string => typeof service === "string")
      .slice(0, 10);
  }
}
