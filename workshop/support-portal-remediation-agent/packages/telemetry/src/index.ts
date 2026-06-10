import { BUSINESS_TRANSACTIONS } from "@ibobs/shared-types";
import { appVersion, deploymentEnvironment, serviceNamespace } from "./config";

export const businessTransactionLabels = {
  [BUSINESS_TRANSACTIONS.customerSupportResponse]: "AI Claim Status",
  [BUSINESS_TRANSACTIONS.caseStatusLookup]: "Policy Coverage Lookup",
  [BUSINESS_TRANSACTIONS.knowledgeArticleSearch]: "Claims FAQ Search",
  [BUSINESS_TRANSACTIONS.legacyCustomerSupportResponse]: "AI Claim Status",
  [BUSINESS_TRANSACTIONS.legacyCaseStatusLookup]: "Policy Coverage Lookup",
  [BUSINESS_TRANSACTIONS.legacyKnowledgeArticleSearch]: "Claims FAQ Search"
};

export function buildTelemetryAttributes(transaction: keyof typeof businessTransactionLabels | string) {
  return {
    "service.namespace": serviceNamespace,
    "deployment.environment": deploymentEnvironment,
    "service.version": appVersion,
    "app.version": appVersion,
    "app.business_transaction": transaction
  };
}

export * from "./node";
export * from "./splunk-node";
export * from "./logger";
export * from "./config";
