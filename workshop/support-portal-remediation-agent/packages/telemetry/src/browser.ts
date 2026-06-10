export function buildRumConfig(applicationName: string) {
  return {
    applicationName,
    deploymentEnvironment: import.meta.env?.VITE_DEPLOYMENT_ENVIRONMENT ?? "demo",
    realm: import.meta.env?.VITE_SPLUNK_REALM ?? "us1",
    rumTokenConfigured: Boolean(import.meta.env?.VITE_SPLUNK_RUM_TOKEN),
    sessionReplayEnabled: import.meta.env?.VITE_SPLUNK_SESSION_REPLAY_ENABLED === "true",
    deactivatedReason: "RUM bootstrap wiring placeholder until token is configured."
  };
}
