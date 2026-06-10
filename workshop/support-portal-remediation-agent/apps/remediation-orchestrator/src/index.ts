import cors from "@fastify/cors";
import Fastify from "fastify";
import { timingSafeEqual } from "node:crypto";
import { defaultPorts, localServicePort, localServiceUrl } from "@ibobs/runtime-config";
import { parseAssistantEvidence } from "@ibobs/evidence-parser";
import { evaluatePolicy } from "@ibobs/policy-engine";
import {
  ACTION_TYPES,
  BUSINESS_TRANSACTIONS,
  POLICY_MODES,
  getIncident,
  listIncidents,
  listWebhookReceipts,
  resetIncidents,
  resetWebhookReceipts,
  saveIncident,
  saveWebhookReceipt,
  type AssistantEvidenceInput,
  type DetectorWebhookPayload,
  type EvidenceBundle,
  type ProposedAction,
  type WebhookReceipt
} from "@ibobs/shared-types";
import {
  annotateServerEntrySpan,
  annotateCurrentSpan,
  buildNodeTelemetryConfig,
  createServiceLogger,
  initSplunkNodeTelemetry,
  runInSpan
} from "@ibobs/telemetry";
import { RemediationAgentClient } from "./agent-client";
import { SplunkObservabilityClient, type SplunkEnrichmentResult } from "./splunk-client";

async function buildEvidenceBundle(
  input: AssistantEvidenceInput,
  splunkClient: SplunkObservabilityClient,
  detectorPayloadOverride?: DetectorWebhookPayload
): Promise<{ evidence: EvidenceBundle; enrichment: SplunkEnrichmentResult }> {
  const existingIncident = input.incidentId ? getIncident(input.incidentId) : undefined;
  const matchingReceipt = input.incidentId
    ? listWebhookReceipts().find((receipt) => receipt.incidentId === input.incidentId)
    : undefined;
  const detectorPayload: DetectorWebhookPayload =
    detectorPayloadOverride ?? {
      detectorId:
        input.detectorId ??
        existingIncident?.detectorId ??
        matchingReceipt?.detectorId ??
        "detector-demo-001",
      detectorName:
        existingIncident?.detectorName ??
        matchingReceipt?.detectorName ??
        "Claims Knowledge Cache Volume Pressure",
      severity: "critical",
      triggeredAt: new Date().toISOString(),
      incidentId: input.incidentId,
      dimensions: {
        service: "claims-knowledge",
        environment: "demo"
      }
    };
  const enrichment = await splunkClient.enrichDetector(detectorPayload);
  const rawText = (input.rawText ?? input.assistantResponseText ?? "").trim();
  const parsed = parseAssistantEvidence({
    ...input,
    rawText: rawText || enrichment.assistantSummary || ""
  });
  const liveEvidenceAvailable = enrichment.apiBacked || rawText.length > 0;

  return {
    evidence: {
      incidentId: input.incidentId ?? detectorPayload.incidentId ?? "incident-demo-001",
      scenarioId: "cache-disk-pressure",
      detector: {
        detectorId: detectorPayload.detectorId,
        detectorName: detectorPayload.detectorName,
        severity: detectorPayload.severity,
        triggeredAt: detectorPayload.triggeredAt,
        dimensions: detectorPayload.dimensions ?? {}
      },
      browserExperience: {
        affectedSessions: enrichment.affectedSessions,
        frustrationSignals: ["rage_click", "error_click"],
        sessionReplayUrl: enrichment.sessionReplayUrl,
        affectedJourney: BUSINESS_TRANSACTIONS.customerSupportResponse
      },
      serviceImpact: {
        affectedServices: enrichment.affectedServices,
        suspectService: enrichment.suspectService,
        p95LatencyMs: enrichment.p95LatencyMs,
        errorRate: enrichment.errorRate,
        affectedTransactions:
          (enrichment.affectedTransactions as EvidenceBundle["serviceImpact"]["affectedTransactions"] | undefined) ??
          [BUSINESS_TRANSACTIONS.customerSupportResponse]
      },
      investigation: {
        likelyCause:
          rawText.length > 0
            ? parsed.likelyCause
            : enrichment.likelyCause ??
              (liveEvidenceAvailable
                ? parsed.likelyCause
                : "Live Splunk evidence was not available; keep remediation recommendation-only until signals are verified."),
        recentChange: enrichment.recentChange,
        confidenceBand:
          rawText.length > 0
            ? parsed.confidenceBand
            : enrichment.confidenceBand ?? (liveEvidenceAvailable ? parsed.confidenceBand : "low")
      },
      approvalEvidence: enrichment.approvalEvidence,
      candidateActions: parsed.candidateActions as (typeof ACTION_TYPES)[keyof typeof ACTION_TYPES][],
      sourceNotes: {
        assistantSummary: rawText || enrichment.assistantSummary,
        enrichmentApplied: enrichment.apiBacked,
        apiEnrichmentSources: enrichment.sources,
        enrichmentWarnings: enrichment.warnings,
        observabilityResources: enrichment.observabilityResources,
        traceIds: enrichment.traceIds
      }
    },
    enrichment
  };
}

function normalizeAssistantInput(input: AssistantEvidenceInput): AssistantEvidenceInput {
  return {
    source: input.source ?? "splunk_ai_assistant",
    rawText: input.rawText ?? input.assistantResponseText ?? "",
    pastedBy: input.pastedBy ?? "operator",
    pastedAt: input.pastedAt ?? new Date().toISOString(),
    detectorId: input.detectorId,
    incidentId: input.incidentId
  };
}

async function intakeAssistantEvidence(
  input: AssistantEvidenceInput,
  splunkClient: SplunkObservabilityClient
) {
  const normalizedInput = normalizeAssistantInput(input);
  const { evidence, enrichment } = await buildEvidenceBundle(normalizedInput, splunkClient);
  const policy = evaluatePolicy(evidence);

  return {
    evidence,
    enrichment,
    policy
  };
}

function buildIncidentFromWebhook(payload: DetectorWebhookPayload) {
  const incidentId = payload.incidentId ?? `incident-${Date.now()}`;

  return saveIncident({
    incidentId,
    scenarioId: "cache-disk-pressure",
    businessTransaction: BUSINESS_TRANSACTIONS.customerSupportResponse,
    detectorId: payload.detectorId,
    detectorName: payload.detectorName,
    status: "open"
  });
}

function normalizeSeverity(value: unknown): DetectorWebhookPayload["severity"] {
  const normalized = typeof value === "string" ? value.toLowerCase() : "";
  if (normalized === "info" || normalized === "warning" || normalized === "critical") {
    return normalized;
  }
  if (normalized === "major" || normalized === "minor") {
    return "warning";
  }
  return "critical";
}

function normalizeDetectorWebhookPayload(input: unknown): DetectorWebhookPayload {
  const payload = (input ?? {}) as Record<string, unknown>;
  const detectorId =
    (typeof payload.detectorId === "string" && payload.detectorId) ||
    (typeof payload.detector_id === "string" && payload.detector_id) ||
    (typeof payload.incidentId === "string" && payload.incidentId) ||
    `detector-${Date.now()}`;
  const detectorName =
    (typeof payload.detectorName === "string" && payload.detectorName) ||
    (typeof payload.detector === "string" && payload.detector) ||
    (typeof payload.rule === "string" && payload.rule) ||
    "Splunk Detector Alert";
  const triggeredAt =
    (typeof payload.triggeredAt === "string" && payload.triggeredAt) ||
    (typeof payload.alertTimestamp === "string" && payload.alertTimestamp) ||
    new Date().toISOString();
  const incidentId =
    (typeof payload.incidentId === "string" && payload.incidentId) ||
    (typeof payload.eventType === "string" && payload.eventType) ||
    undefined;

  const dimensions: Record<string, string> = {
    service:
      (typeof payload.service === "string" && payload.service) ||
      (typeof payload["service.name"] === "string" && (payload["service.name"] as string)) ||
      "claims-portal-api",
    environment:
      (typeof payload.environment === "string" && payload.environment) ||
      (typeof payload["deployment.environment"] === "string" && (payload["deployment.environment"] as string)) ||
      "demo"
  };

  return {
    detectorId,
    detectorName,
    severity: normalizeSeverity(payload.severity),
    triggeredAt,
    incidentId,
    dimensions
  };
}

function buildWebhookReceipt(input: unknown, payload: DetectorWebhookPayload, sourceHost?: string): WebhookReceipt {
  const raw = (input ?? {}) as Record<string, unknown>;

  return {
    receiptId: `receipt-${Date.now()}`,
    receivedAt: new Date().toISOString(),
    sourceHost,
    detectorId: payload.detectorId,
    detectorName: payload.detectorName,
    incidentId: payload.incidentId,
    severity: payload.severity,
    triggeredAt: payload.triggeredAt,
    eventType: typeof raw.eventType === "string" ? raw.eventType : undefined,
    status: typeof raw.status === "string" ? raw.status : undefined,
    dimensions: payload.dimensions
  };
}

function isValidWebhookSecret(providedSecret: string | undefined, configuredSecret: string) {
  if (!providedSecret) {
    return false;
  }

  const left = Buffer.from(providedSecret);
  const right = Buffer.from(configuredSecret);

  if (left.length !== right.length) {
    return false;
  }

  return timingSafeEqual(left, right);
}

export function buildServer() {
  const app = Fastify({ loggerInstance: createServiceLogger("remediation-orchestrator") });
  void buildNodeTelemetryConfig({ serviceName: "remediation-orchestrator" });
  void app.register(cors, {
    origin: true,
    allowedHeaders: ["content-type", "traceparent", "tracestate", "baggage", "x-ibobs-webhook-secret"],
    exposedHeaders: ["Server-Timing"]
  });
  app.addHook("preHandler", async (request) => {
    annotateServerEntrySpan({
      method: request.method,
      route: request.routeOptions.url
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
  const splunkClient = new SplunkObservabilityClient(
    process.env.SPLUNK_API_BASE_URL ?? "https://api.us1.signalfx.com",
    process.env.SPLUNK_ACCESS_TOKEN ?? ""
  );
  const agentClient = new RemediationAgentClient(
    localServiceUrl(process.env, {
      baseUrlEnvVar: "REMEDIATION_AGENT_BASE_URL",
      portEnvVar: "REMEDIATION_AGENT_PORT",
      defaultPort: defaultPorts.remediationAgent
    })
  );
  const webhookSharedSecret = process.env.SPLUNK_WEBHOOK_SHARED_SECRET;

  async function openIncidentFromDetector(payload: DetectorWebhookPayload) {
    const incident = buildIncidentFromWebhook(payload);
    const { evidence, enrichment } = await runInSpan(
      "splunk.enrich_detector",
      {
        "incident.id": incident.incidentId,
        "app.business_transaction": incident.businessTransaction,
        "o11y.detector_id": payload.detectorId
      },
      () =>
        buildEvidenceBundle(
          {
            source: "splunk_mcp",
            rawText: "",
            pastedBy: "mcp",
            pastedAt: new Date().toISOString(),
            incidentId: incident.incidentId,
            detectorId: payload.detectorId
          },
          splunkClient,
          {
            ...payload,
            incidentId: incident.incidentId
          }
        )
    );
    const policy = evaluatePolicy(evidence);
    const enrichedIncident = saveIncident({
      ...incident,
      evidence
    });
    return {
      incident: enrichedIncident,
      enrichment,
      evidence,
      policy
    };
  }

  app.get("/remediation/health", async () => ({
    status: "ok",
    service: "remediation-orchestrator"
  }));

  app.get("/remediation/agent-monitoring", async () => {
    const agentHealth = await agentClient.health();
    const apiKeySource = process.env.GALILEO_API_KEY
      ? "environment"
      : process.env.GALILEO_API_KEY_FILE
        ? "file"
        : "missing";
    const agentMonitoring = "agentMonitoring" in agentHealth ? agentHealth.agentMonitoring : "unavailable";
    const agentReportsGalileoReady = agentMonitoring === "galileo";

    return {
      status: agentReportsGalileoReady ? "ready" : "not_ready",
      provider: "galileo",
      project: process.env.GALILEO_PROJECT ?? "ciscolive26",
      logStream: process.env.GALILEO_LOG_STREAM ?? "remediation-agent",
      consoleUrl: process.env.GALILEO_CONSOLE_URL || "https://app.galileo.ai",
      apiKeyConfigured: apiKeySource !== "missing" || agentReportsGalileoReady,
      apiKeySource: apiKeySource === "missing" && agentReportsGalileoReady ? "agent" : apiKeySource,
      agent: agentHealth,
      remediationInstrumentation: [
        {
          stage: "evaluate",
          spanType: "agent",
          spanName: "remediation.evaluate",
          route: "POST /agent/evaluate"
        },
        {
          stage: "execute",
          spanType: "tool",
          spanName: "remediation.execute_action",
          route: "POST /agent/execute/:actionId"
        },
        {
          stage: "verify",
          spanType: "tool",
          spanName: "remediation.verify_recovery",
          route: "POST /agent/verify/:actionId"
        }
      ],
      showcaseInstrumentation: [
        {
          stage: "intake",
          spanType: "workflow",
          spanName: "showcase.incident_intake",
          purpose: "Open the incident story and customer impact."
        },
        {
          stage: "retrieve",
          spanType: "retriever",
          spanName: "showcase.retrieve_observability_context",
          purpose: "Show evidence documents and source metadata."
        },
        {
          stage: "triage",
          spanType: "agent",
          spanName: "showcase.triage_agent",
          purpose: "Explain trusted evidence and missing signals."
        },
        {
          stage: "hypothesize",
          spanType: "agent",
          spanName: "showcase.hypothesis_agent",
          purpose: "Compare root-cause hypotheses."
        },
        {
          stage: "protect",
          spanType: "tool",
          spanName: "showcase.guardrail_pre_action_check",
          purpose: "Show the unsafe restart instruction being blocked."
        },
        {
          stage: "plan",
          spanType: "agent",
          spanName: "showcase.action_planning_agent",
          purpose: "Choose a bounded remediation action."
        },
        {
          stage: "approval",
          spanType: "tool",
          spanName: "showcase.human_approval",
          purpose: "Record human approval."
        },
        {
          stage: "execute",
          spanType: "tool",
          spanName: "showcase.execute_remediation",
          purpose: "Apply the cache cleanup."
        },
        {
          stage: "verify",
          spanType: "tool",
          spanName: "showcase.verify_recovery",
          purpose: "Validate recovery with a live request."
        },
        {
          stage: "postmortem",
          spanType: "agent",
          spanName: "showcase.postmortem_agent",
          purpose: "Generate the audit summary."
        }
      ]
    };
  });

  app.post("/remediation/galileo/showcase", async (request) => {
    const payload = request.body as {
      incidentId?: string;
      executeRemediation?: boolean;
      includeUnsafeOperatorNote?: boolean;
    };
    request.log.info({ payload }, "running galileo showcase scenario");

    return runInSpan(
      "remediation.galileo_showcase",
      {
        "incident.id": payload.incidentId ?? "galileo-showcase",
        "app.business_transaction": BUSINESS_TRANSACTIONS.customerSupportResponse,
        "agent.monitoring.provider": "galileo"
      },
      () => agentClient.runGalileoShowcase(payload)
    );
  });

  app.get("/remediation/incidents", async () => listIncidents());

  app.get("/remediation/webhook-receipts", async () => listWebhookReceipts());

  app.post("/remediation/reset", async (request) => {
    const incidentsCleared = resetIncidents();
    const webhookReceiptsCleared = resetWebhookReceipts();
    request.log.info({ incidentsCleared, webhookReceiptsCleared }, "remediation flow reset");
    return {
      status: "reset",
      incidentsCleared,
      webhookReceiptsCleared
    };
  });

  app.get("/remediation/incidents/:incidentId", async (request, reply) => {
    const incident = getIncident((request.params as { incidentId: string }).incidentId);
    if (!incident) {
      reply.code(404);
      return { error: "Incident not found" };
    }
    return incident;
  });

  app.post("/webhooks/splunk/detector", async (request, reply) => {
    if (webhookSharedSecret) {
      const providedSecret = request.headers["x-ibobs-webhook-secret"];
      const normalizedSecret =
        typeof providedSecret === "string" ? providedSecret : Array.isArray(providedSecret) ? providedSecret[0] : undefined;

      if (!isValidWebhookSecret(normalizedSecret, webhookSharedSecret)) {
        reply.code(401);
        return {
          error: "Invalid webhook secret"
        };
      }
    }

    const payload = normalizeDetectorWebhookPayload(request.body);
    const receipt = saveWebhookReceipt(
      buildWebhookReceipt(
        request.body,
        payload,
        typeof request.headers.host === "string" ? request.headers.host : undefined
      )
    );
    request.log.info(
      {
        webhookReceipt: {
          receiptId: receipt.receiptId,
          detectorId: receipt.detectorId,
          incidentId: receipt.incidentId,
          eventType: receipt.eventType,
          status: receipt.status
        }
      },
      "webhook receipt recorded"
    );
    return openIncidentFromDetector(payload);
  });

  app.post("/remediation/demo/incidents", async (request) => {
    const payload = normalizeDetectorWebhookPayload(request.body);
    request.log.info(
      {
        detectorId: payload.detectorId,
        detectorName: payload.detectorName
      },
      "opening local demo incident"
    );
    return openIncidentFromDetector(payload);
  });

  app.post("/remediation/context", async (request) => {
    const payload = request.body as AssistantEvidenceInput;
    request.log.info({ assistantEvidence: payload }, "building remediation context");
    const existingIncident = payload.incidentId ? getIncident(payload.incidentId) : undefined;
    const result = await runInSpan(
      "remediation.context_build",
      {
        "incident.id": payload.incidentId ?? "incident-demo-001",
        "app.business_transaction": BUSINESS_TRANSACTIONS.customerSupportResponse
      },
      () => intakeAssistantEvidence(payload, splunkClient)
    );
    const incident = saveIncident({
      incidentId: result.evidence.incidentId,
      scenarioId: result.evidence.scenarioId,
      businessTransaction: result.evidence.browserExperience.affectedJourney,
      detectorId: existingIncident?.detectorId,
      detectorName: existingIncident?.detectorName,
      status: "proposed",
      evidence: result.evidence
    });

    return {
      incident,
      evidence: result.evidence,
      enrichment: result.enrichment,
      policy: result.policy
    };
  });

  app.post("/remediation/explain", async (request) => {
    const payload = request.body as AssistantEvidenceInput;
    request.log.info({ assistantEvidence: payload }, "explaining remediation evidence");
    const existingIncident = payload.incidentId ? getIncident(payload.incidentId) : undefined;
    if ((!payload.rawText && !payload.assistantResponseText) && existingIncident?.evidence) {
      return splunkClient.explainEvidence(existingIncident.evidence);
    }

    const { evidence } = await intakeAssistantEvidence(payload, splunkClient);
    return splunkClient.explainEvidence(evidence);
  });

  app.post("/remediation/propose", async (request, reply) => {
    const payload = request.body as AssistantEvidenceInput;
    request.log.info({ assistantEvidence: payload }, "proposing remediation action");
    const existingIncident = payload.incidentId ? getIncident(payload.incidentId) : undefined;

    if ((!payload.rawText && !payload.assistantResponseText) && existingIncident?.evidence) {
      const evidence = existingIncident.evidence;
      const policy = evaluatePolicy(evidence);
      annotateCurrentSpan({
        "app.policy_mode": policy.policyMode,
        "app.enrichment_applied": evidence.sourceNotes.enrichmentApplied
      });

      const proposedAction = await runInSpan(
        "remediation.agent_evaluate",
        {
          "incident.id": evidence.incidentId,
          "app.business_transaction": evidence.browserExperience.affectedJourney,
          "app.policy_mode": policy.policyMode
        },
        () => agentClient.evaluate(evidence, policy.policyMode)
      );

      saveIncident({
        incidentId: evidence.incidentId,
        scenarioId: evidence.scenarioId,
        businessTransaction: evidence.browserExperience.affectedJourney,
        detectorId: existingIncident.detectorId,
        detectorName: existingIncident.detectorName,
        status: "proposed",
        evidence,
        proposedAction
      });

      return {
        proposedAction,
        evidence,
        policy
      };
    }

    const result = await runInSpan(
      "remediation.propose_action",
      {
        "incident.id": payload.incidentId ?? "incident-demo-001",
        "app.business_transaction": BUSINESS_TRANSACTIONS.customerSupportResponse
      },
      () => intakeAssistantEvidence(payload, splunkClient)
    );
    annotateCurrentSpan({
      "app.policy_mode": result.policy.policyMode,
      "app.enrichment_applied": result.evidence.sourceNotes.enrichmentApplied
    });

    if (!result.policy.eligible && result.policy.policyMode === POLICY_MODES.recommendOnly) {
      reply.code(202);
      const fallbackAction: ProposedAction = {
        actionId: `action-${Date.now()}`,
        incidentId: result.evidence.incidentId,
        type: result.evidence.candidateActions[0],
        target: "claims-knowledge-cache",
        confidenceBand: result.evidence.investigation.confidenceBand,
        policyMode: result.policy.policyMode,
        reasoningSummary: "Policy limited this incident to recommendation-only handling.",
        validationPlan: ["Escalate to operator review", "Confirm filesystem pressure drops before execution"],
        status: "proposed"
      };

      saveIncident({
        incidentId: result.evidence.incidentId,
        scenarioId: result.evidence.scenarioId,
        businessTransaction: result.evidence.browserExperience.affectedJourney,
        detectorId: existingIncident?.detectorId,
        detectorName: existingIncident?.detectorName,
        status: "proposed",
        evidence: result.evidence,
        proposedAction: fallbackAction
      });

      return {
        proposedAction: fallbackAction,
        evidence: result.evidence,
        policy: result.policy
      };
    }

    const proposedAction = await runInSpan(
      "remediation.agent_evaluate",
      {
        "incident.id": result.evidence.incidentId,
        "app.business_transaction": result.evidence.browserExperience.affectedJourney,
        "app.policy_mode": result.policy.policyMode
      },
      () => agentClient.evaluate(result.evidence, result.policy.policyMode)
    );

    saveIncident({
      incidentId: result.evidence.incidentId,
      scenarioId: result.evidence.scenarioId,
      businessTransaction: result.evidence.browserExperience.affectedJourney,
      detectorId: existingIncident?.detectorId,
      detectorName: existingIncident?.detectorName,
      status: "proposed",
      evidence: result.evidence,
      proposedAction
    });

    return {
      proposedAction,
      evidence: result.evidence,
      policy: result.policy
    };
  });

  app.post("/remediation/approve/:actionId", async (request, reply) => {
    const actionId = (request.params as { actionId: string }).actionId;
    const incidentId = (request.body as { incidentId?: string }).incidentId;
    request.log.info({ actionId, incidentId }, "approving remediation action");
    if (!incidentId) {
      reply.code(400);
      return { error: "incidentId is required" };
    }

    const incident = getIncident(incidentId);
    if (!incident?.proposedAction) {
      reply.code(404);
      return { error: "Proposed action not found for incident" };
    }
    if (incident.proposedAction.policyMode !== POLICY_MODES.approvalRequired) {
      reply.code(409);
      return {
        error: `Action is ${incident.proposedAction.policyMode} and cannot be executed from the approval endpoint.`,
        incident
      };
    }

    const approvedAt = new Date().toISOString();
    const approvedAction: ProposedAction = {
      ...incident.proposedAction,
      status: "approved"
    };
    saveIncident({
      ...incident,
      status: "approved",
      proposedAction: approvedAction,
      approvedAt
    });

    saveIncident({
      ...incident,
      status: "executing",
      proposedAction: approvedAction,
      approvedAt
    });
    const executeResult = await runInSpan(
      "remediation.execute_action",
      {
        "incident.id": incidentId,
        "action.id": actionId,
        "action.type": approvedAction.type
      },
      () => agentClient.execute(approvedAction)
    );
    const executedAt = new Date().toISOString();
    const verifyResult =
      executeResult.status === "executed"
        ? await runInSpan(
            "remediation.verify_action",
            {
              "incident.id": incidentId,
              "action.id": actionId,
              "action.type": approvedAction.type
            },
            () => agentClient.verify(approvedAction)
          )
        : {
            actionId,
            actionType: approvedAction.type,
            status: "failed" as const,
            scenarioState: executeResult.scenarioState ?? "unknown",
            notes: ["Verification skipped because execution failed."]
          };
    const verifiedAt = new Date().toISOString();

    const updatedAction: ProposedAction = {
      ...approvedAction,
      status:
        verifyResult.status === "validated"
          ? "validated"
          : executeResult.status === "executed"
            ? "executed"
            : "rejected"
    };

    saveIncident({
      ...incident,
      status:
        verifyResult.status === "validated"
          ? "validated"
          : executeResult.status === "executed"
            ? "approved"
            : "open",
      proposedAction: updatedAction,
      executeResult,
      verifyResult,
      approvedAt,
      executedAt,
      verifiedAt
    });

    return {
      approved: true,
      actionId,
      incident: getIncident(incidentId),
      executeResult,
      verifyResult,
      incidentId
    };
  });

  app.get("/remediation/actions/:actionId", async (request) => {
    const actionId = (request.params as { actionId: string }).actionId;
    request.log.info({ actionId }, "fetching remediation action");
    const actionOwner = listIncidents().find((incident) => incident.proposedAction?.actionId === actionId);
    return actionOwner?.proposedAction ?? { actionId, status: "unknown" };
  });

  return app;
}

const demoInput: AssistantEvidenceInput = {
  source: "splunk_ai_assistant",
  rawText:
    "High confidence that claims-knowledge cache filesystem pressure degraded the AI Claim Status transaction. Disk utilization for the cache mount is above threshold and APM shows claims-knowledge latency. Recommended action: clean_claims_knowledge_cache.",
  pastedBy: "operator",
  pastedAt: new Date().toISOString()
};

if (process.env.NODE_ENV !== "test") {
  initSplunkNodeTelemetry("remediation-orchestrator");
  const port = localServicePort(process.env, "ORCHESTRATOR_PORT", defaultPorts.orchestrator);
  const server = buildServer();
  server.log.info({ demoInput }, "remediation-orchestrator scaffold ready");
  server.listen({ port, host: "0.0.0.0" }).catch((error) => {
    server.log.error(error);
    process.exit(1);
  });
}
