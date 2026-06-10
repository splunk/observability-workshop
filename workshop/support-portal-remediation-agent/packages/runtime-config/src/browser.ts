import { defaultPorts } from "./index";

type BrowserEnv = Record<string, string | undefined>;

export function browserBaseUrl(env: BrowserEnv, envVar: string, defaultPort: number) {
  return env[envVar] ?? `http://127.0.0.1:${defaultPort}`;
}

function escapeRegex(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function buildCorsPropagationUrls(urls: string[]) {
  const patterns = new Map<string, RegExp>();

  for (const value of urls) {
    const parsed = new URL(value);
    const pathPrefix = parsed.pathname === "/" ? "/" : `${parsed.pathname.replace(/\/$/, "")}/`;
    const candidates =
      parsed.hostname === "127.0.0.1"
        ? ["127.0.0.1", "localhost"]
        : parsed.hostname === "localhost"
          ? ["localhost", "127.0.0.1"]
          : [parsed.hostname];

    for (const hostname of candidates) {
      const origin = `${parsed.protocol}//${hostname}${parsed.port ? `:${parsed.port}` : ""}`;
      patterns.set(origin, new RegExp(`^${escapeRegex(origin)}${escapeRegex(pathPrefix)}`));
    }
  }

  return Array.from(patterns.values());
}

export function browserAppConfig(env: BrowserEnv) {
  const apiBaseUrl = browserBaseUrl(env, "VITE_API_BASE_URL", defaultPorts.apiGateway);
  const orchestratorBaseUrl = browserBaseUrl(env, "VITE_ORCHESTRATOR_BASE_URL", defaultPorts.orchestrator);
  const scenarioControllerBaseUrl = browserBaseUrl(
    env,
    "VITE_SCENARIO_CONTROLLER_BASE_URL",
    defaultPorts.scenarioController
  );

  return {
    apiBaseUrl,
    orchestratorBaseUrl,
    scenarioControllerBaseUrl,
    tracePropagationUrls: buildCorsPropagationUrls([apiBaseUrl, orchestratorBaseUrl, scenarioControllerBaseUrl])
  };
}

export function currentBrowserAppConfig() {
  return browserAppConfig(import.meta.env as BrowserEnv);
}
