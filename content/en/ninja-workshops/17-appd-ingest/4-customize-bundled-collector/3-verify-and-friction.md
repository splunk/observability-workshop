---
title: 3. Verify
weight: 3
---

You should now have APM and infrastructure in both AppDynamics and Splunk Observability Cloud, all served by a single OTel collector process the AppD launcher manages. Confirm that, then look at exactly what running in this configuration required.

## Verify Splunk APM

1. Open **Splunk Observability Cloud**
2. Click **APM -> Service Map** in the left navigation panel.
3. In the **Environment** dropdown, choose `<INSTANCE>-appd-dual`. The workshop config's `resource/workshop` processor stamps that environment name on every signal regardless of what the Java agent sends.
4. Click the **OrderService** service bubble. 

![Splunk Observability Cloud APM](../../_images/o11y-apm.png?width=50vw)

5. Open **Traces** from the right menu
6. Click a `GET /order` trace.
7. Click the root span and confirm the AppDynamics correlation attributes are present:

![Splunk Observability Cloud APM with AppD attributes](../../_images/o11y-appd-attributes.png?width=50vw)

| Attribute | Example value |
|---|---|
| `appd.app.name` | `Dual-Ingest-YOURINITIALS` |
| `appd.tier.name` | `OrderService` |
| `appd.bt.name` | `/order` or `/inventory` |
| `appd.request.guid` | The AppDynamics request GUID |

These attributes are the proof that the trace went through a Java agent in dual mode and that the OTel pipeline preserved them all the way to Splunk.

{{% notice title="Give it a few minutes" style="info" icon="info-circle" %}}
Allow 2 to 5 minutes for the first traces to appear after restarting the Java app.
{{% /notice %}}

## Verify Splunk Infrastructure

The fastest way to confirm the bundled collector is shipping host metrics tagged with the same dimensions needed to correlate with your traces is to check the tiles for Infrastructure (and in some cases Logs) at the bottom of the screen. 

![Splunk Observability Cloud Infrastructure Correlation Tile](../../_images/o11y-Infra-Correlation.png?width=50vw)


## Verify AppDynamics is Unaffected

The AppD side of both signals continues to flow unchanged:

- **AppDynamics Controller > Applications > `Dual-Ingest-${INSTANCE}` > OrderService** still shows business transactions for `/order` and `/inventory`.
- **AppDynamics Controller > Servers** still shows the host with CPU, memory, disk, and network from the machine agent's SIM data.

Dual mode and the workshop OTel config do not touch the AppDynamics protocols, they only add an OTel pipeline alongside them.

## The Hidden Friction

Everything works! The problem is what it took to get here, and what is silently still broken.

### The lifecycle is glued to AppD

Stopping the machine agent stops the OTel collector with it. There is no `systemctl status otel-collector` and no separate journal (though they could be manually added). Restart the machine agent to pick up a config change and you also bounce all your OTel pipelines. 

More importantly an AppDynamics machine agent upgrade can also overwrite `conf/otel/agent_config.yaml` because it is part of the AppD install tree. You would need to manage that specific otel configuration file on the instance in some fashion.

### The collector binary is on AppD's release cadence

The OTel binary inside the AppD machine agent ships when AppD ships. 

OTel features and security fixes you might want from a more recent Splunk Distribution release have to wait for the next AppD machine agent release.

## What This Means

The bundled collector path is not wrong. The bundled collector is primarily intended as a stop gap or migration method.

For most teams running a Splunk Observability stack alongside AppDynamics, the standalone Splunk OTel Collector is a much better deal. The install script writes every `SPLUNK_*` environment variable into `/etc/otel/collector/splunk-otel-collector.conf`, ships the Smart Agent monitors like `smartagent/processlist` process data correctly, runs the collector as its own `systemd` service with independent restart and upgrade behavior, and follows the Splunk Distribution release cadence.

That is what Phase 4 sets up, using the same workshop `collector-config.yaml` you just used here. The difference between this phase and the next is almost entirely operational.
