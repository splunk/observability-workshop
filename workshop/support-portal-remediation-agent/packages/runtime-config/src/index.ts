export type LocalServiceOptions = {
  baseUrlEnvVar: string;
  portEnvVar: string;
  defaultPort: number;
  defaultHost?: string;
  protocol?: "http" | "https";
};

export function localServicePort(
  env: Record<string, string | undefined>,
  portEnvVar: string,
  defaultPort: number
) {
  return Number(env[portEnvVar] ?? defaultPort);
}

export function localServiceUrl(
  env: Record<string, string | undefined>,
  { baseUrlEnvVar, portEnvVar, defaultPort, defaultHost = "127.0.0.1", protocol = "http" }: LocalServiceOptions
) {
  const configured = env[baseUrlEnvVar];
  if (configured) {
    return configured;
  }

  const port = localServicePort(env, portEnvVar, defaultPort);
  return `${protocol}://${defaultHost}:${port}`;
}

export const defaultPorts = {
  apiGateway: 18100,
  assistantService: 18101,
  caseService: 18102,
  knowledgeService: 18103,
  scenarioController: 18104,
  orchestrator: 18110,
  remediationAgent: 18800
} as const;
