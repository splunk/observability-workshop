---
title: Running Workflows
weight: 4
time: 15 minutes
---

## Triggering Workflows

All workflows are configured with `workflow_dispatch`, meaning they must be triggered manually. There are two main ways to run workflows:

1. **GitHub UI** - Visual interface, easiest for most users
2. **GitHub CLI** - Command-line interface, great for automation

## Method 1: GitHub UI

### Step 1: Navigate to Actions Tab

1. Go to your forked repository on GitHub
2. Click the **Actions** tab at the top

### Step 2: Select Workflow

On the left sidebar, you'll see all available workflows:
- Deploy Smart Agent
- Install Node Agent (Batched)
- Install Machine Agent (Batched)
- Install DB Agent (Batched)
- Install Java Agent (Batched)
- Uninstall Node Agent (Batched)
- Uninstall Machine Agent (Batched)
- Uninstall DB Agent (Batched)
- Uninstall Java Agent (Batched)
- Stop and Clean Smart Agent (Batched)
- Cleanup All Agents

Click on the workflow you want to run.

### Step 3: Run Workflow

1. Click **"Run workflow"** button (top right)
2. Select branch: **main**
3. (Optional) Adjust **batch_size** if desired
4. Click **"Run workflow"** button

### Step 4: Monitor Execution

1. The workflow will appear in the list below
2. Click on the workflow run to view details
3. Watch progress in real-time
4. Click on job names to see detailed logs

## Method 2: GitHub CLI

### Install GitHub CLI

```bash
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### Authenticate

```bash
gh auth login
```

### Run Workflows

```bash
# Deploy Smart Agent (default batch size)
gh workflow run "Deploy Smart Agent" --repo YOUR_USERNAME/github-actions-lab

# Deploy with custom batch size
gh workflow run "Deploy Smart Agent" \
  --repo YOUR_USERNAME/github-actions-lab \
  -f batch_size=128

# Install agents
gh workflow run "Install Node Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

gh workflow run "Install Machine Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

# Uninstall agents
gh workflow run "Uninstall Node Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

# Stop and clean
gh workflow run "Stop and Clean Smart Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

# Complete cleanup
gh workflow run "Cleanup All Agents" \
  --repo YOUR_USERNAME/github-actions-lab
```

### Monitor Workflows

```bash
# List recent workflow runs
gh run list --repo YOUR_USERNAME/github-actions-lab

# View specific run
gh run view RUN_ID --repo YOUR_USERNAME/github-actions-lab

# Watch run in progress
gh run watch RUN_ID --repo YOUR_USERNAME/github-actions-lab

# View failed logs
gh run view RUN_ID --log-failed --repo YOUR_USERNAME/github-actions-lab
```

## First Deployment Walkthrough

Let's walk through a complete first-time deployment:

### Step 1: Verify Setup

Before running any workflows, ensure:
- ✅ Self-hosted runner shows "Idle" (green)
- ✅ `SSH_PRIVATE_KEY` secret is configured
- ✅ `DEPLOYMENT_HOSTS` variable contains your target IPs
- ✅ Network connectivity verified

### Step 2: Deploy Smart Agent

**Via GitHub UI:**
1. Go to **Actions** tab
2. Select **"Deploy Smart Agent"**
3. Click **"Run workflow"**
4. Accept default batch_size (256)
5. Click **"Run workflow"**

**Via GitHub CLI:**
```bash
gh workflow run "Deploy Smart Agent" --repo YOUR_USERNAME/github-actions-lab
```

### Step 3: Monitor Execution

The workflow will show:
1. **Prepare** job - Creating batch matrix
2. **Deploy** job (one per batch) - Deploying to hosts

Click on each job to view detailed logs.

### Step 4: Verify Installation

SSH into a target host and check:

```bash
# SSH to target
ssh ubuntu@172.31.1.243

# Check Smart Agent status
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl status
```

**Expected output:**
```
Smart Agent is running (PID: 12345)
Service: appdsmartagent.service
Status: active (running)
```

### Step 5: Install Additional Agents (Optional)

If needed, install specific agent types:

```bash
# Install Machine Agent
gh workflow run "Install Machine Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab

# Install DB Agent
gh workflow run "Install DB Agent (Batched for Large Scale)" \
  --repo YOUR_USERNAME/github-actions-lab
```

## Understanding Workflow Output

### Prepare Job Output

```
Loading deployment hosts...
Total hosts: 1000
Batch size: 256
Creating 4 batches...
Batch 1: Hosts 1-256
Batch 2: Hosts 257-512
Batch 3: Hosts 513-768
Batch 4: Hosts 769-1000
```

### Deploy Job Output (per batch)

```
Processing batch 1 of 4
Deploying to 256 hosts in parallel...
Host 172.31.1.1: SUCCESS
Host 172.31.1.2: SUCCESS
Host 172.31.1.3: SUCCESS
...
Batch 1 complete: 256/256 succeeded
```

### Completion Summary

```
Deployment Summary:
Total hosts: 1000
Successful: 998
Failed: 2
Failed hosts:
  - 172.31.1.48
  - 172.31.1.125
```

## Common Deployment Scenarios

### Scenario 1: Initial Deployment

```bash
# 1. Deploy Smart Agent
gh workflow run "Deploy Smart Agent"

# 2. Verify deployment
# SSH to a host and check status

# 3. Install agents as needed
gh workflow run "Install Machine Agent (Batched for Large Scale)"
gh workflow run "Install DB Agent (Batched for Large Scale)"
```

### Scenario 2: Update Smart Agent

```bash
# 1. Stop and clean current installation
gh workflow run "Stop and Clean Smart Agent (Batched for Large Scale)"

# 2. Update Smart Agent ZIP in repository
# (Push new version to repository)

# 3. Deploy new version
gh workflow run "Deploy Smart Agent"

# 4. Reinstall agents
gh workflow run "Install Machine Agent (Batched for Large Scale)"
```

### Scenario 3: Add New Hosts

```bash
# 1. Update DEPLOYMENT_HOSTS variable in GitHub
# Add new IPs

# 2. Deploy to all hosts (will skip existing ones with idempotent logic)
gh workflow run "Deploy Smart Agent"
```

### Scenario 4: Complete Removal

```bash
# 1. Stop and clean
gh workflow run "Stop and Clean Smart Agent (Batched for Large Scale)"

# 2. Complete removal
gh workflow run "Cleanup All Agents"
```

{{% notice style="danger" %}}
"Cleanup All Agents" permanently deletes `/opt/appdynamics`. This cannot be undone!
{{% /notice %}}

## Troubleshooting Workflow Failures

### Workflow Stays in "Queued"

**Symptom**: Workflow doesn't start

**Cause**: Runner not available or offline

**Solution**:
1. Check runner status: Settings → Actions → Runners
2. Verify runner shows "Idle" (green)
3. Restart runner if needed: `sudo ./svc.sh restart`

### SSH Connection Failures

**Symptom**: "Permission denied" or "Connection refused" errors

**Solutions**:

**Test SSH manually:**
```bash
# From runner instance
ssh -i ~/.ssh/test-key.pem ubuntu@172.31.1.243
```

**Check security groups:**
- Verify SSH (22) allowed from runner
- Confirm runner and targets in same security group

**Verify SSH key:**
- Ensure `SSH_PRIVATE_KEY` secret matches actual key
- Verify public key is on target hosts

### Partial Batch Failures

**Symptom**: Some hosts succeed, others fail

**Solution**:
1. View workflow logs to identify failed hosts
2. SSH to failed hosts to investigate
3. Re-run workflow (idempotent - skips successful hosts)

### Batch Job Errors

**Symptom**: "Error splitting hosts into batches"

**Solution**:
- Check `DEPLOYMENT_HOSTS` variable format
- Ensure one IP per line
- No trailing spaces or special characters
- Use Unix line endings (LF, not CRLF)

## Performance Tuning

### Adjusting Batch Size

**Smaller batches** (fewer resources, slower):
```bash
gh workflow run "Deploy Smart Agent" -f batch_size=128
```

**Larger batches** (more resources, faster):
```bash
gh workflow run "Deploy Smart Agent" -f batch_size=256
```

### Runner Resource Recommendations

| Hosts | CPU | Memory | Batch Size |
|-------|-----|--------|------------|
| 1-100 | 2 cores | 4 GB | 256 |
| 100-500 | 4 cores | 8 GB | 256 |
| 500-2000 | 8 cores | 16 GB | 256 |
| 2000+ | 16 cores | 32 GB | 256 |

## Best Practices

1. **Test on single host first**
   - Create a test variable with 1 IP
   - Run workflow to verify
   - Then deploy to full list

2. **Monitor workflow execution**
   - Watch logs in real-time
   - Check for errors immediately
   - Verify on sample hosts

3. **Use appropriate batch sizes**
   - Default (256) works for most cases
   - Reduce if runner struggles
   - Monitor runner resource usage

4. **Keep workflows up to date**
   - Pull latest changes from repository
   - Test updates on non-production first
   - Document any customizations

5. **Maintain runner health**
   - Keep runner online and idle
   - Update runner software regularly
   - Monitor disk space and resources

## Next Steps

Congratulations! You've successfully learned how to automate AppDynamics Smart Agent deployment using GitHub Actions. For more information, visit the [complete repository](https://github.com/chambear2809/github-actions-lab).
