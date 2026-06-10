# CLUS-LTROBS-2001 Infrastructure

This directory contains instructor-owned infrastructure for the Cisco Live lab.
Students do not run Terraform and do not need AWS, NVIDIA, Splunk admin, or
cluster-admin access.

Current target:

- AWS EKS
- GPU worker node group using `g5.4xlarge` by default
- NVIDIA GPU Operator and DCGM metrics
- shared NVIDIA NIM endpoint
- instructor Splunk OpenTelemetry Collector for Kubernetes and platform metrics
- one namespace-scoped student collector and `shopmate-ai` app per student

## Terraform

The Terraform entry point is [`terraform/`](terraform/).

Recommended flow:

```bash
cd infra/terraform
terraform init -backend-config=backend/dev.hcl
terraform plan -var-file=env/dev.tfvars
terraform apply -var-file=env/dev.tfvars
```

The backend and variable files are intentionally examples only. Copy them to
lab-specific files outside source control before applying.

## Validation

After Terraform finishes, configure kubectl:

```bash
aws eks update-kubeconfig \
  --region <aws-region> \
  --name <cluster-name>
```

Then validate the platform:

```bash
kubectl get nodes
kubectl get pods -n gpu-operator
kubectl get svc -A | rg -i dcgm
kubectl get pods -A | rg -i nim
```

NIM deployment details still need to be locked against the selected NVIDIA NIM
chart or manifest. Until that is finalized, Terraform creates the EKS baseline,
GPU node group, optional GPU Operator release, ECR repositories, platform
namespaces, and student namespace RBAC.

## Build And Publish ShopMate

Students do not build application images. Before a lab delivery, the instructor or build team must publish the `shopmate-ai` image to a registry that the EKS cluster can pull from.

From a fresh workstation:

```bash
git clone <repo-url> ai-pods
cd ai-pods
```

After Terraform has created the ECR repositories:

```bash
export AWS_REGION="$(terraform -chdir=infra/terraform output -raw aws_region)"
export SHOPMATE_REPO="$(terraform -chdir=infra/terraform output -json ecr_repository_urls | jq -r '.["shopmate-ai"]')"
export SHOPMATE_IMAGE="${SHOPMATE_REPO}:lab-stable"
export ECR_REGISTRY="$(printf "%s\n" "$SHOPMATE_REPO" | cut -d/ -f1)"

aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR_REGISTRY"

docker build --platform linux/amd64 -t "$SHOPMATE_IMAGE" shopmate-sports
docker push "$SHOPMATE_IMAGE"
```

If the published image URI differs from the checked-in lab value, update the `image:` field in both:

- `infra/k8s/shopmate-ai.yaml`
- `workshop/lab-files/shopmate-ai.yaml`
