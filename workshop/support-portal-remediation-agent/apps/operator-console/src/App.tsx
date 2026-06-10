import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  BadgeCheck,
  Bot,
  CheckCircle2,
  ClipboardCheck,
  Clock3,
  FileText,
  Gauge,
  HardDrive,
  KeyRound,
  ListChecks,
  Play,
  Radar,
  RefreshCw,
  RotateCcw,
  ShieldCheck,
  Sparkles,
  TerminalSquare,
  Zap
} from "lucide-react";
import { currentBrowserAppConfig } from "@ibobs/runtime-config/browser";
import "./App.css";

const exampleAssistantOutput = "";

type EvidenceMetricStatus = "confirmed" | "not_confirmed" | "unavailable" | string;

type EvidenceMetric = {
  label: string;
  source: string;
  metricName?: string;
  value?: number;
  unit?: string;
  threshold?: number;
  status: EvidenceMetricStatus;
  detail: string;
};

type ImpactChainStep = {
  stage: string;
  label: string;
  detail: string;
  status: EvidenceMetricStatus;
};

type ApprovalEvidence = {
  customerImpact?: EvidenceMetric[];
  backendImpact?: EvidenceMetric[];
  infrastructureImpact?: EvidenceMetric[];
  impactChain?: ImpactChainStep[];
};

type OrchestratorResponse = {
  incident?: {
    incidentId: string;
    detectorId?: string;
    detectorName?: string;
    status?: string;
    businessTransaction?: string;
    approvedAt?: string;
    executedAt?: string;
    verifiedAt?: string;
  };
  enrichment?: {
    apiBacked?: boolean;
    sources?: string[];
    warnings?: string[];
    affectedServices?: string[];
    suspectService?: string;
    affectedTransactions?: string[];
  };
  evidence?: {
    browserExperience?: {
      affectedSessions?: number;
      affectedJourney?: string;
      sessionReplayUrl?: string;
    };
    serviceImpact?: {
      affectedServices?: string[];
      suspectService?: string;
      p95LatencyMs?: number;
      errorRate?: number;
      affectedTransactions?: string[];
    };
    investigation?: {
      recentChange?: string;
      confidenceBand?: string;
    };
    approvalEvidence?: ApprovalEvidence;
    sourceNotes?: {
      enrichmentApplied?: boolean;
      apiEnrichmentSources?: string[];
      enrichmentWarnings?: string[];
      observabilityResources?: Array<{
        type: string;
        name: string;
        detail?: string;
        url?: string;
      }>;
      traceIds?: string[];
    };
  };
  policy?: {
    eligible?: boolean;
    policyMode?: string;
    reason?: string;
  };
  proposedAction?: {
    actionId?: string;
    type?: string;
    target?: string;
    confidenceBand?: string;
    policyMode?: string;
    reasoningSummary?: string;
    validationPlan?: string[];
    status?: string;
  };
  approved?: boolean;
  actionId?: string;
  verifyResult?: {
    status?: string;
    scenarioState?: string;
    measuredLatencyMs?: number;
    latencyThresholdMs?: number;
    supportRequestStatus?: number;
    notes?: string[];
  };
  executeResult?: {
    status?: string;
    scenarioState?: string;
    actionType?: string;
    target?: string;
    notes?: string[];
  };
  sessionId?: string;
  project?: string;
  logStream?: string;
  story?: string[];
  showcaseTraces?: Array<{
    name: string;
    type: string;
    includesProtectSpan?: boolean;
    enabled?: boolean;
  }>;
  guardrail?: {
    status?: string;
    unsafeRestartInstruction?: boolean;
    syntheticPiiDetected?: boolean;
    nextAction?: string;
  };
  plan?: {
    recommendedAction?: string;
    target?: string;
    needsApproval?: boolean;
    reasoningSummary?: string;
  };
  verification?: {
    status?: string;
    measuredLatencyMs?: number;
    latencyThresholdMs?: number;
  };
  postmortem?: {
    summary?: string;
    auditOutcome?: string;
    governanceHighlights?: string[];
  };
  demoGuide?: string[];
};

type StoredIncident = {
  incidentId: string;
  detectorId?: string;
  detectorName?: string;
  status?: string;
  businessTransaction?: string;
  approvedAt?: string;
  executedAt?: string;
  verifiedAt?: string;
  evidence?: OrchestratorResponse["evidence"];
  proposedAction?: OrchestratorResponse["proposedAction"];
  executeResult?: OrchestratorResponse["executeResult"];
  verifyResult?: OrchestratorResponse["verifyResult"];
};

type WebhookReceipt = {
  incidentId?: string;
  detectorId?: string;
  detectorName?: string;
};

type AgentMonitoringStatus = {
  status: "ready" | "not_ready" | string;
  provider: string;
  project: string;
  logStream: string;
  consoleUrl?: string;
  apiKeyConfigured: boolean;
  apiKeySource: "environment" | "file" | "missing" | string;
  agent: {
    status: string;
    model?: string;
    telemetry?: string;
    agentMonitoring?: string;
    error?: string;
  };
  remediationInstrumentation: Array<{
    stage: string;
    spanType: string;
    spanName: string;
    route: string;
  }>;
  showcaseInstrumentation?: Array<{
    stage: string;
    spanType: string;
    spanName: string;
    purpose: string;
  }>;
};

type CommandAction =
  | "create"
  | "refresh"
  | "explain"
  | "propose"
  | "approve"
  | "showcase"
  | "pressure"
  | "reset"
  | "monitoring"
  | "resetFlow"
  | null;

function readResponse(value: string): OrchestratorResponse | null {
  try {
    return JSON.parse(value) as OrchestratorResponse;
  } catch {
    return null;
  }
}

function formatScenarioLabel(value: string) {
  return value
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function valueOrFallback(value: string | number | undefined | null, fallback = "n/a") {
  return value === undefined || value === null || value === "" ? fallback : String(value);
}

function formatEvidenceValue(value: number | undefined, unit?: string) {
  if (value === undefined) {
    return "not returned";
  }
  const formatted = Number.isInteger(value)
    ? value.toLocaleString()
    : value.toLocaleString(undefined, { maximumFractionDigits: 1 });
  return unit === "%" ? `${formatted}%` : `${formatted}${unit ? ` ${unit}` : ""}`;
}

function statusClass(status: EvidenceMetricStatus | undefined) {
  if (status === "confirmed") {
    return "confirmed";
  }
  if (status === "not_confirmed") {
    return "not-confirmed";
  }
  return "unavailable";
}

function metricStatusLabel(status: EvidenceMetricStatus | undefined) {
  if (status === "confirmed") {
    return "Confirmed";
  }
  if (status === "not_confirmed") {
    return "Below threshold";
  }
  return "Missing";
}

function chainStatusLabel(status: EvidenceMetricStatus | undefined) {
  if (status === "confirmed") {
    return "Confirmed";
  }
  if (status === "not_confirmed") {
    return "Unconfirmed";
  }
  return "Missing";
}

function formatCommandError(error: unknown) {
  const message = error instanceof Error ? error.message : String(error);
  return message === "Failed to fetch" ? "Backend services unavailable." : message;
}

function CommandButton({
  children,
  icon: Icon,
  onClick,
  disabled,
  variant = "secondary"
}: {
  children: string;
  icon: typeof Play;
  onClick: () => void;
  disabled?: boolean;
  variant?: "primary" | "secondary" | "danger" | "approve";
}) {
  return (
    <button className={`button button-${variant}`} onClick={onClick} disabled={disabled}>
      <Icon size={17} aria-hidden="true" />
      <span>{children}</span>
    </button>
  );
}

function MetricTile({
  label,
  value,
  icon: Icon,
  tone = "neutral"
}: {
  label: string;
  value: string | number;
  icon: typeof Activity;
  tone?: "neutral" | "healthy" | "risk" | "action";
}) {
  return (
    <article className={`metric-tile metric-${tone}`}>
      <Icon size={20} aria-hidden="true" />
      <div>
        <span>{label}</span>
        <strong>{value}</strong>
      </div>
    </article>
  );
}

function EvidenceMetricGroup({
  title,
  icon: Icon,
  metrics = []
}: {
  title: string;
  icon: typeof Activity;
  metrics?: EvidenceMetric[];
}) {
  if (metrics.length === 0) {
    return null;
  }

  return (
    <div className="evidence-proof-card">
      <div className="evidence-card-heading">
        <Icon size={18} aria-hidden="true" />
        <h3>{title}</h3>
      </div>
      <ul className="evidence-metric-list">
        {metrics.map((metric) => (
          <li key={`${metric.source}-${metric.label}`}>
            <div className="evidence-metric-heading">
              <span>{metric.source}</span>
              <strong>{metric.label}</strong>
              <em className={`evidence-status status-${statusClass(metric.status)}`}>
                {metricStatusLabel(metric.status)}
              </em>
            </div>
            <div className="evidence-metric-value">
              <b>{formatEvidenceValue(metric.value, metric.unit)}</b>
              {metric.threshold !== undefined ? (
                <span>Threshold {formatEvidenceValue(metric.threshold, metric.unit)}</span>
              ) : null}
            </div>
            {metric.metricName ? <code>{metric.metricName}</code> : null}
            <p>{metric.detail}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function App() {
  const { orchestratorBaseUrl, scenarioControllerBaseUrl } = currentBrowserAppConfig();
  const [assistantSummary, setAssistantSummary] = useState(exampleAssistantOutput);
  const [incidentId, setIncidentId] = useState("");
  const [result, setResult] = useState<string>("No incident loaded yet.");
  const [scenarioState, setScenarioState] = useState("healthy");
  const [busyAction, setBusyAction] = useState<CommandAction>(null);
  const [commandMessage, setCommandMessage] = useState("Ready for incident intake.");
  const [lastUpdated, setLastUpdated] = useState("Not refreshed");
  const [agentMonitoring, setAgentMonitoring] = useState<AgentMonitoringStatus | null>(null);
  const parsedResult = readResponse(result);

  async function runCommand(action: Exclude<CommandAction, null>, label: string, fn: () => Promise<void>) {
    setBusyAction(action);
    setCommandMessage(label);

    try {
      await fn();
      setCommandMessage(`${label} complete.`);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (error) {
      const message = formatCommandError(error);
      setCommandMessage(message);
      setResult(JSON.stringify({ error: message }, null, 2));
    } finally {
      setBusyAction(null);
    }
  }

  function handlePassiveRefreshError(error: unknown) {
    setCommandMessage(formatCommandError(error));
    setLastUpdated(new Date().toLocaleTimeString());
  }

  async function refreshIncidents() {
    const [incidentsResponse, receiptsResponse] = await Promise.all([
      fetch(`${orchestratorBaseUrl}/remediation/incidents`),
      fetch(`${orchestratorBaseUrl}/remediation/webhook-receipts`)
    ]);
    const incidents = (await incidentsResponse.json()) as StoredIncident[];
    const receipts = (await receiptsResponse.json()) as WebhookReceipt[];
    const latestIncident = incidents.at(-1);

    if (!latestIncident) {
      if (incidentId || readResponse(result)?.incident || readResponse(result)?.evidence) {
        setIncidentId("");
        setResult("No incident loaded yet.");
      }
      return;
    }

    const matchingReceipt = receipts.find((receipt) => receipt.incidentId === latestIncident.incidentId);
    const incidentWithDetector = {
      ...latestIncident,
      detectorId: latestIncident.detectorId ?? matchingReceipt?.detectorId,
      detectorName: latestIncident.detectorName ?? matchingReceipt?.detectorName
    };

    const detailResponse = await fetch(
      `${orchestratorBaseUrl}/remediation/incidents/${encodeURIComponent(incidentWithDetector.incidentId)}`
    );
    const detailedIncident = detailResponse.ok
      ? ((await detailResponse.json()) as StoredIncident)
      : incidentWithDetector;
    const hydratedIncident = {
      ...detailedIncident,
      detectorId: detailedIncident.detectorId ?? incidentWithDetector.detectorId,
      detectorName: detailedIncident.detectorName ?? incidentWithDetector.detectorName
    };

    setIncidentId(hydratedIncident.incidentId);

    setResult((current) => {
      const parsed = readResponse(current);
      if (
        parsed?.incident?.incidentId === hydratedIncident.incidentId &&
        parsed?.incident?.detectorId === hydratedIncident.detectorId &&
        parsed?.incident?.detectorName === hydratedIncident.detectorName &&
        parsed?.proposedAction?.actionId === hydratedIncident.proposedAction?.actionId &&
        parsed?.verifyResult?.status === hydratedIncident.verifyResult?.status
      ) {
        return current;
      }

      return JSON.stringify(
        {
          incident: {
            incidentId: hydratedIncident.incidentId,
            detectorId: hydratedIncident.detectorId,
            detectorName: hydratedIncident.detectorName,
            status: hydratedIncident.status,
            businessTransaction: hydratedIncident.businessTransaction,
            approvedAt: hydratedIncident.approvedAt,
            executedAt: hydratedIncident.executedAt,
            verifiedAt: hydratedIncident.verifiedAt
          },
          evidence: hydratedIncident.evidence,
          proposedAction: hydratedIncident.proposedAction,
          executeResult: hydratedIncident.executeResult,
          verifyResult: hydratedIncident.verifyResult
        },
        null,
        2
      );
    });
  }

  async function refreshAgentMonitoring() {
    const response = await fetch(`${orchestratorBaseUrl}/remediation/agent-monitoring`);
    const payload = (await response.json()) as AgentMonitoringStatus;
    setAgentMonitoring(payload);
  }

  useEffect(() => {
    void refreshScenario().catch(handlePassiveRefreshError);
    void refreshIncidents().catch(handlePassiveRefreshError);
    void refreshAgentMonitoring().catch(handlePassiveRefreshError);

    const intervalId = window.setInterval(() => {
      void refreshScenario().catch(handlePassiveRefreshError);
      void refreshIncidents().catch(handlePassiveRefreshError);
      void refreshAgentMonitoring().catch(handlePassiveRefreshError);
      setLastUpdated(new Date().toLocaleTimeString());
    }, 5000);

    return () => window.clearInterval(intervalId);
  }, []);

  async function createIncident() {
    await runCommand("create", "Creating incident and gathering Splunk MCP evidence", async () => {
      const response = await fetch(`${orchestratorBaseUrl}/remediation/demo/incidents`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          detectorId: "det-frontend-demo",
          detectorName: "Claims Knowledge Cache Volume Pressure",
          severity: "critical",
          triggeredAt: new Date().toISOString(),
          service: "claims-knowledge",
          environment: "demo"
        })
      });
      const payload = await response.json();
      if (!response.ok || !payload.incident?.incidentId) {
        setResult(JSON.stringify(payload, null, 2));
        return;
      }
      setIncidentId(payload.incident.incidentId);
      setResult(JSON.stringify(payload, null, 2));
    });
  }

  async function proposeAction() {
    await runCommand("propose", "Requesting remediation proposal", async () => {
      const operatorNotes = assistantSummary.trim();
      const response = await fetch(`${orchestratorBaseUrl}/remediation/propose`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          source: "splunk_mcp",
          ...(operatorNotes ? { rawText: operatorNotes } : {}),
          pastedBy: "operator",
          pastedAt: new Date().toISOString(),
          incidentId
        })
      });
      const payload = await response.json();
      setResult(JSON.stringify(payload, null, 2));
    });
  }

  async function approveAction() {
    await runCommand("approve", "Approving bounded action", async () => {
      if (!parsedResult) {
        setResult("Current result is not valid JSON.");
        return;
      }

      const actionId = parsedResult.proposedAction?.actionId;
      if (!actionId || !incidentId) {
        setResult("No proposed action available to approve.");
        return;
      }

      const response = await fetch(`${orchestratorBaseUrl}/remediation/approve/${actionId}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ incidentId })
      });
      const payload = await response.json();
      setResult(JSON.stringify(payload, null, 2));
    });
  }

  async function runGalileoShowcase() {
    await runCommand("showcase", "Running Galileo showcase session", async () => {
      const response = await fetch(`${orchestratorBaseUrl}/remediation/galileo/showcase`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          incidentId: `galileo-console-${Date.now()}`,
          executeRemediation: true,
          includeUnsafeOperatorNote: true
        })
      });
      const payload = await response.json();
      setIncidentId(payload.incidentId ?? incidentId);
      setResult(JSON.stringify(payload, null, 2));
    });
  }

  async function resetRemediationFlow() {
    await runCommand("resetFlow", "Resetting remediation flow", async () => {
      const response = await fetch(`${orchestratorBaseUrl}/remediation/reset`, {
        method: "POST"
      });
      const payload = await response.json();
      setIncidentId("");
      setAssistantSummary("");
      setResult(JSON.stringify(payload, null, 2));
    });
  }

  async function explainEvidence() {
    await runCommand("explain", "Explaining evidence package", async () => {
      if (!incidentId) {
        setResult("Create an incident before requesting an explanation.");
        return;
      }

      const operatorNotes = assistantSummary.trim();
      const response = await fetch(`${orchestratorBaseUrl}/remediation/explain`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          source: "splunk_mcp",
          ...(operatorNotes ? { rawText: operatorNotes } : {}),
          pastedBy: "operator",
          pastedAt: new Date().toISOString(),
          incidentId
        })
      });
      const payload = await response.json();
      setResult(JSON.stringify(payload, null, 2));
    });
  }

  async function refreshScenario() {
    const response = await fetch(`${scenarioControllerBaseUrl}/scenario/state`);
    const payload = (await response.json()) as { activeScenario: string };
    setScenarioState(payload.activeScenario);
  }

  async function activateScenario(scenarioId: string) {
    await runCommand("pressure", "Activating cache pressure scenario", async () => {
      const response = await fetch(`${scenarioControllerBaseUrl}/scenario/activate/${scenarioId}`, {
        method: "POST"
      });
      const payload = (await response.json()) as { activeScenario: string };
      setScenarioState(payload.activeScenario);
    });
  }

  async function resetScenario() {
    await runCommand("reset", "Resetting scenario", async () => {
      const response = await fetch(`${scenarioControllerBaseUrl}/scenario/reset`, {
        method: "POST"
      });
      const payload = (await response.json()) as { activeScenario: string };
      setScenarioState(payload.activeScenario);
    });
  }

  const enrichmentWarnings =
    parsedResult?.evidence?.sourceNotes?.enrichmentWarnings ?? parsedResult?.enrichment?.warnings ?? [];
  const enrichmentSources =
    parsedResult?.evidence?.sourceNotes?.apiEnrichmentSources ?? parsedResult?.enrichment?.sources ?? [];
  const observabilityResources = parsedResult?.evidence?.sourceNotes?.observabilityResources ?? [];
  const approvalEvidence = parsedResult?.evidence?.approvalEvidence;
  const canApprove =
    Boolean(incidentId && parsedResult?.proposedAction?.actionId) &&
    parsedResult?.proposedAction?.policyMode === "approval_required" &&
    parsedResult?.proposedAction?.status === "proposed";
  const isScenarioHealthy = scenarioState === "healthy";
  const isGalileoReady = agentMonitoring?.status === "ready";
  const agentMonitoringLabel = agentMonitoring
    ? isGalileoReady
      ? "galileo ready"
      : agentMonitoring.apiKeyConfigured
        ? "not initialized"
        : "key missing"
    : "unknown";
  const lifecycle = useMemo(
    () => [
      {
        label: "Incident intake",
        detail: "Detector webhook or demo incident received",
        done: Boolean(incidentId || parsedResult?.incident?.incidentId),
        icon: Radar
      },
      {
        label: "Evidence package",
        detail: "Splunk MCP evidence attached",
        done: Boolean(parsedResult?.evidence || parsedResult?.enrichment),
        icon: FileText
      },
      {
        label: "Policy check",
        detail: "Guardrails determine approval mode",
        done: Boolean(parsedResult?.policy || parsedResult?.proposedAction?.policyMode),
        icon: ShieldCheck
      },
      {
        label: "Human approval",
        detail: "Presenter approves eligible bounded action",
        done: Boolean(parsedResult?.approved || parsedResult?.incident?.approvedAt),
        icon: KeyRound
      },
      {
        label: "Execution",
        detail: "Remediation agent applies the action",
        done: Boolean(parsedResult?.executeResult?.status || parsedResult?.incident?.executedAt),
        icon: Play
      },
      {
        label: "Verification",
        detail: "Filesystem pressure and latency recovery validated",
        done: Boolean(parsedResult?.verifyResult?.status || parsedResult?.incident?.verifiedAt),
        icon: BadgeCheck
      }
    ],
    [incidentId, parsedResult]
  );

  return (
    <main className="console-shell">
      <header className="console-hero">
        <div className="hero-panel">
          <span className="eyebrow">
            <Sparkles size={16} aria-hidden="true" />
            Cisco Live incident command
          </span>
          <h1>AI Remediation Command Center</h1>
          <p>
            Presenter console for MCP evidence intake, policy-governed approval, execution, validation,
            and audit review.
          </p>
        </div>

        <aside className="status-panel">
          <div className="status-header">
            <span>Run state</span>
            <span className={`status-pill ${isScenarioHealthy ? "status-healthy" : "status-risk"}`}>
              {isScenarioHealthy ? <CheckCircle2 size={15} /> : <AlertTriangle size={15} />}
              {formatScenarioLabel(scenarioState)}
            </span>
          </div>
          <div className="command-message">
            <Clock3 size={18} aria-hidden="true" />
            <strong>{commandMessage}</strong>
          </div>
          <div className="status-grid">
            <span>Incident</span>
            <strong>{incidentId || parsedResult?.incident?.incidentId || "none"}</strong>
            <span>Last refresh</span>
            <strong>{lastUpdated}</strong>
          </div>
        </aside>
      </header>

      <section className="metric-grid" aria-label="Live incident summary">
        <MetricTile
          icon={Gauge}
          label="Status"
          value={
            parsedResult?.proposedAction?.status ??
            parsedResult?.incident?.status ??
            parsedResult?.verifyResult?.status ??
            "idle"
          }
          tone={parsedResult?.verifyResult?.status ? "healthy" : "neutral"}
        />
        <MetricTile
          icon={ShieldCheck}
          label="Policy"
          value={parsedResult?.policy?.policyMode ?? parsedResult?.proposedAction?.policyMode ?? "not evaluated"}
          tone={canApprove ? "risk" : "neutral"}
        />
        <MetricTile
          icon={HardDrive}
          label="Suspect signal"
          value={parsedResult?.evidence?.serviceImpact?.suspectService ?? parsedResult?.enrichment?.suspectService ?? "cache volume"}
          tone={parsedResult?.evidence?.serviceImpact?.suspectService ? "action" : "neutral"}
        />
        <MetricTile
          icon={Bot}
          label="Action"
          value={parsedResult?.proposedAction?.type ?? parsedResult?.actionId ?? "not proposed"}
          tone={parsedResult?.proposedAction?.type ? "action" : "neutral"}
        />
        <MetricTile
          icon={Activity}
          label="Agent monitor"
          value={agentMonitoringLabel}
          tone={isGalileoReady ? "healthy" : agentMonitoring?.apiKeyConfigured ? "risk" : "neutral"}
        />
      </section>

      <section className="lifecycle-panel" aria-label="Incident lifecycle">
        {lifecycle.map((step, index) => {
          const Icon = step.icon;
          const isCurrent = !step.done && lifecycle.slice(0, index).every((previous) => previous.done);
          return (
            <article className={`lifecycle-step ${step.done ? "step-done" : ""} ${isCurrent ? "step-current" : ""}`} key={step.label}>
              <div className="step-index">
                <Icon size={18} aria-hidden="true" />
              </div>
              <div>
                <h2>{step.label}</h2>
                <p>{step.detail}</p>
              </div>
            </article>
          );
        })}
      </section>

      <section className="command-grid">
        <article className="panel evidence-panel">
          <div className="panel-heading">
            <div>
              <span className="section-kicker">Splunk MCP handoff</span>
              <h2>Evidence Intake</h2>
            </div>
            <span className="mini-pill">MCP-backed</span>
          </div>
          <p className="panel-copy">
            Create an incident to query Splunk Observability Cloud through MCP. Operator notes are optional.
          </p>
          <textarea
            value={assistantSummary}
            onChange={(event) => setAssistantSummary(event.target.value)}
            placeholder="Optional operator notes. Leave blank to use Splunk MCP evidence only."
            rows={9}
            className="textarea"
          />
          <div className="button-row">
            <CommandButton icon={Radar} onClick={createIncident} disabled={busyAction !== null} variant="primary">
              Gather MCP Evidence
            </CommandButton>
            <CommandButton icon={RotateCcw} onClick={resetRemediationFlow} disabled={busyAction !== null}>
              Reset Flow
            </CommandButton>
            <CommandButton
              icon={RefreshCw}
              onClick={() => runCommand("refresh", "Refreshing latest incident", refreshIncidents)}
              disabled={busyAction !== null}
            >
              Refresh
            </CommandButton>
            <CommandButton icon={FileText} onClick={explainEvidence} disabled={!incidentId || busyAction !== null}>
              Explain
            </CommandButton>
            <CommandButton icon={Bot} onClick={proposeAction} disabled={!incidentId || busyAction !== null}>
              Propose
            </CommandButton>
            <CommandButton icon={ClipboardCheck} onClick={approveAction} disabled={!canApprove || busyAction !== null} variant="approve">
              Approve
            </CommandButton>
          </div>
        </article>

        <aside className="panel control-panel">
          <div className="panel-heading">
            <div>
              <span className="section-kicker">Demo control</span>
              <h2>Scenario Controls</h2>
            </div>
          </div>
          <p>Fill the claims-knowledge cache volume before incident intake, then clean it during remediation.</p>
          <div className="control-actions">
            <CommandButton
              icon={Zap}
              onClick={() => activateScenario("cache-disk-pressure")}
              disabled={busyAction !== null}
              variant="danger"
            >
              Trigger Cache Pressure
            </CommandButton>
            <CommandButton icon={RotateCcw} onClick={resetScenario} disabled={busyAction !== null}>
              Reset Scenario
            </CommandButton>
            <CommandButton
              icon={RefreshCw}
              onClick={() => runCommand("refresh", "Refreshing scenario state", refreshScenario)}
              disabled={busyAction !== null}
            >
              Refresh Status
            </CommandButton>
          </div>
          <div className="monitoring-summary">
            <div className="panel-heading">
              <div>
                <span className="section-kicker">Galileo</span>
                <h2>Agent Monitoring</h2>
              </div>
              <span className={`mini-pill ${isGalileoReady ? "mini-pill-ready" : "mini-pill-risk"}`}>
                {agentMonitoringLabel}
              </span>
            </div>
            <dl className="definition-grid compact">
              <div>
                <dt>Key source</dt>
                <dd>{agentMonitoring?.apiKeySource ?? "unknown"}</dd>
              </div>
              <div>
                <dt>Project</dt>
                <dd>{agentMonitoring?.project ?? "ciscolive26"}</dd>
              </div>
              <div>
                <dt>Log stream</dt>
                <dd>{agentMonitoring?.logStream ?? "remediation-agent"}</dd>
              </div>
              <div>
                <dt>Agent</dt>
                <dd>{agentMonitoring?.agent.agentMonitoring ?? agentMonitoring?.agent.status ?? "unknown"}</dd>
              </div>
              <div>
                <dt>Session</dt>
                <dd>{parsedResult?.sessionId ?? "not generated"}</dd>
              </div>
            </dl>
            <div className="showcase-card">
              <div>
                <strong>Showcase Story</strong>
                <span>{parsedResult?.postmortem?.auditOutcome ?? "ready"}</span>
              </div>
              <p>
                {parsedResult?.postmortem?.summary ??
                  "Generate a session with evidence retrieval, agent reasoning, guardrails, approval, action, and verification."}
              </p>
            </div>
            <div className="instrumentation-list showcase-list">
              <strong>Showcase traces</strong>
              <ul>
                {(agentMonitoring?.showcaseInstrumentation ?? []).map((span) => (
                  <li key={span.spanName}>
                    <span>{span.stage}</span>
                    <b>{span.spanName}</b>
                    <em>{span.spanType}</em>
                  </li>
                ))}
              </ul>
            </div>
            <div className="control-actions">
              <CommandButton icon={Sparkles} onClick={runGalileoShowcase} disabled={!isGalileoReady || busyAction !== null} variant="primary">
                Run Showcase
              </CommandButton>
              <CommandButton
                icon={Activity}
                onClick={() => runCommand("monitoring", "Refreshing Galileo monitoring", refreshAgentMonitoring)}
                disabled={busyAction !== null}
              >
                Refresh Galileo
              </CommandButton>
            </div>
          </div>
        </aside>
      </section>

      <section className="detail-grid">
        {approvalEvidence ? (
          <article className="panel approval-evidence-panel">
            <div className="panel-heading">
              <div>
                <span className="section-kicker">Pre-approval evidence</span>
                <h2>Problem Impact Chain</h2>
              </div>
              <span className="mini-pill">metrics-backed</span>
            </div>
            <div className="evidence-proof-grid">
              <EvidenceMetricGroup title="Customer endpoint" icon={Activity} metrics={approvalEvidence.customerImpact} />
              <EvidenceMetricGroup title="APM service" icon={Gauge} metrics={approvalEvidence.backendImpact} />
              <EvidenceMetricGroup title="Infrastructure" icon={HardDrive} metrics={approvalEvidence.infrastructureImpact} />
            </div>
            {approvalEvidence.impactChain && approvalEvidence.impactChain.length > 0 ? (
              <div className="impact-chain-list">
                <strong>
                  <Zap size={17} aria-hidden="true" />
                  Impact chain
                </strong>
                <ol>
                  {approvalEvidence.impactChain.map((step) => (
                    <li key={`${step.stage}-${step.label}`}>
                      <span className={`evidence-status status-${statusClass(step.status)}`}>
                        {chainStatusLabel(step.status)}
                      </span>
                      <div>
                        <b>{step.label}</b>
                        <p>{step.detail}</p>
                      </div>
                    </li>
                  ))}
                </ol>
              </div>
            ) : null}
          </article>
        ) : null}

        <article className="panel summary-panel">
          <div className="panel-heading">
            <div>
              <span className="section-kicker">Live summary</span>
              <h2>Incident Context</h2>
            </div>
          </div>
          <dl className="definition-grid">
            <div>
              <dt>Incident ID</dt>
              <dd>{parsedResult?.incident?.incidentId ?? incidentId ?? "none"}</dd>
            </div>
            <div>
              <dt>Detector</dt>
              <dd>{parsedResult?.incident?.detectorName ?? "n/a"}</dd>
            </div>
            <div>
              <dt>Affected transaction</dt>
              <dd>
                {parsedResult?.evidence?.browserExperience?.affectedJourney ??
                  parsedResult?.incident?.businessTransaction ??
                  "not set"}
              </dd>
            </div>
            <div>
              <dt>Sessions impacted</dt>
              <dd>{valueOrFallback(parsedResult?.evidence?.browserExperience?.affectedSessions)}</dd>
            </div>
            <div>
              <dt>Suspect service</dt>
              <dd>
                {parsedResult?.evidence?.serviceImpact?.suspectService ??
                  parsedResult?.enrichment?.suspectService ??
                  "n/a"}
              </dd>
            </div>
            <div>
              <dt>Approval</dt>
              <dd>{parsedResult?.approved || parsedResult?.incident?.approvedAt ? "approved" : "pending"}</dd>
            </div>
          </dl>
        </article>

        <article className="panel">
          <div className="panel-heading">
            <div>
              <span className="section-kicker">Enrichment</span>
              <h2>Evidence Sources</h2>
            </div>
            <span className="mini-pill">
              {parsedResult?.evidence?.sourceNotes?.enrichmentApplied ?? parsedResult?.enrichment?.apiBacked
                ? "MCP/API-backed"
                : "fallback"}
            </span>
          </div>
          <dl className="definition-grid compact">
            <div>
              <dt>Sources</dt>
              <dd>{enrichmentSources.length > 0 ? enrichmentSources.join(", ") : "none"}</dd>
            </div>
            <div>
              <dt>Resources</dt>
              <dd>{observabilityResources.length > 0 ? String(observabilityResources.length) : "none"}</dd>
            </div>
            <div>
              <dt>Recent change</dt>
              <dd>{parsedResult?.evidence?.investigation?.recentChange ?? "not available"}</dd>
            </div>
            <div>
              <dt>Session replay</dt>
              <dd>{parsedResult?.evidence?.browserExperience?.sessionReplayUrl ? "linked" : "not available"}</dd>
            </div>
          </dl>
          {enrichmentWarnings.length > 0 ? (
            <div className="warning-list">
              <strong>Warnings</strong>
              <ul>
                {enrichmentWarnings.map((warning) => (
                  <li key={warning}>{warning}</li>
                ))}
              </ul>
            </div>
          ) : null}
          {observabilityResources.length > 0 ? (
            <div className="resource-list">
              <strong>Resources</strong>
              <ul>
                {observabilityResources.slice(0, 8).map((resource) => (
                  <li key={`${resource.type}-${resource.name}`}>
                    <span>{resource.type}</span>
                    <b>{resource.name}</b>
                    {resource.detail ? <em>{resource.detail}</em> : null}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </article>

        <article className="panel">
          <div className="panel-heading">
            <div>
              <span className="section-kicker">Action context</span>
              <h2>Approval And Validation</h2>
            </div>
          </div>
          <dl className="definition-grid compact">
            <div>
              <dt>Confidence</dt>
              <dd>
                {parsedResult?.proposedAction?.confidenceBand ??
                  parsedResult?.evidence?.investigation?.confidenceBand ??
                  "unknown"}
              </dd>
            </div>
            <div>
              <dt>Reason</dt>
              <dd>{parsedResult?.policy?.reason ?? parsedResult?.proposedAction?.reasoningSummary ?? "n/a"}</dd>
            </div>
            <div>
              <dt>Execution</dt>
              <dd>{parsedResult?.executeResult?.status ?? "not executed"}</dd>
            </div>
            <div>
              <dt>Verification</dt>
              <dd>{parsedResult?.verifyResult?.status ?? "not verified"}</dd>
            </div>
            <div>
              <dt>Measured latency</dt>
              <dd>
                {parsedResult?.verifyResult?.measuredLatencyMs !== undefined
                  ? `${parsedResult.verifyResult.measuredLatencyMs} ms`
                  : "n/a"}
              </dd>
            </div>
            <div>
              <dt>Latency threshold</dt>
              <dd>
                {parsedResult?.verifyResult?.latencyThresholdMs !== undefined
                  ? `${parsedResult.verifyResult.latencyThresholdMs} ms`
                  : "n/a"}
              </dd>
            </div>
          </dl>
          <div className="validation-list">
            <strong>
              <ListChecks size={17} aria-hidden="true" />
              Validation plan
            </strong>
            <ul>
              {(parsedResult?.proposedAction?.validationPlan ?? ["Waiting for proposed action."]).map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ul>
          </div>
        </article>
      </section>

      <section className="raw-panel">
        <div className="panel-heading">
          <div>
            <span className="section-kicker">Debug view</span>
            <h2>
              <TerminalSquare size={22} aria-hidden="true" />
              Raw Response
            </h2>
          </div>
          <span className="mini-pill">json</span>
        </div>
        <pre>{result}</pre>
      </section>
    </main>
  );
}
