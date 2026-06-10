import test from "node:test";
import assert from "node:assert/strict";
import {
  buildShowcaseRequest,
  runGalileoShowcaseCli,
  summarizeShowcaseResponse
} from "../../scripts/galileo-showcase.mjs";

test("buildShowcaseRequest maps environment flags to the orchestrator payload", () => {
  const request = buildShowcaseRequest({
    GALILEO_SHOWCASE_ORCHESTRATOR_URL: "http://orchestrator.local",
    GALILEO_SHOWCASE_INCIDENT_ID: "incident-galileo-1",
    GALILEO_SHOWCASE_EXECUTE_REMEDIATION: "false",
    GALILEO_SHOWCASE_UNSAFE_NOTE: "false"
  });

  assert.equal(request.orchestratorUrl, "http://orchestrator.local");
  assert.deepEqual(request.body, {
    incidentId: "incident-galileo-1",
    executeRemediation: false,
    includeUnsafeOperatorNote: false
  });
});

test("summarizeShowcaseResponse returns the presenter-facing Galileo fields", () => {
  const summary = summarizeShowcaseResponse({
    incidentId: "incident-galileo-2",
    sessionId: "session-123",
    project: "ciscolive26",
    logStream: "remediation-agent",
    consoleUrl: "https://app.galileo.ai",
    showcaseTraces: [
      { name: "showcase.incident_intake" },
      { name: "showcase.guardrail_pre_action_check" }
    ],
    guardrail: { status: "blocked" },
    plan: { recommendedAction: "clean_claims_knowledge_cache" },
    verification: { status: "validated" }
  });

  assert.deepEqual(summary, {
    incidentId: "incident-galileo-2",
    sessionId: "session-123",
    project: "ciscolive26",
    logStream: "remediation-agent",
    traces: ["showcase.incident_intake", "showcase.guardrail_pre_action_check"],
    guardrail: "blocked",
    recommendedAction: "clean_claims_knowledge_cache",
    verification: "validated",
    consoleUrl: "https://app.galileo.ai"
  });
});

test("runGalileoShowcaseCli posts to the orchestrator and writes the summary", async () => {
  let requestedUrl = "";
  let requestedBody: unknown;
  const output: string[] = [];
  const errors: string[] = [];

  const exitCode = await runGalileoShowcaseCli({
    env: {
      GALILEO_SHOWCASE_ORCHESTRATOR_URL: "http://127.0.0.1:18110",
      GALILEO_SHOWCASE_INCIDENT_ID: "incident-cli-test"
    },
    fetchImpl: (async (url, init) => {
      requestedUrl = String(url);
      requestedBody = JSON.parse(String(init?.body));
      return new Response(
        JSON.stringify({
          incidentId: "incident-cli-test",
          project: "ciscolive26",
          logStream: "remediation-agent",
          showcaseTraces: [{ name: "showcase.triage_agent" }],
          guardrail: { status: "blocked" },
          plan: { recommendedAction: "clean_claims_knowledge_cache" },
          verification: { status: "validated" }
        })
      );
    }) as typeof fetch,
    stdout: (value) => output.push(value),
    stderr: (value) => errors.push(value)
  });

  assert.equal(exitCode, 0);
  assert.equal(requestedUrl, "http://127.0.0.1:18110/remediation/galileo/showcase");
  assert.deepEqual(requestedBody, {
    incidentId: "incident-cli-test",
    executeRemediation: true,
    includeUnsafeOperatorNote: true
  });
  assert.equal(errors.length, 0);
  assert.equal(JSON.parse(output[0] ?? "{}").recommendedAction, "clean_claims_knowledge_cache");
});
