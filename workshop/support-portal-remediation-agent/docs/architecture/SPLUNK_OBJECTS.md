# Splunk Objects

## Dashboards to provision as code

- Executive Story
- APM Service Requests
- Digital Experience
- Service Health
- Remediation Operations
- Galileo remediation-agent companion view, configured outside Splunk

## Detectors to provision as code

- Claims Knowledge Cache Filesystem Pressure
- Claims Knowledge APM Latency
- Claims Knowledge APM Error Rate

## Signal source

Use default Splunk Observability signals:

- `disk.utilization`
- `service.request`
- `service.request.duration.ns`
- RUM and browser spans
- remediation service spans

## Provisioning direction

Use `infra/splunk/specs` for iterative dashboard and detector authoring. Use Terraform when you need managed state and controlled rollout.
