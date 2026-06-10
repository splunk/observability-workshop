import test from "node:test";
import assert from "node:assert/strict";

test("agent monitoring reports configured when the agent says Galileo is ready", async () => {
  const originalFetch = globalThis.fetch;
  const originalNodeEnv = process.env.NODE_ENV;
  const originalAgentBaseUrl = process.env.REMEDIATION_AGENT_BASE_URL;
  const originalGalileoApiKey = process.env.GALILEO_API_KEY;
  const originalGalileoApiKeyFile = process.env.GALILEO_API_KEY_FILE;

  process.env.NODE_ENV = "test";
  process.env.REMEDIATION_AGENT_BASE_URL = "http://agent.local";
  delete process.env.GALILEO_API_KEY;
  delete process.env.GALILEO_API_KEY_FILE;

  globalThis.fetch = (async (url) => {
    assert.equal(String(url), "http://agent.local/agent/health");
    return new Response(
      JSON.stringify({
        status: "ok",
        model: "gpt-4.1-mini",
        telemetry: "enabled",
        agentMonitoring: "galileo"
      })
    );
  }) as typeof fetch;

  const { buildServer } = await import("../../apps/remediation-orchestrator/src/index.ts");
  const app = buildServer();

  try {
    const response = await app.inject({
      method: "GET",
      url: "/remediation/agent-monitoring"
    });
    const payload = response.json();

    assert.equal(response.statusCode, 200);
    assert.equal(payload.status, "ready");
    assert.equal(payload.apiKeyConfigured, true);
    assert.equal(payload.apiKeySource, "agent");
    assert.equal(payload.agent.agentMonitoring, "galileo");
  } finally {
    await app.close();
    globalThis.fetch = originalFetch;
    if (originalNodeEnv === undefined) {
      delete process.env.NODE_ENV;
    } else {
      process.env.NODE_ENV = originalNodeEnv;
    }
    if (originalAgentBaseUrl === undefined) {
      delete process.env.REMEDIATION_AGENT_BASE_URL;
    } else {
      process.env.REMEDIATION_AGENT_BASE_URL = originalAgentBaseUrl;
    }
    if (originalGalileoApiKey === undefined) {
      delete process.env.GALILEO_API_KEY;
    } else {
      process.env.GALILEO_API_KEY = originalGalileoApiKey;
    }
    if (originalGalileoApiKeyFile === undefined) {
      delete process.env.GALILEO_API_KEY_FILE;
    } else {
      process.env.GALILEO_API_KEY_FILE = originalGalileoApiKeyFile;
    }
  }
});
