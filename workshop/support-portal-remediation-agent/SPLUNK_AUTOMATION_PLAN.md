# Splunk Automation Plan

## Goal

Provision as much of the Splunk Observability Cloud configuration as possible from code.

This project should avoid manual dashboard and detector creation. Configuration should live in version control and be reproducible.

## Preferred Automation Mechanism

Use the official Splunk Observability Cloud Terraform provider:

- provider: `splunk-terraform/signalfx`

Why:

- public support for automating dashboards, dashboard groups, and detectors
- easier for a coding agent to generate and maintain than raw REST payloads
- aligns with monitor-as-code practices

Secondary mechanism:

- direct detector API or dashboard API only where Terraform support is insufficient

## What To Automate

### Dashboards

Automate:

- custom dashboard groups
- executive dashboard
- digital experience dashboard
- business transactions dashboard
- service health dashboard
- remediation dashboard
- Galileo agent monitoring companion view

Dashboard requirements:

- use the new dashboard experience when practical
- keep the primary incident path metric-driven with RUM, APM, and host filesystem charts
- use consistent filters for `deployment.environment=demo`

### Detectors

Automate:

- business transaction latency detector
- business transaction error rate detector
- knowledge service latency detector
- remediation validation failure detector
- remediation duration detector

Webhook target:

- orchestrator detector webhook endpoint

### Teams and permissions

Automate if needed:

- dashboard group sharing
- detector ownership tags
- team links where supported

## What Is Likely Not Fully Automatable

Based on current public docs, treat these as probable exceptions unless validated directly in your tenant:

- business transaction rules
- endpoint and operation grouping rules

Reason:

- public docs clearly show UI-driven setup paths
- I did not find a clear public API or Terraform resource for these objects in the official docs reviewed

Plan for now:

- document these as pre-flight setup tasks
- keep the definitions simple and stable
- revisit automation only if tenant-specific API validation proves support

## File Structure

```text
infra/terraform/
  providers.tf
  variables.tf
  outputs.tf
  dashboards/
  detectors/
  dashboard-groups/
```

## Naming Convention

Use stable names with session context:

- dashboard group: `IBOBS 2002 Demo`
- dashboard: `IBOBS Executive Story`
- dashboard: `IBOBS Digital Experience`
- dashboard: `IBOBS Business Transactions`
- detector: `IBOBS AI Claim Status Latency`

## Inputs

Required variables:

- `splunk_access_token`
- `splunk_realm`
- `deployment_environment`
- `orchestrator_webhook_url`

Optional variables:

- `dashboard_group_name`
- `session_prefix`

## Delivery Rule

If a Splunk object can be provisioned through Terraform or a public API, the coding agent should implement it as code.

If a Splunk object cannot be provisioned through a supported public interface, the coding agent should:

1. document the manual pre-flight step clearly
2. minimize the number of such steps
3. keep the object definition aligned with the telemetry model in code
