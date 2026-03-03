---
title: Wrap Up
linkTitle: 6. Wrap Up
weight: 6
archetype: chapter
time: 5 minutes
description: Key takeaways, cleanup instructions, and ideas for extending the workshop.
---

## Key Takeaways

1. **OBI instruments from the kernel.** No SDKs, no code changes, no recompilation. eBPF probes observe HTTP/gRPC traffic at the network level.

2. **Context propagation happens at the network level.** OBI injects `Traceparent` headers into outgoing HTTP requests, linking traces across services -- even when those services have zero knowledge of tracing.

3. **The deployment pattern is consistent.** Whether you're on bare metal, Docker, or Kubernetes, the approach is the same: run OBI alongside your apps and point it at a collector.

4. **This solves real enterprise problems.** Legacy apps, compiled binaries, regulatory constraints, developer resistance -- OBI gives you observability without requiring anyone to change their code.

## Cleanup

### Kubernetes

``` bash
helm uninstall splunk-otel-collector
kubectl delete namespace obi-workshop
```

### Docker

``` bash
cd ~/workshop/obi/02-obi-docker
docker-compose down
```

### Phase 0 (Python)

``` bash
sudo pkill -f ./obi 2>/dev/null
kill %1 2>/dev/null
```

## Extending the Workshop

Once you've completed all phases, here are ideas for using an LLM (Cursor, Copilot, ChatGPT, etc.) to extend the workshop:

### Add a New Endpoint

Ask the LLM to add a `GET /order-status/:id` endpoint to `order-processor`. OBI will trace it automatically -- no config changes needed (it already watches port 8080).

### Add a New Service

Ask the LLM to create an `inventory-service` in Python (Flask) on port 8082. You'll need to:

- Create the service code and Dockerfile
- Add it to `docker-compose.yaml`
- Add port 8082 to `obi-config.yaml`

### Add Error Scenarios

Ask the LLM to make `payment-service` randomly fail 20% of the time with a 500 status. Then add retry logic in `order-processor`. Watch the error rates appear in Splunk APM.

### Add Latency Simulation

Ask the LLM to add random 100-500ms latency in `payment-service`. Watch the latency distribution appear in Splunk APM's service view.

{{% notice title="Note" style="info" %}}
When extending:

- Do **not** add OpenTelemetry SDKs -- the whole point is zero-code instrumentation
- Keep services on the Docker network; avoid `localhost` for inter-service calls
- Update `obi-config.yaml` when adding new ports
- Rebuild after code changes: `docker-compose up --build -d`
{{% /notice %}}
