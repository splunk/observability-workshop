import { ACTION_TYPES, BUSINESS_TRANSACTIONS, type AssistantEvidenceInput } from "@ibobs/shared-types";

export type ParsedAssistantEvidence = {
  likelyCause: string;
  confidenceBand: "low" | "medium" | "high";
  candidateActions: string[];
  inferredTransaction: string;
};

function matchFirst(text: string, patterns: RegExp[]) {
  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match?.[1]) {
      return match[1].trim();
    }
  }

  return undefined;
}

function normalizeTransaction(text: string) {
  const value = text.toLowerCase();
  if (
    value.includes(BUSINESS_TRANSACTIONS.caseStatusLookup) ||
    value.includes(BUSINESS_TRANSACTIONS.legacyCaseStatusLookup) ||
    value.includes("policy coverage") ||
    value.includes("case status")
  ) {
    return BUSINESS_TRANSACTIONS.caseStatusLookup;
  }
  if (
    value.includes(BUSINESS_TRANSACTIONS.knowledgeArticleSearch) ||
    value.includes(BUSINESS_TRANSACTIONS.legacyKnowledgeArticleSearch) ||
    value.includes("claims faq") ||
    value.includes("knowledge article search")
  ) {
    return BUSINESS_TRANSACTIONS.knowledgeArticleSearch;
  }
  if (
    value.includes(BUSINESS_TRANSACTIONS.customerSupportResponse) ||
    value.includes(BUSINESS_TRANSACTIONS.legacyCustomerSupportResponse) ||
    value.includes("ai claim status")
  ) {
    return BUSINESS_TRANSACTIONS.customerSupportResponse;
  }
  return BUSINESS_TRANSACTIONS.customerSupportResponse;
}

function inferTransaction(text: string) {
  const explicitTransaction = matchFirst(text, [
    /business transaction:\s*([^\n]+)/i,
    /affected transaction:\s*([^\n]+)/i
  ]);

  if (explicitTransaction) {
    return normalizeTransaction(explicitTransaction);
  }

  const normalized = text.toLowerCase();
  return normalized.includes("policy") || normalized.includes("case")
    ? BUSINESS_TRANSACTIONS.caseStatusLookup
    : normalized.includes("faq") || normalized.includes("search")
      ? BUSINESS_TRANSACTIONS.knowledgeArticleSearch
      : BUSINESS_TRANSACTIONS.customerSupportResponse;
}

function inferCandidateActions(text: string) {
  const normalized = text.toLowerCase();
  const actions = new Set<string>();

  if (
    normalized.includes("clean_claims_knowledge_cache") ||
    normalized.includes("clean_service_cache") ||
    normalized.includes("clean claims knowledge cache") ||
    normalized.includes("clean service cache") ||
    normalized.includes("clean the cache") ||
    normalized.includes("cache cleanup") ||
    normalized.includes("cache pressure") ||
    normalized.includes("disk pressure") ||
    normalized.includes("filesystem pressure") ||
    normalized.includes("disk utilization")
  ) {
    actions.add(ACTION_TYPES.cleanServiceCache);
  }

  if (normalized.includes("restart")) {
    actions.add(ACTION_TYPES.restartService);
  }

  if (actions.size === 0) {
    actions.add(ACTION_TYPES.cleanServiceCache);
  }

  const preferredOrder = [
    ACTION_TYPES.cleanServiceCache,
    ACTION_TYPES.restartService
  ];

  return preferredOrder.filter((action) => actions.has(action));
}

function inferConfidence(text: string) {
  const normalized = text.toLowerCase();
  const explicitConfidence = matchFirst(text, [
    /confidence:\s*(low|medium|high)\b/i,
    /\b(low|medium|high)\s+confidence\b/i
  ]);

  if (explicitConfidence) {
    return explicitConfidence.toLowerCase() as "low" | "medium" | "high";
  }

  if (
    normalized.includes("no disk.utilization") ||
    normalized.includes("no disk utilization") ||
    normalized.includes("no filesystem") ||
    normalized.includes("could not be confirmed") ||
    normalized.includes("unavailable") ||
    normalized.includes("empty result set") ||
    normalized.includes("query timeout") ||
    normalized.includes("insufficient signal")
  ) {
    return "low";
  }

  if (
    /(?:disk|filesystem) utilization[^.\n]*(?:above|elevated|high|pressure|threshold|9\d|8[5-9])/.test(normalized) ||
    normalized.includes("traceid:") ||
    normalized.includes("latency is elevated") ||
    normalized.includes("cache filesystem pressure") ||
    ((normalized.includes("claims-knowledge") || normalized.includes("support-knowledge")) &&
      (normalized.includes("clean_claims_knowledge_cache") || normalized.includes("clean_service_cache")))
  ) {
    return "high";
  }

  if (normalized.includes("low confidence")) {
    return "low";
  }

  return "medium";
}

function isNegativeEvidence(value: string) {
  return /\b(?:no|not|unavailable|insufficient|empty result set|could not be confirmed|cannot provide|timed? out|timeout)\b/i.test(value);
}

function buildLikelyCauseSummary(text: string) {
  const likelyCause = matchFirst(text, [
    /likely cause:\s*([^\n]+)/i
  ]);
  const recentChange = matchFirst(text, [
    /recent (?:change|changes):\s*([^\n]+)/i,
    /recent change:\s*([^\n]+)/i
  ]);
  const diskSignal = matchFirst(text, [
    /disk (?:signal|evidence|utilization):\s*([^\n]+)/i,
    /filesystem (?:signal|evidence|utilization):\s*([^\n]+)/i
  ]);
  const slowDependency = matchFirst(text, [
    /slow dependencies or services:\s*([^\n]+)/i,
    /(?:^|\n)service:\s*((?:claims|support)-[^\n]+)/i
  ]);
  const latencyEvidence = matchFirst(text, [
    /latency evidence:\s*([^\n]+)/i,
    /evidence of latency:\s*([^\n]+)/i
  ]);

  const parts = [likelyCause, recentChange, diskSignal, slowDependency, latencyEvidence]
    .filter((value): value is string => Boolean(value))
    .map((value) => value.replace(/\s+/g, " ").trim());
  const positiveParts = parts.filter((value) => !isNegativeEvidence(value));

  if (positiveParts.length > 0) {
    return positiveParts.join(" | ");
  }

  if (parts.length > 0 || isNegativeEvidence(text)) {
    return "Splunk AI did not confirm filesystem or APM evidence; keep remediation recommendation-only until signals are verified.";
  }

  return text.trim() || "AI Assistant summary pending.";
}

export function parseAssistantEvidence(input: AssistantEvidenceInput): ParsedAssistantEvidence {
  const text = (input.rawText ?? input.assistantResponseText ?? "").trim();
  const inferredTransaction = inferTransaction(text);
  const candidateActions = inferCandidateActions(text);
  const confidenceBand = inferConfidence(text);

  return {
    likelyCause: buildLikelyCauseSummary(text),
    confidenceBand,
    candidateActions,
    inferredTransaction
  };
}
