# Platform paths for Advanced Collector .conf26

The live lab always runs one agent-mode Collector. Platform differences affect
only where that process runs.

| Participant or target | Live workshop path | Persistent deployment path |
| --- | --- | --- |
| macOS Apple Silicon | Portable Darwin binary in `~/advanced-otel-workshop` | Use a supported Linux VM/EC2 host or Kubernetes for production |
| Linux amd64 or arm64 | Portable Linux binary in `~/advanced-otel-workshop` | Use the in-product Linux guided install or official installer |
| Windows or restricted company laptop | Splunk Show instance | Use the in-product Windows guided install or official MSI for Windows production hosts |
| Kubernetes | Outside the timed lab | Use the Splunk OpenTelemetry Collector Helm chart |

## Local macOS or Linux

Use the platform-specific download commands in the .conf26 Hugo guide, then run
`~/advanced-otel-workshop/setup-workshop.sh`. The prompt selects local-only or
optional Splunk Observability Cloud export. Both paths use one
`1-agent/agent_config.yaml` file and include local validation.
The same file retains a HEC-ready `logs` path and uses `logs/workshop` for the
live local log exercises. It also retains `metrics/internal` for Collector
self-monitoring, `logs/signalfx` for process-list events, and `logs/entities`
for discovery-mode entity events.

The macOS path does not install a daemon, require Homebrew or `sudo`, or modify
`/Library`. It is a temporary workshop runtime rather than a packaged
production installation.

## Splunk Show instance

Use `ec2-user-data.sh` on Amazon Linux 2023 or Ubuntu, or run it once before
creating an AMI. It stages the pinned Collector, load generator, and setup
script under the attendee's `~/advanced-otel-workshop` folder. It does not
store a Splunk token or run the attendee setup prompt.

The attendee flow requires SSH and `scp` so the generated YAML can move between
the browser computer and the host. Restrict port 22 to the event egress ranges
and provide one host per pair. Do not use Session Manager alone unless the
facilitator also supplies an equivalent file-transfer workflow.

## Persistent targets

- Linux: use the guided install or official installer so the Collector runs as
  a managed service.
- Windows: use the guided install or official MSI and Windows service.
- Kubernetes: use the Splunk Collector Helm chart in agent mode for the closest
  persistent equivalent to this workshop. Size and secure the deployment for
  the production telemetry path.

Local validation is required. Backend validation is optional for attendees who
enable cloud export.
