# Accounts And Access Plan

## Purpose

This document defines all accounts, credentials, and access needed to run the `CLUS-LTROBS-2001` demo and workshop.

Goals:

- avoid account setup during the 4-hour lab
- make instructor-owned accounts explicit
- make student requirements simple
- prevent students from needing AWS, NVIDIA, or cluster-admin privileges
- support students running the lab from their own laptops

## Account Summary

| Area | Owner | Students Need Account? | Purpose |
|---|---|---:|---|
| AWS | Instructor | No | EKS cluster, GPU nodes, networking, storage, ingress |
| Splunk Observability Cloud | Instructor provides access | Prefer yes | View traces, metrics, dashboards, AI Agent Monitoring |
| Splunk ingest token | Instructor | No personal token | Student collectors export telemetry |
| NVIDIA NGC / NIM | Instructor | No | Pull/run NIM and access selected model |
| Kubernetes/EKS | Instructor creates access | No cloud account required | Namespace-scoped student access |
| Container registry | Instructor/build team | No | Host `shopmate-ai` and load generator images |
| GitHub/source repo | Instructor/build team | Optional | Pull lab files if students edit locally |

## Instructor-Owned Accounts

### AWS Account

Required for:

- EKS cluster
- `g5.4xlarge` GPU worker nodes
- VPC, subnets, route tables, security groups
- EBS volumes
- load balancers or ingress
- Amazon ECR if used as the container registry

Instructor needs:

- AWS account with approved `g5.4xlarge` quota in the selected region
- permissions to create EKS clusters and node groups
- permissions to create IAM roles and policies
- permissions to create or use VPC networking
- permissions to create ECR repositories if used
- permissions to delete or scale down all lab resources after the workshop

Pre-lab checks:

1. Confirm `g5.4xlarge` quota.
2. Confirm EKS service quota.
3. Confirm worker nodes have outbound internet access.
4. Confirm the account can create IAM roles for EKS.
5. Confirm teardown permissions.

### Splunk Observability Cloud Account

Required for:

- metric ingest
- trace ingest
- AI Agent Monitoring
- dashboards
- tokenomics and chargeback analysis

Instructor needs:

- Splunk Observability Cloud org
- realm, for example `us0`, `us1`, or `eu0`
- lab-scoped ingest token
- instructor user account
- student user accounts or approved shared lab login
- permissions to create/import dashboards

Preferred student access:

- one Splunk user per student

Fallback:

- shared read-only lab login, if event and security policy allow it

Values provided to students:

```text
SPLUNK_OBSERVABILITY_URL=<org-url>
SPLUNK_REALM=<realm>
SPLUNK_ACCESS_TOKEN=<lab-ingest-token-or-preloaded-secret>
```

Security rule:

- use a lab-scoped ingest token
- rotate or delete the token after the lab
- prefer preloading the token into Kubernetes Secrets instead of asking students to paste it into files

### NVIDIA NGC / NIM Access

Required for:

- pulling NIM images
- accepting model terms
- running the selected model endpoint

Instructor needs:

- NVIDIA account with access to required NIM assets
- NGC API key or image pull secret
- accepted terms for the selected model
- access to `meta/llama-3.2-1b-instruct` or approved replacement model

Students do not need NVIDIA accounts.

Instructor provides:

```text
NIM_BASE_URL=<internal-nim-service-url>
NIM_API_KEY=<stored-in-k8s-secret-or-placeholder>
NIM_MODEL=meta/llama-3.2-1b-instruct
```

### Container Registry

Required for:

- `shopmate-ai` image
- optional load generator image

Options:

- Amazon ECR
- GitHub Container Registry
- Docker Hub
- private lab registry

Instructor/build team needs:

- push permissions
- image pull access from EKS
- image pull secret if registry is private

Recommended tags:

```text
shopmate-ai:lab-stable
shopmate-ai:dev
loadgen:lab-stable
```

Students do not need registry accounts if the cluster can pull images.

## Student Requirements

Students should not need:

- AWS account
- NVIDIA account
- EKS admin access
- cluster-admin permissions
- container registry account

Students need:

- laptop
- browser
- internet access
- terminal
- `kubectl`
- `helm`
- optional `curl`
- optional Python if running local load generator
- Splunk Observability login or shared lab login
- assigned namespace
- assigned student ID
- assigned department/cost center
- kubeconfig or namespace access instructions

Student handout values:

```text
student.id=student-01
team.name=team-a
department.name=marketing
department.cost_center=cc-4100
namespace=student-01
deployment.environment=student-01
k8s.cluster.name=clus-ltrobs-2001-student-01
chargeback.account=cb-student-01
Splunk URL=<url>
Splunk realm=<realm>
Splunk token=<token or preloaded secret>
App URL=<url or port-forward command>
```

## Kubernetes Access For Students

Recommended model:

- one namespace per student
- one Kubernetes identity or service account per student
- namespace-scoped RBAC
- no cluster-admin
- no AWS console access

Students should be able to:

- get/list/watch pods in their namespace
- create/update/delete deployments in their namespace
- create/update/delete configmaps in their namespace
- create/update/delete services in their namespace
- create/update/delete secrets in their namespace if secrets are not preloaded
- install a Helm release in their namespace
- read logs for pods in their namespace

Students should not be able to:

- modify node groups
- modify cluster roles
- modify other namespaces
- create DaemonSets
- modify the instructor collector
- modify NIM
- modify GPU Operator

## Student Roster

Create a roster before the lab.

Required columns:

```csv
student_number,student_id,namespace,team,department,cost_center,chargeback_account,k8s_cluster_name,deployment_environment,splunk_user,app_url
1,student-01,student-01,team-a,marketing,cc-4100,cb-student-01,clus-ltrobs-2001-student-01,student-01,student01@example.com,https://student-01.example.com
```

Department assignment example:

| Students | Department | Cost Center |
|---|---|---|
| 01-04 | marketing | `cc-4100` |
| 05-08 | customer_support | `cc-4200` |
| 09-12 | merchandising | `cc-4300` |
| 13-16 | finance | `cc-4400` |
| 17-20 | operations | `cc-4500` |

## Secrets To Create

Instructor namespace:

```text
splunk-instructor-token
ngc-api-key
nim-api-key
registry-pull-secret
```

Each student namespace:

```text
splunk-access-token
nim-api-key
registry-pull-secret
```

If possible, preload `splunk-access-token` into each namespace so students do not copy the ingest token into files.

## Pre-Lab Account Setup Checklist

Instructor must complete:

1. AWS account ready.
2. GPU quota approved.
3. Splunk Observability org ready.
4. Splunk ingest token created.
5. Splunk student users or shared lab login ready.
6. NVIDIA/NGC access verified.
7. NIM model access accepted and tested.
8. Container registry ready.
9. `shopmate-ai` image pushed.
10. Student roster generated.
11. Student namespaces created.
12. Student kubeconfigs or access instructions generated.
13. Secrets created in namespaces.
14. Instructor validation script passes.
15. One test student flow passes end to end.

## Student Pre-Lab Checklist

Send students:

1. Install `kubectl`.
2. Install `helm`.
3. Confirm browser access to Splunk Observability.
4. Confirm they can connect to Kubernetes.
5. Confirm they know their namespace and student ID.

Students should test:

```text
kubectl get pods -n <student-namespace>
helm version
```

## Local Minikube Testing On macOS

For developers and instructors, the project should be testable locally on macOS with Minikube.

Local Minikube testing does not require:

- AWS account
- NVIDIA account
- real GPU
- real NIM
- container registry account if images are built into Minikube

Local Minikube testing still needs:

- Splunk Observability org, realm, and ingest token if validating export to Splunk
- `kubectl`
- `helm`
- Docker Desktop or compatible runtime
- `minikube`

Use:

- fake NIM service for chat and `/v1/metrics`
- fake DCGM exporter for `/metrics`
- fake NIM mode in `shopmate-ai`

See [`docs/MINIKUBE_MACOS_TEST_PLAN.md`](/Users/mkuglerr/code2/codex_projects/ai-pods/docs/MINIKUBE_MACOS_TEST_PLAN.md).

## Day-Of Distribution

Provide each student:

- roster row
- kubeconfig or cluster access instructions
- Splunk URL
- Splunk username/password or SSO instructions
- Splunk realm
- app URL or port-forward instructions
- department persona
- chargeback account

Avoid distributing:

- AWS console credentials
- NGC credentials
- cluster-admin kubeconfig
- production Splunk tokens

## Post-Lab Cleanup

After the lab:

1. Rotate or delete lab Splunk ingest token.
2. Disable or delete temporary student Splunk users.
3. Delete student kubeconfigs or service account tokens.
4. Delete student namespaces.
5. Delete NIM secrets.
6. Scale GPU node group to zero or delete EKS cluster.
7. Confirm no `g5.4xlarge` instances remain running.
8. Delete temporary registry credentials if used.

## Decision Summary

Students create no external accounts.

The instructor creates and provides:

- AWS/EKS environment
- Splunk access
- Splunk realm and ingest token
- NVIDIA/NIM access
- Kubernetes namespace access
- app endpoint
- student identity and department assignment

This keeps the workshop focused on instrumentation and analysis, not account provisioning.
