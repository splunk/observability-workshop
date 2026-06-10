export const serviceNamespace = process.env.OTEL_SERVICE_NAMESPACE ?? "ibobs2002";
export const deploymentEnvironment = process.env.DEPLOYMENT_ENVIRONMENT ?? "demo";
export const appVersion =
  process.env.OTEL_SERVICE_VERSION ??
  process.env.APP_VERSION ??
  process.env.npm_package_version ??
  "0.1.0";
