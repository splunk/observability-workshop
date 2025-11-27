---
title: Prerequisites
weight: 2
---

## Required Tools

Before starting this workshop, ensure you have the following tools installed:

### AWS CLI
```bash
# Check installation
aws --version

# Should output: aws-cli/2.x.x or higher
```

### kubectl
```bash
# Check installation
kubectl version --client

# Should output: Client Version: v1.28.0 or higher
```

### eksctl
```bash
# Check installation
eksctl version

# Should output: 0.150.0 or higher
```

### Helm
```bash
# Check installation
helm version

# Should output: version.BuildInfo{Version:"v3.x.x"}
```

## AWS Requirements

- AWS account with permissions to create:
  - EKS clusters
  - VPCs and subnets
  - EC2 instances
  - IAM roles and policies
  - Elastic Network Interfaces
- AWS CLI configured with credentials (`aws configure`)

## Splunk Observability Cloud

You'll need:

- A Splunk Observability Cloud account
- An **Access Token** with ingest permissions
- Your **Realm** identifier (e.g., us1, us2, eu0)

{{% notice title="Getting Splunk Credentials" style="tip" %}}
In Splunk Observability Cloud:
1. Navigate to **Settings** → **Access Tokens**
2. Create a new token with **Ingest** permissions
3. Note your realm from the URL: `https://app.<realm>.signalfx.com`
{{% /notice %}}

## Cost Considerations

### AWS Costs (Approximate)
- **EKS Control Plane**: ~$73/month
- **EC2 Nodes (2x m5.xlarge)**: ~$280/month
- **Data Transfer**: Variable
- **EBS Volumes**: ~$20/month

**Estimated Total**: ~$380-400/month for lab environment

### Splunk Costs
- Based on metrics volume (DPM - Data Points per Minute)
- Free trial available for testing

{{% notice title="Warning" style="warning" %}}
Remember to clean up resources after completing the workshop to avoid ongoing charges.
{{% /notice %}}

## Time Estimate

- **EKS Cluster Creation**: 15-20 minutes
- **Cilium Installation**: 10-15 minutes
- **Integration Setup**: 10 minutes
- **Total**: Approximately 90 minutes
