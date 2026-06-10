# Instructor-Only Terraform Destroy And Rebuild Plan

## Summary

This document defines the lifecycle plan for destroying, rebuilding, and resetting the full `CLUS-LTROBS-2001` lab environment.

This is an instructor-only operational plan. Students do not perform cleanup, reset, teardown, rebuild, or local laptop cleanup as part of the workshop.

Terraform is the only supported infrastructure lifecycle tool for the AWS lab stack.

## Core Decisions

- Terraform is the only supported tool for infrastructure create, update, destroy, and rebuild.
- Cleanup, reset, teardown, and rebuild are instructor-only responsibilities.
- Cleanup documentation must remain internal and must not be added to the MkDocs student guide.
- Students do not run cleanup commands.
- Students do not reset shared or namespace resources.
- Students do not need AWS, Kubernetes admin, Splunk admin, or Terraform permissions.
- Destroy validation must prove that no tagged billable AWS or GPU resources remain.
- Splunk cleanup is instructor-owned.
- Historical Splunk telemetry may remain visible until the configured retention period expires.
- Any future GPU rollout exercise must be included in teardown and destroy validation.

## Terraform Requirements

Terraform must manage the full AWS lab stack unless a resource is explicitly documented as an external dependency.

Required Terraform state model:

- remote backend
- S3 state bucket
- DynamoDB state locking
- environment-specific state paths, for example `dev`, `dry-run`, and `event`
- restricted access for instructor or lab operations team only

Current implementation path:

- Terraform code lives in `infra/terraform/`.
- Backend examples live in `infra/terraform/backend/`.
- Environment variable examples live in `infra/terraform/env/`.

Every Terraform-managed AWS resource must use common tags:

```text
Project=clus-ltrobs-2001
Environment=<dev|dry-run|event>
Owner=<team-or-person>
ExpiresAt=<date-time>
ManagedBy=terraform
```

Terraform-managed scope should include:

- VPC and networking, if lab-created
- EKS cluster
- GPU node groups
- EC2 launch templates
- IAM roles and policies
- security groups
- load balancers and target groups, if created by Terraform or Kubernetes automation
- EBS volumes and snapshots created for the lab
- ECR repositories, if lab-created
- Kubernetes add-ons if managed through Terraform

Anything not managed by Terraform must be listed in future `infra/teardown.md` as an external dependency or manual cleanup item.

## Full Destroy Scope

Full environment destroy must remove or validate removal of:

- EKS cluster
- GPU node groups
- EC2 GPU instances
- EC2 launch templates
- EBS volumes created by the lab
- EBS snapshots created by the lab
- load balancers
- target groups
- security groups
- NAT gateways, if lab-created
- Elastic IPs, if lab-created
- IAM roles and policies created by the lab
- ECR repositories, only if lab-created and approved for deletion
- Kubernetes add-ons managed by the lab
- NVIDIA GPU Operator
- NVIDIA NIM deployment
- instructor OpenTelemetry Collector
- student namespaces
- `shopmate-ai` deployments
- student collectors
- load generator jobs
- Kubernetes PVCs, configmaps, secrets, and services owned by the lab

Cluster deletion may remove most Kubernetes resources automatically, but destroy validation must still confirm that AWS resources created indirectly by Kubernetes are gone.

## Instructor Reset Workflow

Instructor reset workflows are for recovering the lab without destroying AWS infrastructure.

Supported reset modes:

```text
soft
clean
baseline
```

`soft` mode:

- restarts lab workloads and collectors
- preserves namespaces, secrets, RBAC, PVCs, and Helm releases
- intended for transient app or collector issues

`clean` mode:

- removes and recreates lab-owned namespace workloads
- removes apps, collectors, jobs, configmaps, and PVCs
- preserves shared platform components
- preserves instructor-owned secrets unless explicitly requested

`baseline` mode:

- rebuilds the complete Kubernetes lab baseline
- recreates namespaces, RBAC, secrets, app templates, student collectors, instructor collector, NIM, and GPU monitoring
- intended for dry runs or pre-event reset

Reset automation must:

- require explicit `LAB_ENVIRONMENT`
- require explicit confirmation for destructive operations
- refuse to operate on clusters missing the expected lab name or lab tags
- operate only on lab-owned namespaces and releases
- produce a before and after resource inventory
- remain instructor-only

## Splunk Cleanup

Instructor cleanup must:

- rotate or delete lab-scoped ingest tokens after teardown
- remove, disable, or archive lab-created dashboards if automation creates them
- remove, disable, or archive lab-created detectors if automation creates them
- preserve Splunk objects not tagged or named for this lab
- document that historical metrics, traces, and logs remain visible until retention expires

Splunk telemetry retention is not treated as part of normal lab reset.

## Destroy Workflow

Pre-destroy steps:

1. Confirm no active class, dry run, or validation session is using the environment.
2. Capture current Terraform state and AWS resource inventory.
3. Capture Kubernetes resource inventory if the cluster is reachable.
4. Scale GPU node groups down if supported and safe.
5. Rotate or disable lab ingest tokens.
6. Export final cost notes if needed.

Terraform destroy steps:

```bash
terraform init
terraform plan -destroy
terraform destroy
```

Post-destroy validation must confirm:

- no running EC2 instances with lab tags
- no stopped EC2 instances with lab tags unless intentionally retained
- no EBS volumes with lab tags
- no EBS snapshots with lab tags unless intentionally retained
- no EKS cluster with the lab name
- no load balancers with lab tags
- no target groups with lab tags
- no NAT gateways with lab tags
- no Elastic IPs with lab tags
- no unexpected GPU spend after the teardown window

## Rebuild Workflow

Rebuild steps:

1. Confirm Terraform backend access.
2. Confirm AWS account and region.
3. Confirm GPU quota for the selected instance type.
4. Confirm Splunk realm and lab ingest token strategy.
5. Confirm NVIDIA NGC/NIM credentials and model entitlement.
6. Run Terraform:

```bash
terraform init
terraform plan -var-file=env/dev.tfvars
terraform apply -var-file=env/dev.tfvars
```

7. Validate EKS cluster access.
8. Validate GPU nodes are ready.
9. Validate NVIDIA GPU Operator.
10. Validate DCGM exporter.
11. Validate NIM endpoint and `/v1/metrics`.
12. Validate instructor OpenTelemetry Collector.
13. Validate student namespace baseline.
14. Run one end-to-end test namespace.

## Validation Requirements

Full lifecycle validation must be completed before the event:

1. Build the environment from Terraform.
2. Validate GPU, NIM, instructor collector, and one test namespace.
3. Generate app, trace, token, GPU, and NIM telemetry.
4. Run instructor-only clean reset.
5. Rebuild Kubernetes baseline.
6. Confirm telemetry works again.
7. Run `terraform plan -destroy`.
8. Run `terraform destroy`.
9. Confirm no tagged billable resources remain.
10. Rebuild with `terraform apply`.
11. Validate again.

Cost guardrail validation must confirm:

- GPU instances can be discovered by tag.
- GPU node groups can be scaled down or destroyed.
- AWS Budgets or equivalent cost alarms are configured for unexpected spend.
- The teardown checklist includes GPU rollout resources if that exercise is implemented.

## Future Files To Create

When implementation starts, create:

```text
infra/teardown.md
infra/rebuild.md
infra/scripts/destroy-lab.sh
infra/scripts/validate-destroy.sh
infra/scripts/reset-lab-namespaces.sh
infra/scripts/rebuild-lab-baseline.sh
```

These files are instructor-only and must not be linked from the student MkDocs navigation.
