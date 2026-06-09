# Splunk Observability Cloud to Splunk On-Call Terraform Example

This directory contains an optional Terraform example for the Observability Cloud and Splunk On-Call incident response workshop.

The Terraform creates a Splunk Observability Cloud detector and configures the detector rule to notify Splunk On-Call through a routing key. Use the UI-based workshop first if attendees are learning the workflow. Use this example when you want to show how detector configuration can be managed as code.

## Variables

Create a local `terraform.tfvars` file with values like the following. Do not commit real tokens or routing keys.

```hcl
access_token = "YOUR_OBSERVABILITY_CLOUD_ACCESS_TOKEN"
realm        = "us1"
sfx_prefix   = "checkout-workshop"
sfx_vo_id    = "YOUR_SPLUNK_ON_CALL_INTEGRATION_ID"
routing_key  = "checkout-initials"
```

Variable details:

| Variable | Meaning |
| --- | --- |
| `access_token` | Splunk Observability Cloud access token used by Terraform. |
| `realm` | Observability Cloud realm such as `us0`, `us1`, or `eu0`. |
| `sfx_prefix` | Prefix used in the detector name and the sample `aws_tag_Name` filter. |
| `sfx_vo_id` | Splunk Observability Cloud notification integration credential ID for Splunk On-Call. |
| `routing_key` | Splunk On-Call routing key assigned to the target escalation policy. |

The detector uses `sfx_prefix` to filter `cpu.utilization` by `aws_tag_Name`. Adjust the metric or filter in `main.tf` if your workshop environment uses different telemetry.

## Before Running Terraform

Complete the UI integration setup first:

1. In Splunk On-Call, create the team, escalation policy, and routing key.
2. Enable **Integrations > 3rd Party Integrations > Splunk Observability Cloud System Monitoring**.
3. Copy the Service API Endpoint with the `$routing_key` placeholder intact.
4. In Splunk Observability Cloud, create the Splunk On-Call notification integration using that endpoint as the Post URL.
5. Confirm the integration validates successfully.
6. Locate the Observability Cloud integration credential ID and use it as `sfx_vo_id`.

The detector notification string in `main.tf` follows this format:

```text
VictorOps,<observability-cloud-integration-id>,<splunk-on-call-routing-key>
```

## Run

```bash
terraform init
terraform plan
terraform apply
```

## Notes

The notification target in `main.tf` uses the provider notification string `VictorOps,<integration id>,<routing key>`. Splunk On-Call was formerly VictorOps, and this identifier is still used by the Terraform provider notification target.

For the participant-facing lab, see:

```text
content/en/ninja-workshops/operations/16-o11y-on-call-incident-response/
```
