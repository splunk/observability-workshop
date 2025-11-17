---
title: GitHub Setup
weight: 2
time: 10 minutes
---

## Prerequisites

Before you begin, ensure you have:

- GitHub account with repository access
- AWS VPC with Ubuntu EC2 instances
- SSH key pair (PEM file) for authentication to target hosts
- AppDynamics Smart Agent package
- Target Ubuntu EC2 instances with SSH access

## Fork or Clone the Repository

First, get access to the GitHub Actions lab repository:

**Repository URL**: [https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)

```bash
# Option 1: Fork the repository via GitHub UI
# Go to https://github.com/chambear2809/github-actions-lab
# Click "Fork" button

# Option 2: Clone directly (for testing)
git clone https://github.com/chambear2809/github-actions-lab.git
cd github-actions-lab
```

## Configure Self-hosted Runner

Your self-hosted runner must be deployed in the same AWS VPC as your target EC2 instances.

### Install Runner on EC2 Instance

1. **Launch EC2 instance** in your VPC (Ubuntu or Amazon Linux 2)

2. **Navigate to runner settings** in your forked repository:
   ```
   Settings → Actions → Runners → New self-hosted runner
   ```

3. **SSH into the runner instance** and execute installation commands:

```bash
# Create runner directory
mkdir actions-runner && cd actions-runner

# Download runner (check GitHub for latest version)
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure (use token from GitHub UI)
./config.sh --url https://github.com/YOUR_USERNAME/github-actions-lab --token YOUR_TOKEN

# Install as service
sudo ./svc.sh install

# Start service
sudo ./svc.sh start
```

### Verify Runner Status

Check that the runner appears as **"Idle"** (green) in:
```
Settings → Actions → Runners
```

{{% notice style="tip" %}}
The runner must remain online and idle to pick up workflow jobs. If it shows offline, check the service status: `sudo ./svc.sh status`
{{% /notice %}}

## Configure GitHub Secrets

Navigate to: **Settings → Secrets and variables → Actions → Secrets**

### SSH Private Key Secret

This secret contains your SSH private key for accessing target hosts.

1. Click **"New repository secret"**
2. **Name**: `SSH_PRIVATE_KEY`
3. **Value**: Paste the contents of your PEM file

```bash
# View your PEM file
cat /path/to/your-key.pem
```

Example format:
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```

4. Click **"Add secret"**

{{% notice style="important" %}}
Never commit SSH keys to your repository! Always use GitHub Secrets for sensitive credentials.
{{% /notice %}}

## Configure GitHub Variables

Navigate to: **Settings → Secrets and variables → Actions → Variables**

### Deployment Hosts Variable (Required)

This variable contains the list of all target hosts where Smart Agent should be deployed.

1. Click **"New repository variable"**
2. **Name**: `DEPLOYMENT_HOSTS`
3. **Value**: Enter your target host IPs (one per line)

```
172.31.1.243
172.31.1.48
172.31.1.5
172.31.10.20
172.31.10.21
```

**Format Requirements:**
- One IP per line
- No commas
- No spaces
- No extra characters
- Use Unix line endings (LF, not CRLF)

4. Click **"Add variable"**

### Optional Variables

These variables are optional and used for Smart Agent service user/group configuration:

#### SMARTAGENT_USER
1. Click **"New repository variable"**
2. **Name**: `SMARTAGENT_USER`
3. **Value**: e.g., `appdynamics`
4. Click **"Add variable"**

#### SMARTAGENT_GROUP
1. Click **"New repository variable"**
2. **Name**: `SMARTAGENT_GROUP`
3. **Value**: e.g., `appdynamics`
4. Click **"Add variable"**

## Network Configuration

For the lab setup with all EC2 instances in the same VPC and security group:

### Security Group Rules

**Inbound Rules:**
- SSH (port 22) from same security group (source: same SG)

**Outbound Rules:**
- HTTPS (port 443) to 0.0.0.0/0 (for GitHub API access)
- SSH (port 22) to same security group (for target access)

### Network Best Practices

- ✅ Use private IP addresses (172.31.x.x) for `DEPLOYMENT_HOSTS`
- ✅ Runner and targets in same security group
- ✅ No public IPs needed on target hosts
- ✅ Runner communicates via private network
- ✅ Outbound HTTPS required for GitHub polling

## Verify Configuration

Before running workflows, verify your setup:

### 1. Check Runner Status

1. Go to **Settings → Actions → Runners**
2. Verify runner shows as "Idle" (green)
3. Check "Last seen" timestamp is recent

### 2. Test SSH Connectivity

SSH from your runner instance to a target host:

```bash
# On runner instance
ssh -i ~/.ssh/your-key.pem ubuntu@172.31.1.243
```

If successful, you should get a shell prompt on the target host.

### 3. Verify Secrets and Variables

1. Go to **Settings → Secrets and variables → Actions**
2. Confirm secrets tab shows: `SSH_PRIVATE_KEY`
3. Confirm variables tab shows: `DEPLOYMENT_HOSTS`

### 4. Check Repository Access

Ensure the runner can access the repository:

```bash
# On runner instance, as the runner user
cd ~/actions-runner
./run.sh  # Test run (Ctrl+C to stop)
```

You should see: "Listening for Jobs"

## Troubleshooting Common Issues

### Runner Not Picking Up Jobs

**Symptom**: Workflows stay in "queued" state

**Solution**:
- Check runner status: `sudo systemctl status actions.runner.*`
- Restart runner: `sudo ./svc.sh restart`
- Verify outbound HTTPS (443) connectivity to GitHub

### SSH Connection Failures

**Symptom**: Workflows fail with "Permission denied" or "Connection refused"

**Solution**:
```bash
# Test from runner
ssh -i ~/.ssh/test-key.pem ubuntu@172.31.1.243 -o ConnectTimeout=10

# Check security group allows SSH from runner
# Verify private key matches public key on targets
```

### Invalid Characters in Hostname

**Symptom**: Error: "hostname contains invalid characters"

**Solution**:
- Edit `DEPLOYMENT_HOSTS` variable
- Ensure no trailing spaces
- Use Unix line endings (LF, not CRLF)
- One IP per line, no extra characters

### Secrets Not Found

**Symptom**: Error: "Secret SSH_PRIVATE_KEY not found"

**Solution**:
- Verify secret name exactly matches: `SSH_PRIVATE_KEY`
- Check secret is in repository secrets (not environment secrets)
- Ensure you have repository admin access

## Security Best Practices

Follow these best practices for secure operations:

- ✅ Use GitHub Secrets for all private keys
- ✅ Rotate SSH keys regularly
- ✅ Keep runner in private VPC subnet
- ✅ Restrict runner security group to minimal access
- ✅ Update runner software regularly
- ✅ Enable branch protection rules
- ✅ Use separate keys for different environments
- ✅ Enable audit logging for repository access

## Next Steps

With GitHub configured and the runner set up, you're ready to explore the available workflows and execute your first deployment!
