# Advanced Collector .conf26 facilitator guide

This workshop uses one agent-mode Collector, one `agent_config.yaml`, and one
`loadgen` process. The detailed
attendee instructions live in the Hugo page
`content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector-conf2026/`.

## Delivery objective

Participants should leave with one repeatable workflow:

1. Understand an existing Collector configuration.
2. Make a focused policy decision in OTel Collector Config Builder.
3. Export the complete YAML and restart safely.
4. Prove the outcome with new telemetry.

## Run of show

| Segment | Time | Facilitator checkpoint |
| --- | ---: | --- |
| Pair, register, and open the online guide | 5 min | Pair anyone waiting for organization activation |
| Download binaries or enter the remote host | 5 min | Everyone reaches `~/advanced-otel-workshop` |
| Run one Collector and `loadgen` | 10 min | Host metrics and `cinema-service` traces are visible or local debug works |
| Review `agent_config.yaml` in Config Builder | 5 min | Participants can identify eight pipelines: six defaults and two workshop paths |
| Optimize volume and trace policy | 13 min | Use the facilitator solution only when a pair cannot finish |
| Restart and validate with new telemetry | 13 min | Preserve evidence for metrics, traces, filtering, and privacy |
| Take-home and wrap-up | 4 min | Point to Platform logs and profiling extensions |

The timed lab, including wrap-up, is 55 minutes.

## Environment routing

- **Local Apple Silicon/Linux:** attendees download the matching v0.157.0
  Collector and `loadgen`, then run `./setup-workshop.sh`.
- **Windows or restricted laptop:** use one Splunk Show instance per
  pair over restricted SSH. The attendee's browser computer must also have
  `scp` for the two YAML transfer steps.
- **Cloud export:** the setup prompt writes each participant's realm and ingest
  token to a mode-600 `workshop-env.sh`. Tokens are not stored in the AMI or
  YAML.
- **Local-only path:** pressing Enter at the setup prompt keeps trace, log, and
  throttled workshop-metric validation local. The normal host-metrics pipeline
  plus `metrics/internal`, `logs/signalfx`, and `logs/entities` use `nop`
  instead of cloud exporters.
- **Log paths:** `logs/workshop` owns the live debug/file exercise. The retained
  `logs` pipeline stays on `nop` until the take-home HEC configuration;
  `logs/signalfx` retains the default process-list path, and `logs/entities`
  remains unchanged for discovery mode.

## One-agent process model

Participants run one Collector process and invoke the same load generator for
the baseline, health, and log checks:

```text
otelcol --config=agent_config.yaml
loadgen -count 5
loadgen -health -count 5
loadgen -logs -json -count 5
```

There is no `gateway.yaml`, gateway listener, agent-to-gateway exporter, or
second Collector process. Participants restart the same Agent once after they
replace its configuration in Chapter 5.

## Support boundaries

- If registration is still pending, pair the participant with a working
  organization or use local-only mode.
- If Config Builder work is incomplete at minute 10 of the optimization block,
  use the facilitator-only `agent_config.solution.yaml` in the .conf26 content
  folder and apply the same local-only exporter replacements as the setup
  script when cloud export is disabled.
- Keep the optional syslog receiver, Platform log export, Log Observer Connect,
  and profiling in the take-home path.
- Keep the live lab on Collector v0.157.0. The take-home section links to
  current Splunk documentation for Platform logs and AlwaysOn Profiling.

Local post-processing validation is required. Backend validation is optional
for attendees who enable cloud export.
