import { POLICY_MODES, type EvidenceBundle, type PolicyDecision } from "@ibobs/shared-types";

export function evaluatePolicy(evidence: EvidenceBundle): PolicyDecision {
  if (evidence.investigation.confidenceBand === "low") {
    return {
      eligible: false,
      policyMode: POLICY_MODES.recommendOnly,
      reason: "Confidence is too low for automated remediation."
    };
  }

  return {
    eligible: true,
    policyMode: POLICY_MODES.approvalRequired,
    reason: "Confidence is sufficient, but customer-facing remediation requires approval."
  };
}
