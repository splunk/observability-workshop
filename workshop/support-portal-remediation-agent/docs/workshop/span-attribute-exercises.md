# Default Signal Exercises

These exercises teach students how to use standard Splunk Observability signals for the lab without adding custom application metrics or relying on logs.

## Learning goals

Students should be able to:

- separate lab data with `INSTANCE` and OpenTelemetry resource attributes
- identify the claims portal journey in RUM/APM
- find `claims-knowledge` latency in APM
- find cache pressure through host filesystem metrics
- inspect remediation service spans in Splunk and agent/model traces in Galileo

## Exercise 1: Set student identity

Set a unique instance value:

```dotenv
INSTANCE=student-001
OTEL_RESOURCE_ATTRIBUTES=lab.name=ciscolive26,lab.student.id=student-001,service.instance.id=student-001,host.name=student-001,deployment.environment=demo
```

Restart the stack after changing `.env`.

Expected result:

- Splunk queries can filter by `service.instance.id=student-001`
- lab dashboards can filter by `lab.student.id=student-001`

Discussion prompt:

> Why do we need a student identity when the class shares one Splunk Observability account?

Expected answer:

Shared accounts are fine for a workshop, but every participant needs a filter boundary so their signals do not blend together.

## Exercise 2: Generate baseline signals

In the claims portal:

1. run `AI Claim Status`
2. run `Policy Coverage Lookup`
3. run `Claims FAQ Search`

In Splunk:

- open APM and find services such as `claims-portal-api`, `claims-assistant`, and `claims-knowledge`
- open RUM or Digital Experience and inspect the portal activity if RUM is configured

Discussion prompt:

> Why should we create healthy baseline traffic before triggering the incident?

Expected answer:

Baseline traffic proves the system works and gives the degraded state something to compare against.

## Exercise 3: Trigger cache pressure

Click `Trigger Cache Pressure`.

Then run `AI Claim Status` again.

Optional local checks:

```bash
curl -s http://127.0.0.1:18104/scenario/state
curl -s http://127.0.0.1:18103/knowledge/cache/status
```

Expected result:

- scenario state is `cache-disk-pressure`
- cache utilization rises
- AI Claim Status gets slower

## Exercise 4: Find the default metrics

In Splunk Observability:

1. Filter to the student `INSTANCE`.
2. In Infrastructure Monitoring, find filesystem utilization.
3. In APM, find `claims-knowledge` request duration.
4. In RUM, use `Pages` or `Network Requests` to confirm portal traffic if browser data is available.
5. Open `/api/support/respond` in `Network Requests` if it appears.
6. In APM, inspect the AI Claim Status trace path as the reliable backend proof.

Signals to look for:

- `disk.utilization`
- `service.request.duration.ns`
- `service.request`
- RUM/browser spans for the portal journey

Discussion prompt:

> Why is host filesystem utilization stronger evidence than a synthetic custom metric called cache_full?

Expected answer:

It is a standard infrastructure signal. Students can apply the same skill to real hosts and containers instead of learning a one-off demo metric.

## Exercise 5: Inspect the remediation agent

In the operator console:

1. gather MCP evidence
2. open the evidence package
3. request a proposed action
4. approve `clean_claims_knowledge_cache`

In Splunk APM and Galileo, inspect:

- `remediation-orchestrator`
- `remediation-agent`
- Galileo model provider call metadata, when `OPENAI_API_KEY` and `GALILEO_API_KEY_FILE` or `GALILEO_API_KEY` are set
- action attributes such as `action.type=clean_claims_knowledge_cache`

Discussion prompt:

> Why do we keep policy and approval outside the model response?

Expected answer:

The model can help choose a bounded action, but deterministic policy and human approval define what is allowed to execute.

## Exercise 6: Verify recovery

After approval:

1. run `AI Claim Status`
2. check the operator validation panel
3. check filesystem utilization and APM duration again

Expected result:

- scenario state returns to `healthy`
- claim status response latency improves
- cache utilization drops or stops increasing

## Instructor notes

- Keep the story focused on default Splunk signals.
- Do not introduce logs as required evidence.
- Do not ask students to add custom metrics for the incident.
- Use custom span/resource attributes only for trace filtering and lab identity.
