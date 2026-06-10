import test from "node:test";
import assert from "node:assert/strict";
import { RemediationAgentClient } from "../../apps/remediation-orchestrator/src/agent-client.ts";
import {
  ACTION_TYPES,
  BUSINESS_TRANSACTIONS,
  POLICY_MODES,
  type EvidenceBundle
} from "../../packages/shared-types/src/index.ts";

function buildEvidence(): EvidenceBundle {
  return {
    incidentId: "incident-agent-client",
    scenarioId: "cache-disk-pressure",
    detector: {
      detectorId: "detector-cache",
      detectorName: "Claims Knowledge Cache Volume Pressure",
      severity: "critical",
      triggeredAt: "2026-06-03T12:00:00Z",
      dimensions: {
        service: "claims-knowledge",
        environment: "demo"
      }
    },
    browserExperience: {
      affectedSessions: 4,
      frustrationSignals: ["rage_click"],
      affectedJourney: BUSINESS_TRANSACTIONS.customerSupportResponse
    },
    serviceImpact: {
      affectedServices: ["claims-knowledge"],
      suspectService: "claims-knowledge",
      p95LatencyMs: 2400,
      affectedTransactions: [BUSINESS_TRANSACTIONS.customerSupportResponse]
    },
    investigation: {
      likelyCause: "claims-knowledge cache filesystem pressure",
      confidenceBand: "high"
    },
    candidateActions: [ACTION_TYPES.cleanServiceCache],
    sourceNotes: {
      enrichmentApplied: true,
      apiEnrichmentSources: ["mcp:get_apm_service_latency", "mcp:execute_signalflow_program"]
    }
  };
}

test("RemediationAgentClient reports agent health failures as unavailable", async () => {
  const originalFetch = globalThis.fetch;
  globalThis.fetch = (async () => new Response("nope", { status: 503 })) as typeof fetch;

  try {
    const client = new RemediationAgentClient("http://agent.local");
    assert.deepEqual(await client.health(), {
      status: "unavailable",
      error: "remediation agent returned 503"
    });
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("RemediationAgentClient maps agent evaluation into a bounded proposed action", async () => {
  const originalFetch = globalThis.fetch;
  let requestBody: unknown;

  globalThis.fetch = (async (url, init) => {
    assert.equal(String(url), "http://agent.local/agent/evaluate");
    requestBody = JSON.parse(String(init?.body));
    return new Response(
      JSON.stringify({
        incidentId: "incident-agent-client",
        recommendedAction: "clean_claims_knowledge_cache",
        model: "gpt-4.1-mini",
        confidenceBand: "high",
        reasoningSummary: "Clean the bounded claims knowledge cache.",
        needsApproval: true
      })
    );
  }) as typeof fetch;

  try {
    const client = new RemediationAgentClient("http://agent.local");
    const action = await client.evaluate(buildEvidence(), POLICY_MODES.approvalRequired);

    assert.deepEqual(requestBody, {
      incidentId: "incident-agent-client",
      candidateActions: ["clean_claims_knowledge_cache"],
      likelyCause: "claims-knowledge cache filesystem pressure",
      confidenceBand: "high"
    });
    assert.equal(action.incidentId, "incident-agent-client");
    assert.equal(action.type, ACTION_TYPES.cleanServiceCache);
    assert.equal(action.target, "claims-knowledge-cache");
    assert.equal(action.policyMode, POLICY_MODES.approvalRequired);
    assert.equal(action.status, "proposed");
    assert.ok(action.validationPlan.some((step) => /claims-knowledge latency/.test(step)));
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("RemediationAgentClient posts Galileo showcase options to the agent", async () => {
  const originalFetch = globalThis.fetch;
  let requestBody: unknown;

  globalThis.fetch = (async (url, init) => {
    assert.equal(String(url), "http://agent.local/agent/galileo/showcase");
    requestBody = JSON.parse(String(init?.body));
    return new Response(
      JSON.stringify({
        incidentId: "incident-showcase",
        project: "ciscolive26",
        logStream: "remediation-agent",
        model: "gpt-4.1-mini",
        story: ["Splunk MCP evidence handoff"],
        showcaseTraces: [
          { name: "showcase.incident_intake", type: "workflow" },
          { name: "showcase.guardrail_pre_action_check", type: "tool", includesProtectSpan: true }
        ],
        guardrail: { status: "blocked", unsafeRestartInstruction: true },
        plan: { recommendedAction: "clean_claims_knowledge_cache" },
        verification: { status: "validated" },
        demoGuide: ["Open Galileo project ciscolive26"]
      })
    );
  }) as typeof fetch;

  try {
    const client = new RemediationAgentClient("http://agent.local");
    const response = await client.runGalileoShowcase({
      incidentId: "incident-showcase",
      executeRemediation: false,
      includeUnsafeOperatorNote: true
    });

    assert.deepEqual(requestBody, {
      incidentId: "incident-showcase",
      executeRemediation: false,
      includeUnsafeOperatorNote: true
    });
    assert.equal(response.project, "ciscolive26");
    assert.equal(response.guardrail?.status, "blocked");
    assert.equal(response.plan?.recommendedAction, "clean_claims_knowledge_cache");
    assert.equal(response.verification?.status, "validated");
    assert.ok(response.showcaseTraces.some((trace) => trace.includesProtectSpan));
  } finally {
    globalThis.fetch = originalFetch;
  }
});
