---
title: 1. Apply the Workshop Config to the Bundled Collector
weight: 1
---

You will:

1. Stop the bundled collector that came up in Phase 2 (which means stopping the machine agent, since the launcher owns the OTel process).
2. Back up the bundled `agent_config.yaml`.
3. Drop the workshop `collector-config.yaml` into the AppD install in place of it.
4. Export the additional environment variables the workshop config needs that the AppD launcher does not set.
5. Start the machine agent again so the bundled collector comes back up running the workshop config.

## Stop the Combined Machine Agent

Use the pidfiles the launcher wrote in Phase 2:

```bash
cd ~/workshop/appd/machine-agent

kill "$(cat machine-agent.pid)"  2>/dev/null || true
kill "$(cat otel-collector.pid)" 2>/dev/null || true
rm -f machine-agent.pid otel-collector.pid
```

Confirm the OTLP and health-check ports are clear before continuing:

```bash
sudo ss -lntp | grep -E ':4317|:4318|:13133' || echo "ports clear"
```

You should see `ports clear`.

## Back Up the Bundled Config

The default `conf/otel/agent_config.yaml` is what the AppD machine agent ships. Save it before overwriting so you can revert by restoring it:

```bash
cd ~/workshop/appd/machine-agent

cp conf/otel/agent_config.yaml conf/otel/agent_config.yaml.appd-default
```

## See How Much You're About to Add

Before you swap the file, compare what AppD ships against what you are about to drop in. The bundled config is intentionally narrow per the [Combined Agent docs](https://help.splunk.com/en/appdynamics-on-premises/infrastructure-visibility/26.4.0/machine-agent/combined-agent-for-infrastructure-visibility): a `hostmetrics` receiver feeding the `signalfx` exporter, plus the minimal extensions and processors AppD wires up to make that work. The workshop config adds additional receivers for OTLP data, custom resource, correlation, and high-cardinality protection processors. But most importantly they include the `splunk_hec` and `otlp_http` exporters along with the trace, log, and profiling pipelines those exporters need.

Count the line delta first:

```bash
wc -l conf/otel/agent_config.yaml.appd-default ~/workshop/appd/collector-config.yaml
```

Then look at the diff. The full output is several hundred lines, so pipe through `less`:

```bash
diff -u conf/otel/agent_config.yaml.appd-default ~/workshop/appd/collector-config.yaml | less
```


Everything that diff shows is something the AppD bundle does not configure for you. That is the work the standalone install takes care of all of this.

## Drop the Workshop Config Into the AppD Install

```bash
cp ~/workshop/appd/collector-config.yaml conf/otel/agent_config.yaml
```

That's it. The same config you would point the standalone collector at in Phase 4 now sits inside the AppD machine agent install.

## Export the Environment Variables the Workshop Config Needs

The workshop `collector-config.yaml` references variables the AppD launcher does not set. Export them in the same shell you will start the machine agent from:

```bash
export SPLUNK_OTEL_ENABLED=true
export SPLUNK_ACCESS_TOKEN=${ACCESS_TOKEN}
export SPLUNK_REALM=${REALM}

export SPLUNK_INGEST_URL=https://ingest.${REALM}.signalfx.com
export SPLUNK_API_URL=https://api.${REALM}.signalfx.com
export SPLUNK_HEC_TOKEN=${HEC_TOKEN}
export SPLUNK_HEC_URL=${HEC_URL}
export SPLUNK_LISTEN_INTERFACE=0.0.0.0
export SPLUNK_MEMORY_LIMIT_MIB=512
export SPLUNK_BUNDLE_DIR=/usr/lib/splunk-otel-collector/agent-bundle
export SPLUNK_COLLECTD_DIR=/usr/lib/splunk-otel-collector/agent-bundle/run/collectd
```

Notice the count. The first three lines are what Phase 2 needed. The next eight are required to be manually set for the machine agent. The Splunk OpenTelemetry Collector Distro by default handles most of these environment variables.

The workshop config's `resource/workshop` processor stamps `deployment.environment=${INSTANCE}-appd-dual` on every signal regardless of what the Java agent sends, so we do not need `DEPLOYMENT_ENVIRONMENT` exported here.

| Variable | Why the workshop config needs it | Set by AppD launcher? |
|---|---|---|
| `SPLUNK_INGEST_URL` | `signalfx.ingest_url`, `splunk_hec/profiling.endpoint`, `otlp_http.traces_endpoint` | No |
| `SPLUNK_API_URL` | `signalfx.api_url`, `http_forwarder` egress | No |
| `SPLUNK_HEC_TOKEN` | `splunk_hec.token` (logs export) | No |
| `SPLUNK_HEC_URL` | `splunk_hec.endpoint` (logs export) | No |
| `SPLUNK_LISTEN_INTERFACE` | All receivers and extensions bind to `${SPLUNK_LISTEN_INTERFACE}:<port>` | No |
| `SPLUNK_MEMORY_LIMIT_MIB` | `memory_limiter.limit_mib` | No |
| `SPLUNK_BUNDLE_DIR` | `smartagent` extension `bundleDir` (the bundle is not present on disk) | No |
| `SPLUNK_COLLECTD_DIR` | `smartagent` extension `collectd.configDir` (also not present) | No |

The bundle directory `/usr/lib/splunk-otel-collector/agent-bundle` does not exist yet because the AppD machine agent install does not ship it. The smartagent extension will start with the value, the `smartagent/processlist` receiver will fail every scrape because there is no bundle to load monitors from. That is one of the gaps Phase 4 closes.

## Restart the Machine Agent

Use the same launcher invocation as Phase 2. The launcher detects `SPLUNK_OTEL_ENABLED=true` and starts the bundled collector with the new config:

```bash
cd ~/workshop/appd/machine-agent

./bin/machine-agent -p ./machine-agent.pid -d \
  -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com \
  -Dappdynamics.controller.port=443 \
  -Dappdynamics.controller.ssl.enabled=true \
  -Dappdynamics.agent.applicationName=${APPD_APP_NAME} \
  -Dappdynamics.agent.tierName=OrderService \
  -Dappdynamics.agent.nodeName=OrderService-Machine-Node \
  -Dappdynamics.agent.accountName=se-lab \
  -Dappdynamics.agent.accountAccessKey=${APPD_ACCESS_KEY} \
  -Dappdynamics.agent.uniqueHostId=${INSTANCE} \
  -Dappdynamics.sim.enabled=true
```

You should see the launcher pick up the workshop config

## Verify the Bundled Collector Started With the Workshop Config

The workshop config opens the same OTLP, Jaeger, Zipkin, and health-check ports the standalone install does. Confirm a few are listening now that they were not before:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
curl -s http://localhost:13133/ | jq
sudo ss -lntp | grep -E ':4317|:4318|:9411|:13133'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
{
  "status": "Server available",
  "upSince": "2026-05-04T20:30:11.412Z",
  "uptime": "8.221s"
}
LISTEN 0  4096   *:4317   *:*  users:(("otelcol_linux_a",pid=...,fd=...))
LISTEN 0  4096   *:4318   *:*  users:(("otelcol_linux_a",pid=...,fd=...))
LISTEN 0  4096   *:9411   *:*  users:(("otelcol_linux_a",pid=...,fd=...))
LISTEN 0  4096   *:13133  *:*  users:(("otelcol_linux_a",pid=...,fd=...))
```

{{% /tab %}}
{{< /tabs >}}

The bundled collector is now ready to accept OTLP from the Java agent. Move on to enable dual signal mode and point the Java app at it.
