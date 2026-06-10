import test from "node:test";
import assert from "node:assert/strict";
import {
  parseMcpHttpResponse,
  SplunkMcpClient
} from "../../apps/remediation-orchestrator/src/splunk-mcp-client.ts";

test("parseMcpHttpResponse accepts Splunk MCP event-stream responses", () => {
  const parsed = parseMcpHttpResponse(
    [
      "event: message",
      'data: {"jsonrpc":"2.0","id":"1","result":{"tools":[{"name":"get_apm_services"}]}}'
    ].join("\n")
  ) as { result: { tools: Array<{ name: string }> } };

  assert.equal(parsed.result.tools[0]?.name, "get_apm_services");
});

test("SplunkMcpClient gathers service, latency, metric, and trace evidence", async () => {
  const originalFetch = globalThis.fetch;
  const calls: Array<{ method: string; params: unknown }> = [];

  globalThis.fetch = (async (_url, init) => {
    const body = JSON.parse(String(init?.body)) as { method: string; params: { name?: string } };
    calls.push({ method: body.method, params: body.params });

    if (body.method === "tools/list") {
      return new Response(
        JSON.stringify({
          jsonrpc: "2.0",
          id: body.method,
          result: {
            tools: [
              tool("get_apm_services", ["environment"]),
              tool("get_apm_service_latency", ["serviceName", "environment", "start_time", "end_time"]),
              tool("get_apm_service_errors_and_requests", ["serviceName", "environment"]),
              tool("get_apm_exemplar_traces", ["serviceName", "environment"]),
              tool("execute_signalflow_program", ["program", "start_time", "end_time"])
            ]
          }
        })
      );
    }

    const name = body.params.name;
    const textByTool: Record<string, string> = {
      get_apm_services: "claims-knowledge claims-portal-api",
      get_apm_service_latency: '{"service":"claims-knowledge","p95LatencyMs":2400}',
      get_apm_service_errors_and_requests: '{"service":"claims-knowledge","errorRate":0.01,"requests":120}',
      get_apm_exemplar_traces: "traceId=0123456789abcdef0123456789abcdef service=claims-knowledge",
      execute_signalflow_program: "disk.utilization for /var/cache/claims-knowledge is above threshold"
    };

    return new Response(
      JSON.stringify({
        jsonrpc: "2.0",
        id: name,
        result: {
          content: [
            {
              type: "text",
              text: textByTool[name ?? ""] ?? ""
            }
          ]
        }
      })
    );
  }) as typeof fetch;

  try {
    const client = new SplunkMcpClient({
      enabled: true,
      url: "https://api.us1.signalfx.com/v2/mcp",
      accessToken: "token",
      realm: "us1",
      timeoutMs: 1000
    });
    const evidence = await client.gatherEvidence({
      detectorId: "det-1",
      detectorName: "Claims Knowledge Cache Volume Pressure",
      severity: "critical",
      triggeredAt: "2026-05-29T12:00:00Z",
      incidentId: "incident-1",
      dimensions: {
        service: "claims-knowledge",
        environment: "demo"
      }
    });

    assert.equal(calls[0]?.method, "tools/list");
    assert.ok(evidence.sources.includes("mcp:get_apm_service_latency"));
    assert.equal(evidence.suspectService, "claims-knowledge");
    assert.equal(evidence.p95LatencyMs, 2400);
    assert.equal(evidence.confidenceBand, "high");
    assert.deepEqual(evidence.traceIds, ["0123456789abcdef0123456789abcdef"]);
    assert.ok(evidence.observabilityResources?.some((resource) => resource.type === "metric"));
    assert.equal(evidence.approvalEvidence?.customerImpact[0]?.label, "POST /api/support/respond");
    assert.equal(evidence.approvalEvidence?.customerImpact[0]?.status, "confirmed");
    assert.equal(evidence.approvalEvidence?.backendImpact.find((metric) => metric.label.includes("p95"))?.value, 2400);
    assert.equal(evidence.approvalEvidence?.backendImpact.find((metric) => metric.label.includes("error"))?.value, 1);
    assert.equal(evidence.approvalEvidence?.backendImpact.find((metric) => metric.label.includes("error"))?.status, "not_confirmed");
    assert.equal(evidence.approvalEvidence?.impactChain.at(-1)?.status, "confirmed");
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("SplunkMcpClient maps Splunk MCP schema refs to cache metric queries", async () => {
  const originalFetch = globalThis.fetch;
  const originalInstance = process.env.INSTANCE;
  const calls: Array<{ method: string; params: { name?: string; arguments?: { params?: Record<string, unknown> } } }> = [];
  process.env.INSTANCE = "student-001";

  globalThis.fetch = (async (_url, init) => {
    const body = JSON.parse(String(init?.body)) as { method: string; params: { name?: string; arguments?: { params?: Record<string, unknown> } } };
    calls.push({ method: body.method, params: body.params });

    if (body.method === "tools/list") {
      return new Response(
        JSON.stringify({
          jsonrpc: "2.0",
          id: body.method,
          result: {
            tools: [
              schemaRefTool("get_apm_service_latency", "ServiceAnalysisParams", [
                "time_range",
                "service_name",
                "environment_name",
                "tags_or_dimensions"
              ]),
              schemaRefTool("execute_signalflow_program", "ExecuteSignalflowParams", [
                "time_range",
                "program",
                "resolution_ms"
              ])
            ]
          }
        })
      );
    }

    const name = body.params.name;
    const result =
      name === "execute_signalflow_program"
        ? {
            metadata: { series: { sf_originatingMetric: "claims_knowledge.cache.utilization" } },
            timeseries: { "1780084800000": { series: 92.4 } }
          }
        : { p95LatencyMs: 2400 };

    return new Response(JSON.stringify({ jsonrpc: "2.0", id: name, result }));
  }) as typeof fetch;

  try {
    const client = new SplunkMcpClient({
      enabled: true,
      url: "https://api.us1.signalfx.com/v2/mcp",
      accessToken: "token",
      realm: "us1",
      timeoutMs: 1000
    });
    const evidence = await client.gatherEvidence({
      detectorId: "det-1",
      detectorName: "Claims Knowledge Cache Volume Pressure",
      severity: "critical",
      triggeredAt: "2026-05-29T12:00:00Z",
      incidentId: "incident-1",
      dimensions: {
        service: "claims-knowledge",
        environment: "demo"
      }
    });

    const latencyCall = calls.find((call) => call.params.name === "get_apm_service_latency");
    const signalflowCalls = calls.filter((call) => call.params.name === "execute_signalflow_program");
    const latencyParams = latencyCall?.params.arguments?.params;
    const signalflowParams = signalflowCalls[0]?.params.arguments?.params;
    const signalflowPrograms = signalflowCalls.map((call) => String(call.params.arguments?.params?.program));

    assert.equal(latencyParams?.service_name, "claims-knowledge");
    assert.equal(latencyParams?.environment_name, "demo");
    assert.equal(typeof (latencyParams?.time_range as { start?: unknown })?.start, "string");
    assert.equal(typeof (latencyParams?.time_range as { stop?: unknown })?.stop, "string");
    assert.deepEqual(latencyParams?.tags_or_dimensions, {
      "app.business_transaction": ["claim_status_response"],
      "service.instance.id": ["student-001"]
    });
    assert.ok(signalflowPrograms.some((program) => /claims_knowledge\.cache\.utilization/.test(program)));
    assert.ok(signalflowPrograms.some((program) => /claims_knowledge\.claim_status\.latency_ms/.test(program)));
    assert.ok(signalflowPrograms.every((program) => !/disk\.utilization/.test(program)));
    assert.ok(signalflowPrograms.every((program) => /demo\.metric_source/.test(program)));
    assert.equal(typeof (signalflowParams?.time_range as { start?: unknown })?.start, "string");
    assert.equal(typeof (signalflowParams?.time_range as { stop?: unknown })?.stop, "string");
    assert.equal(signalflowParams?.resolution_ms, 30000);
    assert.equal(evidence.confidenceBand, "high");
    assert.equal(evidence.approvalEvidence?.infrastructureImpact[0]?.value, 92.4);
    assert.equal(evidence.approvalEvidence?.infrastructureImpact[0]?.status, "confirmed");
    assert.equal(evidence.approvalEvidence?.backendImpact.find((metric) => metric.label.includes("p95"))?.value, 2400);
  } finally {
    globalThis.fetch = originalFetch;
    if (originalInstance === undefined) {
      delete process.env.INSTANCE;
    } else {
      process.env.INSTANCE = originalInstance;
    }
  }
});

test("SplunkMcpClient does not treat SignalFlow decimals as trace ids", async () => {
  const originalFetch = globalThis.fetch;

  globalThis.fetch = (async (_url, init) => {
    const body = JSON.parse(String(init?.body)) as { method: string; params: { name?: string } };

    if (body.method === "tools/list") {
      return new Response(
        JSON.stringify({
          jsonrpc: "2.0",
          id: body.method,
          result: {
            tools: [
              tool("get_apm_service_latency", ["serviceName", "environment", "start_time", "end_time"]),
              tool("execute_signalflow_program", ["program", "start_time", "end_time"])
            ]
          }
        })
      );
    }

    const result =
      body.params.name === "execute_signalflow_program"
        ? {
            content: [
              {
                type: "text",
                text: JSON.stringify({
                  metadata: {
                    series: {
                      sf_originatingMetric: "claims_knowledge.claim_status.latency_ms"
                    }
                  },
                  timeseries: {
                    "1780102920000": {
                      series: 0.3666666666666667
                    }
                  }
                })
              }
            ]
          }
        : {
            content: [
              {
                type: "text",
                text: '{"service":"claims-knowledge","p95LatencyMs":0.3666666666666667}'
              }
            ]
          };

    return new Response(JSON.stringify({ jsonrpc: "2.0", id: body.params.name, result }));
  }) as typeof fetch;

  try {
    const client = new SplunkMcpClient({
      enabled: true,
      url: "https://api.us1.signalfx.com/v2/mcp",
      accessToken: "token",
      realm: "us1",
      timeoutMs: 1000
    });
    const evidence = await client.gatherEvidence({
      detectorId: "det-1",
      detectorName: "Claims Knowledge Cache Volume Pressure",
      severity: "critical",
      triggeredAt: "2026-05-29T12:00:00Z",
      incidentId: "incident-1",
      dimensions: {
        service: "claims-knowledge",
        environment: "demo"
      }
    });

    assert.deepEqual(evidence.traceIds, []);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

function tool(name: string, params: string[]) {
  return {
    name,
    inputSchema: {
      type: "object",
      properties: {
        params: {
          type: "object",
          properties: Object.fromEntries(params.map((param) => [param, { type: "string" }]))
        }
      }
    }
  };
}

function schemaRefTool(name: string, definitionName: string, params: string[]) {
  return {
    name,
    inputSchema: {
      type: "object",
      properties: {
        params: {
          $ref: `#/$defs/${definitionName}`
        }
      },
      $defs: {
        [definitionName]: {
          type: "object",
          properties: Object.fromEntries(params.map((param) => [param, { type: "string" }]))
        }
      }
    }
  };
}
