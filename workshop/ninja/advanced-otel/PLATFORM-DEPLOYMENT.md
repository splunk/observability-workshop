# Platform paths for Advanced Collector Delta

The live lab always runs one agent-mode Collector. Platform differences affect
only where that process runs.

| Participant or target | Live workshop path | Persistent deployment path |
| --- | --- | --- |
| macOS Apple Silicon or Intel | Portable Darwin binary in `advanced-collector-delta` | Use a supported Linux VM/EC2 host or Kubernetes for production |
| Linux amd64 or arm64 | Portable Linux binary in `advanced-collector-delta` | Use the in-product Linux guided install or official installer |
| Windows or restricted company laptop | Facilitator-provided Linux host | Use the in-product Windows guided install or official MSI for Windows production hosts |
| Kubernetes | Outside the timed lab | Use the Splunk OpenTelemetry Collector Helm chart |

## Local macOS or Linux

```bash
git clone https://github.com/splunk/observability-workshop.git
cd observability-workshop
./workshop/ninja/advanced-otel/setup-workshop.sh --local
cd advanced-collector-delta
./run-collector.sh --local-only agent.yaml
```

When `SPLUNK_REALM` and `SPLUNK_ACCESS_TOKEN` are set locally, omit
`--local-only` to export host metrics and traces directly to Splunk
Observability Cloud.

The macOS path does not install a daemon, require Homebrew or `sudo`, or modify
`/Library`. It is a temporary workshop runtime rather than a packaged
production installation.

## Facilitator-provided Linux host

Use `ec2-user-data.sh` on Amazon Linux 2023 or Ubuntu, or run it once before
creating an AMI. It stages the lab under `/opt/advanced-collector-delta` and
does not store a Splunk token.

Prefer AWS Systems Manager Session Manager. If SSH is required, restrict port
22 to the event egress ranges. Provide one host per pair.

## Persistent targets

- Linux: use the guided install or official installer so the Collector runs as
  a managed service.
- Windows: use the guided install or official MSI and Windows service.
- Kubernetes: use the Splunk Collector Helm chart in agent mode for the closest
  persistent equivalent to this workshop. Size and secure the deployment for
  the production telemetry path.

Backend validation is required; local health alone does not prove ingestion.
