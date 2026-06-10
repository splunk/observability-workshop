import test from "node:test";
import assert from "node:assert/strict";
import {
  getIncident,
  listWebhookReceipts,
  resetIncidents,
  saveIncident,
  saveWebhookReceipt
} from "../../packages/shared-types/src/store.ts";
import { BUSINESS_TRANSACTIONS } from "../../packages/shared-types/src/index.ts";

test("incident store saves and retrieves incidents", () => {
  resetIncidents();

  saveIncident({
    incidentId: "incident-1",
    scenarioId: "cache-disk-pressure",
    businessTransaction: BUSINESS_TRANSACTIONS.customerSupportResponse,
    status: "open"
  });

  assert.equal(getIncident("incident-1")?.status, "open");
});

test("webhook receipt store keeps newest receipts first and caps history at 50", () => {
  for (let index = 0; index < 55; index += 1) {
    saveWebhookReceipt({
      receiptId: `receipt-${index}`,
      receivedAt: `2026-04-08T12:${String(index).padStart(2, "0")}:00Z`,
      detectorId: `det-${index}`,
      detectorName: `Detector ${index}`,
      severity: "critical",
      triggeredAt: "2026-04-08T12:00:00Z"
    });
  }

  const receipts = listWebhookReceipts();
  assert.equal(receipts.length, 50);
  assert.equal(receipts[0]?.receiptId, "receipt-54");
  assert.equal(receipts.at(-1)?.receiptId, "receipt-5");
});
