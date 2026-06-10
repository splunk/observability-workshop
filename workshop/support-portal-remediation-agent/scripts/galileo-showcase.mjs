#!/usr/bin/env node

export function buildShowcaseRequest(env = process.env) {
  return {
    orchestratorUrl: env.GALILEO_SHOWCASE_ORCHESTRATOR_URL ?? "http://127.0.0.1:18110",
    body: {
      incidentId: env.GALILEO_SHOWCASE_INCIDENT_ID ?? `galileo-cli-${Date.now()}`,
      executeRemediation: env.GALILEO_SHOWCASE_EXECUTE_REMEDIATION !== "false",
      includeUnsafeOperatorNote: env.GALILEO_SHOWCASE_UNSAFE_NOTE !== "false"
    }
  };
}

export function summarizeShowcaseResponse(payload) {
  return {
    incidentId: payload.incidentId,
    sessionId: payload.sessionId,
    project: payload.project,
    logStream: payload.logStream,
    traces: payload.showcaseTraces?.map((trace) => trace.name),
    guardrail: payload.guardrail?.status,
    recommendedAction: payload.plan?.recommendedAction,
    verification: payload.verification?.status,
    consoleUrl: payload.consoleUrl
  };
}

export async function runGalileoShowcaseCli({
  env = process.env,
  fetchImpl = fetch,
  stdout = console.log,
  stderr = console.error
} = {}) {
  const request = buildShowcaseRequest(env);
  const response = await fetchImpl(`${request.orchestratorUrl}/remediation/galileo/showcase`, {
    method: "POST",
    headers: {
      "content-type": "application/json"
    },
    body: JSON.stringify(request.body)
  });
  const payload = await response.json();

  if (!response.ok) {
    stderr(JSON.stringify(payload, null, 2));
    return 1;
  }

  stdout(JSON.stringify(summarizeShowcaseResponse(payload), null, 2));
  return 0;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  runGalileoShowcaseCli()
    .then((exitCode) => {
      if (exitCode !== 0) {
        process.exit(exitCode);
      }
    })
    .catch((error) => {
      console.error(error instanceof Error ? error.message : String(error));
      process.exit(1);
    });
}
