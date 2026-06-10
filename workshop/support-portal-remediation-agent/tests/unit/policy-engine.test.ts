import test from "node:test";
import assert from "node:assert/strict";
import { evaluatePolicy } from "../../packages/policy-engine/src/index.ts";
import {
  BUSINESS_TRANSACTIONS,
  POLICY_MODES,
  type EvidenceBundle
} from "../../packages/shared-types/src/index.ts";

function buildEvidence(overrides?: Partial<EvidenceBundle>): EvidenceBundle {
  return {
    incidentId: "incident-123",
    scenarioId: "cache-disk-pressure",
    detector: {
      detectorId: "det-1",
      detectorName: "Claims Knowledge Cache Volume Pressure",
      severity: "critical",
      triggeredAt: "2026-04-08T12:00:00Z",
      dimensions: { service: "claims-knowledge", environment: "demo" }
    },
    browserExperience: {
      affectedSessions: 24,
      frustrationSignals: ["rage_click"],
      affectedJourney: BUSINESS_TRANSACTIONS.customerSupportResponse
    },
    serviceImpact: {
      affectedServices: ["claims-knowledge"],
      suspectService: "claims-knowledge",
      affectedTransactions: [BUSINESS_TRANSACTIONS.customerSupportResponse]
    },
    investigation: {
      likelyCause: "cache filesystem pressure",
      confidenceBand: "high"
    },
    candidateActions: [],
    sourceNotes: {
      enrichmentApplied: false
    },
    ...overrides
  };
}

test("evaluatePolicy blocks automation when confidence is low", () => {
  const decision = evaluatePolicy(
    buildEvidence({
      investigation: {
        likelyCause: "uncertain evidence",
        confidenceBand: "low"
      }
    })
  );

  assert.deepEqual(decision, {
    eligible: false,
    policyMode: POLICY_MODES.recommendOnly,
    reason: "Confidence is too low for automated remediation."
  });
});

test("evaluatePolicy requires approval when confidence is sufficient", () => {
  const decision = evaluatePolicy(buildEvidence());

  assert.deepEqual(decision, {
    eligible: true,
    policyMode: POLICY_MODES.approvalRequired,
    reason: "Confidence is sufficient, but customer-facing remediation requires approval."
  });
});
