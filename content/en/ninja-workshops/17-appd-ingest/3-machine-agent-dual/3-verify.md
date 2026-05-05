---
title: 3. Verify in Both Platforms
weight: 3
---

You should now see infrastructure metrics for the same host in both AppDynamics Server Visibility and Splunk Observability Cloud Infrastructure.

## Verify Infrastructure in AppDynamics

1. Open the [AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/).
2. Open your application (`Dual-Ingest-${INSTANCE}`).
3. Navigate to **Servers** in the left navigation panel.
4. You should see your host (matching the `${INSTANCE}` you set as `appdynamics.agent.uniqueHostId`).

Server Visibility (SIM) shows CPU, memory, disk, network, and process metrics. The Java APM data from Phase 1 still flows under the **OrderService** tier in the same application.

{{% notice title="Patience" style="info" icon="info-circle" %}}
It can take 2 to 5 minutes for the host to appear in **Servers** after the machine agent first starts.
{{% /notice %}}

![AppD Server Visibility row showing the workshop host with CPU, memory, disk, and network metrics](../../_images/appd-machine-agent-metrics.png)

## Verify Infrastructure in Splunk Observability Cloud

The fastest way to confirm the bundled collector is shipping host metrics tagged with your workshop identity is to chart a single metric and filter by `host.name`:

1. Open Splunk Observability Cloud (E.G. https://app.us1.signalfx.com).
2. Click **Metric Finder** in the left navigation panel.
3. Search for [`cpu.utilization`](https://app.us1.signalfx.com/#/chart/v2/new?template=default&filters=sf_metric:cpu.utilization) and click the metric to open the chart.
4. Add a filter: `host.name=${INSTANCE}` (use your actual `${INSTANCE}` value, for example `shw-40fb`).

You should see a live time series for that single host. The data path is the bundled `hostmetrics` receiver inside the machine agent's collector, exported through the `signalfx` exporter to Splunk Observability Cloud. `host.name` matches `${INSTANCE}` because the workshop instance's OS hostname is set to that value, and the bundled config's `resourcedetection` processor reads it from the system.

`deployment.environment` is also stamped on every metric, set from the `DEPLOYMENT_ENVIRONMENT=${INSTANCE}-appd-machine` env var you exported on the previous page. You can add that as a second filter to narrow further or use it to find the host in **Infrastructure > Hosts**.

![Splunk Observability Cloud Infrastructure Monitoring](../../_images/o11y-infra-metrics-appd-machine-agent.png)

## What You Don't See Yet

Open **APM** in Splunk Observability Cloud. The **OrderService** service is **not** there. APM data from the Java agent still flows only to AppDynamics because we have not enabled dual signal mode on the Java agent yet.

You also will not see this host correctly light up the **Infrastructure -> Overview -> Hosts** Navigators due to missing dimensions stamped by the workshop's `resource/workshop` processor, which is not part of the bundled config.

**Phase 3** closes both gaps without leaving the bundled collector. You drop the workshop's full `collector-config.yaml` in place of the AppD-shipped `agent_config.yaml`, export the env vars the workshop config needs, and turn on dual signal mode on the Java agent. **Phase 4** then takes the same workshop config and runs it under the standalone Splunk OTel Collector install for the lifecycle, env var, and Smart Agent bundle wins.

## Where to Look if Something is Off

| Symptom | First place to look |
|---|---|
| No host in Splunk Infrastructure | `~/workshop/appd/machine-agent/logs/otel/otel-collector.log` |
| No host in AppD Server Visibility | `~/workshop/appd/machine-agent/logs/machine-agent.log`, confirm `-Dappdynamics.sim.enabled=true` |
| Bundled collector did not start | Confirm `SPLUNK_OTEL_ENABLED=true` is exported in the same shell that ran `bin/machine-agent` |
