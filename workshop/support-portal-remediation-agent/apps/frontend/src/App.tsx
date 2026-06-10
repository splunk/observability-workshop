import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  BookOpenText,
  CheckCircle2,
  Clock3,
  FileSearch,
  Gauge,
  MessageSquareText,
  RefreshCw,
  RotateCcw,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  Zap
} from "lucide-react";
import { currentBrowserAppConfig } from "@ibobs/runtime-config/browser";
import { setJourneyContext, trackBusinessTransaction } from "./rum";
import "./App.css";

const transactionDefinitions = [
  {
    id: "claim_status_response",
    name: "AI Claim Status",
    detail: "AI-generated claim status response backed by the claims knowledge service.",
    icon: MessageSquareText
  },
  {
    id: "policy_coverage_lookup",
    name: "Policy Coverage Lookup",
    detail: "Independent transaction kept healthy during the primary incident.",
    icon: FileSearch
  },
  {
    id: "claims_faq_search",
    name: "Claims FAQ Search",
    detail: "FAQ search remains available while the claim status path absorbs the cache pressure incident.",
    icon: BookOpenText
  }
];

type ActionKey =
  | "support"
  | "case"
  | "article"
  | "pressure"
  | "reset"
  | "refresh"
  | null;

type RequestState = {
  label: string;
  tone: "idle" | "running" | "success" | "error";
};

function formatScenarioLabel(value: string) {
  return value
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function formatActionError(error: unknown, action: Exclude<ActionKey, null>) {
  const message = error instanceof Error ? error.message : String(error);
  if (message === "Failed to fetch") {
    return action === "support" || action === "case" || action === "article"
      ? "API gateway unavailable for this transaction."
      : "Scenario controller unavailable.";
  }

  return message;
}

function IconButton({
  children,
  icon: Icon,
  onClick,
  disabled,
  variant = "secondary"
}: {
  children: string;
  icon: typeof Send;
  onClick: () => void;
  disabled?: boolean;
  variant?: "primary" | "secondary" | "danger";
}) {
  return (
    <button className={`button button-${variant}`} onClick={onClick} disabled={disabled}>
      <Icon size={17} aria-hidden="true" />
      <span>{children}</span>
    </button>
  );
}

export function App() {
  const { apiBaseUrl, scenarioControllerBaseUrl } = currentBrowserAppConfig();
  const [supportPrompt, setSupportPrompt] = useState(
    "My auto claim status has not updated and I need to know what is delaying payment."
  );
  const [caseId, setCaseId] = useState("POL-4821");
  const [articleQuery, setArticleQuery] = useState("rental reimbursement deductible");
  const [result, setResult] = useState("Choose a transaction to see live API output.");
  const [activeScenario, setActiveScenario] = useState("healthy");
  const [scenarioMessage, setScenarioMessage] = useState("No scenario active.");
  const [busyAction, setBusyAction] = useState<ActionKey>(null);
  const [requestState, setRequestState] = useState<RequestState>({
    label: "Ready for customer traffic.",
    tone: "idle"
  });

  const isIncidentActive = activeScenario !== "healthy";
  const transactionHealth = useMemo(
    () =>
      transactionDefinitions.map((transaction) => {
        const isPrimary = transaction.id === "claim_status_response";
        const status = isPrimary && isIncidentActive ? "At risk" : "Healthy";
        return {
          ...transaction,
          status,
          tone: status === "At risk" ? "risk" : "healthy"
        };
      }),
    [isIncidentActive]
  );

  useEffect(() => {
    setJourneyContext({
      "app.active_scenario": activeScenario
    });
  }, [activeScenario]);

  useEffect(() => {
    void refreshScenario();
  }, []);

  async function runAction(action: Exclude<ActionKey, null>, label: string, fn: () => Promise<void>) {
    setBusyAction(action);
    setRequestState({ label, tone: "running" });

    try {
      await fn();
      setRequestState({ label: `${label} complete.`, tone: "success" });
    } catch (error) {
      const message = formatActionError(error, action);
      setRequestState({ label: message, tone: "error" });
      if (action === "support" || action === "case" || action === "article") {
        setResult(JSON.stringify({ error: message }, null, 2));
      }
    } finally {
      setBusyAction(null);
    }
  }

  async function callSupportResponse() {
    await runAction("support", "Submitting AI claim status transaction", async () => {
      const payload = await trackBusinessTransaction(
        "claim_status_response",
        "claim_status_submit",
        {
          "app.business_transaction": "claim_status_response",
          "app.transaction_name": "AI Claim Status",
          "app.active_scenario": activeScenario,
          "app.ui_surface": "claims_portal"
        },
        async () => {
          const response = await fetch(`${apiBaseUrl}/api/support/respond`, {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({ prompt: supportPrompt })
          });

          if (!response.ok) {
            throw new Error(`Claim status request failed with status ${response.status}`);
          }

          return response.json();
        }
      );

      setResult(JSON.stringify(payload, null, 2));
    });
  }

  async function callCaseLookup() {
    await runAction("case", "Checking policy coverage transaction", async () => {
      const payload = await trackBusinessTransaction(
        "policy_coverage_lookup",
        "policy_coverage_lookup",
        {
          "app.business_transaction": "policy_coverage_lookup",
          "app.transaction_name": "Policy Coverage Lookup",
          "app.active_scenario": activeScenario,
          "app.ui_surface": "claims_portal"
        },
        async () => {
          const response = await fetch(`${apiBaseUrl}/api/cases/${encodeURIComponent(caseId)}`);
          if (!response.ok) {
            throw new Error(`Policy coverage lookup failed with status ${response.status}`);
          }
          return response.json();
        }
      );

      setResult(JSON.stringify(payload, null, 2));
    });
  }

  async function callArticleSearch() {
    await runAction("article", "Searching claims FAQ transaction", async () => {
      const payload = await trackBusinessTransaction(
        "claims_faq_search",
        "claims_faq_search",
        {
          "app.business_transaction": "claims_faq_search",
          "app.transaction_name": "Claims FAQ Search",
          "app.active_scenario": activeScenario,
          "app.ui_surface": "claims_portal"
        },
        async () => {
          const response = await fetch(`${apiBaseUrl}/api/articles/search?q=${encodeURIComponent(articleQuery)}`);
          if (!response.ok) {
            throw new Error(`Claims FAQ search failed with status ${response.status}`);
          }
          return response.json();
        }
      );

      setResult(JSON.stringify(payload, null, 2));
    });
  }

  async function refreshScenario() {
    await runAction("refresh", "Refreshing scenario state", async () => {
      const response = await fetch(`${scenarioControllerBaseUrl}/scenario/state`);
      const payload = (await response.json()) as { activeScenario: string };
      setActiveScenario(payload.activeScenario);
      setScenarioMessage(
        payload.activeScenario === "healthy"
          ? "No scenario active."
          : `Scenario active: ${formatScenarioLabel(payload.activeScenario)}`
      );
    });
  }

  async function activateScenario(scenarioId: string) {
    await runAction("pressure", "Activating cache pressure scenario", async () => {
      const response = await fetch(`${scenarioControllerBaseUrl}/scenario/activate/${scenarioId}`, {
        method: "POST"
      });
      const payload = (await response.json()) as { activeScenario: string };
      setActiveScenario(payload.activeScenario);
      setScenarioMessage(`Scenario active: ${formatScenarioLabel(payload.activeScenario)}`);
    });
  }

  async function resetScenario() {
    await runAction("reset", "Resetting scenario", async () => {
      const response = await fetch(`${scenarioControllerBaseUrl}/scenario/reset`, {
        method: "POST"
      });
      const payload = (await response.json()) as { activeScenario: string };
      setActiveScenario(payload.activeScenario);
      setScenarioMessage("Scenario reset to healthy.");
    });
  }

  return (
    <main className="portal-shell">
      <header className="portal-hero">
        <div className="hero-copy">
          <span className="eyebrow">
            <Sparkles size={16} aria-hidden="true" />
            Cisco Live demo environment
          </span>
          <h1>AI Claims Portal</h1>
          <p>
            Customer-facing insurance workflow for demonstrating claim status impact, transaction isolation, and
            observable recovery during a live incident.
          </p>
        </div>

        <div className="command-card">
          <div className="command-card-header">
            <span>Scenario State</span>
            <span className={`status-pill ${isIncidentActive ? "status-risk" : "status-healthy"}`}>
              {isIncidentActive ? <AlertTriangle size={15} /> : <CheckCircle2 size={15} />}
              {formatScenarioLabel(activeScenario)}
            </span>
          </div>
          <p>{scenarioMessage}</p>
          <div className="command-actions">
            <IconButton
              icon={Zap}
              onClick={() => activateScenario("cache-disk-pressure")}
              disabled={busyAction !== null}
              variant="danger"
            >
              Trigger Cache Pressure
            </IconButton>
            <IconButton icon={RotateCcw} onClick={resetScenario} disabled={busyAction !== null}>
              Reset
            </IconButton>
            <IconButton icon={RefreshCw} onClick={refreshScenario} disabled={busyAction !== null}>
              Refresh
            </IconButton>
          </div>
        </div>
      </header>

      <section className="signal-bar" aria-label="Demo status">
        <div className="signal-item">
          <Gauge size={20} aria-hidden="true" />
          <div>
            <span>Transaction posture</span>
            <strong>{isIncidentActive ? "1 at risk, 2 contained" : "All journeys healthy"}</strong>
          </div>
        </div>
        <div className="signal-item">
          <Activity size={20} aria-hidden="true" />
          <div>
            <span>Telemetry surface</span>
            <strong>RUM, APM, host filesystem</strong>
          </div>
        </div>
        <div className="signal-item">
          <ShieldCheck size={20} aria-hidden="true" />
          <div>
            <span>Demo control</span>
            <strong>Deterministic scenario reset</strong>
          </div>
        </div>
        <div className={`request-state request-${requestState.tone}`}>
          <Clock3 size={19} aria-hidden="true" />
          <strong>{requestState.label}</strong>
        </div>
      </section>

      <section className="workspace-grid">
        <article className="workspace-primary">
          <div className="section-heading">
            <div>
              <span className="section-kicker">Primary customer journey</span>
              <h2>AI Claim Status</h2>
            </div>
            <span className={`status-pill ${isIncidentActive ? "status-risk" : "status-healthy"}`}>
              {isIncidentActive ? "At risk" : "Healthy"}
            </span>
          </div>
          <p className="panel-copy">
            Ask the AI assistant about a claim. When the cache pressure scenario is active, this transaction
            demonstrates the degraded journey while adjacent workflows continue to respond.
          </p>
          <label className="field-label" htmlFor="support-prompt">
            Claim question
          </label>
          <textarea
            id="support-prompt"
            value={supportPrompt}
            onChange={(event) => setSupportPrompt(event.target.value)}
            rows={7}
            className="textarea"
          />
          <div className="panel-footer">
            <IconButton
              icon={Send}
              onClick={callSupportResponse}
              disabled={busyAction !== null}
              variant="primary"
            >
              Submit Claim Status
            </IconButton>
            <span>Trace attribute: claim_status_response</span>
          </div>
        </article>

        <aside className="side-stack">
          <article className="compact-panel">
            <div className="compact-title">
              <FileSearch size={20} aria-hidden="true" />
              <h3>Policy Coverage Lookup</h3>
            </div>
            <p>Validate a separate customer journey while the claim status response is degraded.</p>
            <label className="field-label" htmlFor="case-id">
              Policy ID
            </label>
            <input
              id="case-id"
              className="input"
              value={caseId}
              onChange={(event) => setCaseId(event.target.value)}
            />
            <IconButton icon={ArrowRight} onClick={callCaseLookup} disabled={busyAction !== null}>
              Check Coverage
            </IconButton>
          </article>

          <article className="compact-panel">
            <div className="compact-title">
              <BookOpenText size={20} aria-hidden="true" />
              <h3>Claims FAQ Search</h3>
            </div>
            <p>Confirm FAQ search is still callable while the primary claim status workflow slows down.</p>
            <label className="field-label" htmlFor="article-query">
              Search query
            </label>
            <input
              id="article-query"
              className="input"
              value={articleQuery}
              onChange={(event) => setArticleQuery(event.target.value)}
            />
            <IconButton icon={Search} onClick={callArticleSearch} disabled={busyAction !== null}>
              Search FAQ
            </IconButton>
          </article>
        </aside>
      </section>

      <section className="transaction-strip" aria-label="Business transactions">
        {transactionHealth.map((transaction) => {
          const Icon = transaction.icon;
          return (
            <article className={`transaction-card transaction-${transaction.tone}`} key={transaction.name}>
              <div className="transaction-icon">
                <Icon size={20} aria-hidden="true" />
              </div>
              <div>
                <div className="transaction-topline">
                  <h3>{transaction.name}</h3>
                  <span>{transaction.status}</span>
                </div>
                <p>{transaction.detail}</p>
              </div>
            </article>
          );
        })}
      </section>

      <section className="result-panel">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Inspectable response</span>
            <h2>Live API Result</h2>
          </div>
          <span className="mono-label">json</span>
        </div>
        <pre>{result}</pre>
      </section>
    </main>
  );
}
