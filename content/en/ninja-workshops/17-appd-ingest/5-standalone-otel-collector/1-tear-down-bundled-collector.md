---
title: 1. Free Up the OTel Listener for the Standalone Install
weight: 1
---

The bundled OTel collector inside the AppDynamics machine agent and the standalone Splunk OTel Collector both bind to OTLP ports `4317` and `4318` on the same host. Stop the bundled side first, leaving the AppDynamics machine agent itself running so AppDynamics Server Visibility keeps reporting. The Java app stays running in dual mode the whole time the OTLP outage is short and the AppD APM channel is unaffected.

## Stop the Machine Agent and Its Bundled Collector

Use the pidfiles the launcher wrote in Phase 3:

```bash
cd ~/workshop/appd/machine-agent

kill "$(cat machine-agent.pid)"  2>/dev/null || true
kill "$(cat otel-collector.pid)" 2>/dev/null || true
rm -f machine-agent.pid otel-collector.pid
```

If either pidfile is missing or stale, fall back to `pkill -f machineagent.jar` and `pkill -f otelcol_linux_amd64`.

## Confirm the OTLP Ports Are Free

```bash
sudo ss -lntp | grep -E ':4317|:4318|:13133' || echo "ports clear"
```

You should see `ports clear`. If anything is still listening, kill it before continuing.

## Restart the Machine Agent in AppD-only Mode

Re-run the launcher **without** `SPLUNK_OTEL_ENABLED=true` so the bundled OTel collector stays off and the machine agent process keeps feeding Server Visibility:

```bash
unset SPLUNK_OTEL_ENABLED

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

You should now have:

- **AppDynamics**: APM from the Java agent (still in dual mode) **plus** Server Visibility from the machine agent.
- **Splunk Observability Cloud**: a brief gap while the OTLP listener is down. The Java app continues to send to `localhost:4318` and will retry once the standalone collector comes up next.

{{% notice title="Why not stop the Java app too" style="info" icon="info-circle" %}}
The Java app from Phase 3 is already in dual signal mode and configured to export OTLP to `localhost:4318`. As soon as the standalone collector starts listening on those ports in the next step, the Java app's traces resume without restart. Killing it here would just create more work.
{{% /notice %}}

Move on to install the standalone Splunk OTel Collector.
