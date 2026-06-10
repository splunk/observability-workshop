# Terraform EKS Baseline

This Terraform stack creates the AWS foundation for the `CLUS-LTROBS-2001`
instructor-owned lab environment.

It manages:

- VPC, public subnets, private subnets, internet gateway, and optional NAT gateway
- EKS cluster
- managed GPU node group
- core EKS add-ons
- optional EBS CSI driver add-on with IRSA
- optional NVIDIA GPU Operator Helm release
- ECR repositories for lab images
- platform namespaces
- per-student namespaces, service accounts, roles, and role bindings

It does not currently manage Splunk ingest tokens or NVIDIA NGC credentials.
Keep those out of Terraform state unless the event security model explicitly
approves storing them there.

## Bootstrap Remote State

Create the S3 state bucket and DynamoDB lock table once per AWS account/region,
then copy the example backend file:

```bash
cp backend/dev.hcl.example backend/dev.hcl
```

Edit `backend/dev.hcl`, then initialize:

```bash
terraform init -backend-config=backend/dev.hcl
```

For local validation without remote state:

```bash
terraform init -backend=false
```

## Configure Variables

Copy the example variables file:

```bash
cp env/dev.tfvars.example env/dev.tfvars
```

Edit at least:

- `aws_region`
- `owner`
- `expires_at`
- `student_count`
- `gpu_desired_size`
- `gpu_max_size`

## Deploy

```bash
terraform plan -var-file=env/dev.tfvars
terraform apply -var-file=env/dev.tfvars
```

Configure kubectl from the Terraform output:

```bash
aws eks update-kubeconfig \
  --region <aws-region> \
  --name <cluster-name>
```

## Destroy

Destroy is instructor-only:

```bash
terraform plan -destroy -var-file=env/dev.tfvars
terraform destroy -var-file=env/dev.tfvars
```

After destroy, validate that no tagged GPU instances, EBS volumes, load
balancers, target groups, NAT gateways, Elastic IPs, or EKS clusters remain.
