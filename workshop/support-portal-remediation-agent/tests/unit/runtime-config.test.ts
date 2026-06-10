import test from "node:test";
import assert from "node:assert/strict";
import { browserAppConfig, buildCorsPropagationUrls } from "../../packages/runtime-config/src/browser.ts";
import { defaultPorts, localServicePort, localServiceUrl } from "../../packages/runtime-config/src/index.ts";

test("localServiceUrl derives a base URL from the matching port when no explicit URL is set", () => {
  const value = localServiceUrl(
    {
      API_GATEWAY_PORT: "4100"
    },
    {
      baseUrlEnvVar: "API_GATEWAY_BASE_URL",
      portEnvVar: "API_GATEWAY_PORT",
      defaultPort: defaultPorts.apiGateway
    }
  );

  assert.equal(value, "http://127.0.0.1:4100");
});

test("localServiceUrl prefers an explicit base URL over derived localhost defaults", () => {
  const value = localServiceUrl(
    {
      REMEDIATION_AGENT_BASE_URL: "http://remediation-agent:18800",
      REMEDIATION_AGENT_PORT: "8999"
    },
    {
      baseUrlEnvVar: "REMEDIATION_AGENT_BASE_URL",
      portEnvVar: "REMEDIATION_AGENT_PORT",
      defaultPort: defaultPorts.remediationAgent
    }
  );

  assert.equal(value, "http://remediation-agent:18800");
});

test("localServicePort returns a numeric port using defaults when unset", () => {
  assert.equal(localServicePort({}, "ORCHESTRATOR_PORT", defaultPorts.orchestrator), 18110);
});

test("browserAppConfig derives default local URLs from shared ports", () => {
  const config = browserAppConfig({});

  assert.equal(config.apiBaseUrl, "http://127.0.0.1:18100");
  assert.equal(config.orchestratorBaseUrl, "http://127.0.0.1:18110");
  assert.equal(config.scenarioControllerBaseUrl, "http://127.0.0.1:18104");
});

test("buildCorsPropagationUrls supports both localhost and 127.0.0.1 aliases for local services", () => {
  const patterns = buildCorsPropagationUrls(["http://127.0.0.1:18100"]);

  assert.equal(patterns.some((pattern) => pattern.test("http://127.0.0.1:18100/api/support/respond")), true);
  assert.equal(patterns.some((pattern) => pattern.test("http://localhost:18100/api/support/respond")), true);
});
