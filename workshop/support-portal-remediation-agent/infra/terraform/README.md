# Terraform Provisioning

This directory provisions Splunk Observability dashboards, a dashboard group, and detectors for the Cisco Live app.

The preferred authoring path for dashboard and detector iteration is [infra/splunk](/Users/mkuglerr/code2/codex_projects/ciscolive26/infra/splunk/README.md). Terraform remains available for managed deployment.

## What it creates

- dashboard group: `IBOBS 2002 Demo`
- dashboards:
  - executive story
  - APM service requests
  - digital experience
  - service health
  - remediation operations
- detectors:
  - claims knowledge cache filesystem pressure
  - claims knowledge APM latency
  - claims knowledge APM error rate

## Signal source

The current Terraform config uses out-of-the-box Splunk Observability signals:

- `disk.utilization`
- `service.request`
- `service.request.duration.ns`

It does not rely on custom app-emitted RED metrics or log-derived signals.

## Required variables

- `splunk_access_token`
- `orchestrator_webhook_url`

Recommended:

- `instance`
- `deployment_environment`
- `cache_mountpoint`

Optional:

- `splunk_realm`
- `public_orchestrator_webhook_url`
- `enable_webhook_integration`
- `existing_webhook_credential_id`
- threshold variables from [variables.tf](/Users/mkuglerr/code2/codex_projects/ciscolive26/infra/terraform/variables.tf)

## Example usage

```bash
terraform -chdir=infra/terraform init
terraform -chdir=infra/terraform plan \
  -var="splunk_access_token=$SPLUNK_ACCESS_TOKEN" \
  -var="deployment_environment=${DEPLOYMENT_ENVIRONMENT:-demo}" \
  -var="instance=${INSTANCE:-student-001}" \
  -var="cache_mountpoint=${SPLUNK_CACHE_MOUNTPOINT:-/var/cache/claims-knowledge}" \
  -var="cache_utilization_metric=${SPLUNK_CACHE_UTILIZATION_METRIC:-claims_knowledge.cache.utilization}" \
  -var="claim_status_latency_metric=${SPLUNK_CLAIM_STATUS_LATENCY_METRIC:-claims_knowledge.claim_status.latency_ms}" \
  -var="orchestrator_webhook_url=https://demo.example/webhooks/splunk/detector"
terraform -chdir=infra/terraform apply \
  -var="splunk_access_token=$SPLUNK_ACCESS_TOKEN" \
  -var="deployment_environment=${DEPLOYMENT_ENVIRONMENT:-demo}" \
  -var="instance=${INSTANCE:-student-001}" \
  -var="cache_mountpoint=${SPLUNK_CACHE_MOUNTPOINT:-/var/cache/claims-knowledge}" \
  -var="cache_utilization_metric=${SPLUNK_CACHE_UTILIZATION_METRIC:-claims_knowledge.cache.utilization}" \
  -var="claim_status_latency_metric=${SPLUNK_CLAIM_STATUS_LATENCY_METRIC:-claims_knowledge.claim_status.latency_ms}" \
  -var="orchestrator_webhook_url=https://demo.example/webhooks/splunk/detector"
```

For detector-only updates:

```bash
npm run terraform:webhook-plan
npm run terraform:webhook-apply
```

## Notes

- The webhook URL must be externally reachable for real Splunk webhook notifications.
- A local URL like `http://127.0.0.1:18110/...` is acceptable for planning and runbook links, but Splunk Cloud cannot call back into localhost.
- Use a tunnel or public endpoint before wiring detector notifications directly to the orchestrator.
- Run `terraform -chdir=infra/terraform validate` before planning or applying.
