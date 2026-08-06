# Advanced Collector Delta facilitator skeleton

This workshop replaces the previous agent-and-gateway topology with one
agent-mode Collector, one `agent.yaml`, and one `loadgen` process. The detailed
attendee instructions live in the Hugo page
`content/en/ninja-workshops/foundations/2-opentelemetry-collector-workshops/2-advanced-collector/lab-guide.md`.

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
| Download binaries or enter the remote host | 5 min | Everyone reaches `advanced-collector-delta` |
| Run one Collector and `loadgen` | 10 min | Host metrics and `cinema-service` traces are visible or local debug works |
| Review `agent.yaml` in Config Builder | 5 min | Participants can explain the three pipelines |
| Optimize volume and trace policy | 15 min | Move late pairs to `agent-solution.yaml` after 10 minutes |
| Restart and validate with new telemetry | 15 min | Preserve evidence for metrics, traces, filtering, and privacy |
| Take-home and wrap-up | up to 5 min | Point to Platform logs and profiling extensions |

The timed lab is 55 minutes. Use no more than five additional minutes for the
wrap-up.

## Environment routing

- **Local macOS/Linux:** run `setup-workshop.sh --local`. The script downloads
  the matching v0.157.0 portable Collector and stages the lab without a system
  service. The download is verified against the release checksum.
- **Windows or restricted laptop:** use one facilitator-provided Linux host per
  pair over AWS Systems Manager Session Manager or restricted SSH.
- **Cloud export:** participants set their own realm and organization access
  token in their shell. Tokens are never stored in the AMI, setup script, or
  YAML.
- **Local-only fallback:** run `./run-collector.sh --local-only agent.yaml`.
  This keeps metrics, traces, and logs in the debug exporter.

## One-agent process model

Only these participant processes should run:

```text
otelcol --config agent.yaml
loadgen -correlated -health -security
```

There is no `gateway.yaml`, gateway listener, agent-to-gateway exporter, or
second Collector restart sequence.

## Support boundaries

- If registration is still pending, pair the participant with a working
  organization or use local-only mode.
- If Config Builder work is incomplete at minute 10 of the optimization block,
  copy `agent-solution.yaml` to `agent.yaml` and continue to validation.
- If a participant adds syslog, use
  `agent-solution-with-syslog.yaml` as the fallback.
- Keep the optional syslog receiver, Platform log export, Log Observer Connect,
  and profiling in the take-home path.
- The pinned v0.157.0 build includes profile-signal support in the `splunk_hec`
  exporter and configuration providers for production secret-management
  follow-ups. The live lab intentionally keeps secrets in environment variables,
  and its load generator does not emit profiles.

Backend validation is required; local health alone does not prove ingestion.
