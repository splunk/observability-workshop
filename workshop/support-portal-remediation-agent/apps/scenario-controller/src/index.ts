import cors from "@fastify/cors";
import Fastify from "fastify";
import { defaultPorts, localServicePort, localServiceUrl } from "@ibobs/runtime-config";
import {
  annotateServerEntrySpan,
  createServiceLogger,
  initSplunkNodeTelemetry
} from "@ibobs/telemetry";

export const scenarios = {
  cacheDiskPressure: {
    id: "cache-disk-pressure",
    name: "Claims knowledge cache volume pressure",
    affectedTransaction: "claim_status_response"
  }
};

let activeScenario = "healthy";
const knowledgeServiceBaseUrl = localServiceUrl(process.env, {
  baseUrlEnvVar: "KNOWLEDGE_SERVICE_BASE_URL",
  portEnvVar: "KNOWLEDGE_SERVICE_PORT",
  defaultPort: defaultPorts.knowledgeService
});

export function buildServer() {
  const app = Fastify({ loggerInstance: createServiceLogger("scenario-controller") });
  void app.register(cors, {
    origin: true,
    allowedHeaders: ["content-type", "traceparent", "tracestate", "baggage"],
    exposedHeaders: ["Server-Timing"]
  });
  app.addHook("preHandler", async (request) => {
    annotateServerEntrySpan({
      method: request.method,
      route: request.routeOptions.url
    });
    request.log.info(
      {
        http: { method: request.method, url: request.url },
        params: request.params,
        query: request.query,
        body: request.body
      },
      "request received"
    );
  });
  app.addHook("onResponse", async (request, reply) => {
    request.log.info(
      {
        http: { method: request.method, url: request.url, status_code: reply.statusCode }
      },
      "request completed"
    );
  });

  app.get("/scenario/state", async () => ({
    activeScenario,
    availableScenarios: Object.values(scenarios)
  }));

  app.post("/scenario/activate/:scenarioId", async (request) => {
    activeScenario = (request.params as { scenarioId: string }).scenarioId;
    request.log.info({ activeScenario }, "scenario activated");
    await fetch(`${knowledgeServiceBaseUrl}/knowledge/scenario`, {
      method: "POST",
      headers: {
        "content-type": "application/json"
      },
      body: JSON.stringify({ mode: activeScenario })
    });
    return { activeScenario };
  });

  app.post("/scenario/reset", async (request) => {
    activeScenario = "healthy";
    request.log.info({ activeScenario }, "scenario reset");
    await fetch(`${knowledgeServiceBaseUrl}/knowledge/scenario`, {
      method: "POST",
      headers: {
        "content-type": "application/json"
      },
      body: JSON.stringify({ mode: activeScenario })
    });
    return { activeScenario };
  });

  return app;
}

if (process.env.NODE_ENV !== "test") {
  initSplunkNodeTelemetry("scenario-controller");
  const port = localServicePort(process.env, "SCENARIO_CONTROLLER_PORT", defaultPorts.scenarioController);
  const server = buildServer();
  server.log.info({ scenarios }, "scenario-controller scaffold ready");
  server.listen({ port, host: "0.0.0.0" }).catch((error) => {
    server.log.error(error);
    process.exit(1);
  });
}
