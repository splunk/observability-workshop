import type {
  ActionExecutionResult,
  ActionVerificationResult,
  EvidenceBundle,
  IncidentRecord,
  ProposedAction,
  WebhookReceipt
} from "./index";

export type StoredIncident = IncidentRecord & {
  evidence?: EvidenceBundle;
  proposedAction?: ProposedAction;
  executeResult?: ActionExecutionResult;
  verifyResult?: ActionVerificationResult;
  approvedAt?: string;
  executedAt?: string;
  verifiedAt?: string;
};

const incidents = new Map<string, StoredIncident>();
const webhookReceipts: WebhookReceipt[] = [];

export function saveIncident(record: StoredIncident) {
  incidents.set(record.incidentId, record);
  return record;
}

export function getIncident(incidentId: string) {
  return incidents.get(incidentId);
}

export function listIncidents() {
  return Array.from(incidents.values());
}

export function resetIncidents() {
  const count = incidents.size;
  incidents.clear();
  return count;
}

export function saveWebhookReceipt(receipt: WebhookReceipt) {
  webhookReceipts.unshift(receipt);
  if (webhookReceipts.length > 50) {
    webhookReceipts.length = 50;
  }
  return receipt;
}

export function listWebhookReceipts() {
  return [...webhookReceipts];
}

export function resetWebhookReceipts() {
  const count = webhookReceipts.length;
  webhookReceipts.length = 0;
  return count;
}
