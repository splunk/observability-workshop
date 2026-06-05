---
title: Deployment Workflow
weight: 4
time: 15 minutes
---

## First Deployment

Now that your pipelines are configured, let's walk through executing your first Smart Agent deployment.

### Step 1: Navigate to Pipeline

1. Go to **Jenkins Dashboard**
2. Click on your **Deploy-Smart-Agent** pipeline

### Step 2: Build with Parameters

1. Click **Build with Parameters** in the left sidebar
2. Review the default parameters:
   - **SMARTAGENT_ZIP_PATH**: Verify path is correct
   - **REMOTE_INSTALL_DIR**: `/opt/appdynamics/appdsmartagent`
   - **APPD_USER**: `ubuntu` (or your SSH user)
   - **APPD_GROUP**: `ubuntu`
   - **SSH_PORT**: `22`
   - **AGENT_NAME**: `smartagent`
   - **LOG_LEVEL**: `DEBUG`

3. Adjust parameters if needed
4. Click **Build**

{{% notice style="tip" %}}
For your first deployment, consider testing on a single host by creating a separate credential with just one IP address.
{{% /notice %}}

### Step 3: Monitor Pipeline Execution

After clicking **Build**, you'll see:

1. **Build added to queue** - Build number appears in Build History
2. **Click build number** (e.g., #1) to view details
3. **Click Console Output** to view real-time logs

### Step 4: Understanding Console Output

The console output shows each stage of the deployment:

```
Started by user admin
Running in Durability level: MAX_SURVIVABILITY
[Pipeline] Start of Pipeline
[Pipeline] node
Running on aws-vpc-agent in /home/ubuntu/jenkins/workspace/Deploy-Smart-Agent
[Pipeline] {
[Pipeline] stage
[Pipeline] { (Preparation)
[Pipeline] script
[Pipeline] {
Preparing Smart Agent deployment to 3 hosts: 172.31.1.243, 172.31.1.48, 172.31.1.5
...
```

Key stages you'll see:
1. ✅ **Preparation** - Loads and validates host list
2. ✅ **Extract Smart Agent** - Extracts ZIP file
3. ✅ **Configure Smart Agent** - Creates config.ini
4. ✅ **Deploy to Remote Hosts** - Deploys to each host
5. ✅ **Verify Installation** - Checks Smart Agent status

### Step 5: Review Results

After completion, you'll see:

**Success:**
```
Smart Agent successfully deployed to all hosts
Finished: SUCCESS
```

**Partial Success:**
```
Deployment completed with some failures
Failed hosts: 172.31.1.48
Finished: UNSTABLE
```

**Failure:**
```
Smart Agent deployment failed. Check logs for details.
Finished: FAILURE
```

## Verifying Installation

After a successful deployment, verify Smart Agent is running on target hosts.

### Check Smart Agent Status

SSH into a target host and check the status:

```bash
# SSH to target host
ssh ubuntu@172.31.1.243

# Navigate to installation directory
cd /opt/appdynamics/appdsmartagent

# Check Smart Agent status
sudo ./smartagentctl status
```

**Expected output:**
```
Smart Agent is running (PID: 12345)
Service: appdsmartagent.service
Status: active (running)
```

### List Installed Agents

```bash
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl list
```

**Expected output:**
```
No agents currently installed
(Use install-machine-agent or install-db-agent pipelines to add agents)
```

### Check Logs

```bash
cd /opt/appdynamics/appdsmartagent
tail -f log.log
```

Look for successful connection messages to the AppDynamics controller.

### Verify in AppDynamics Controller

1. Log into your AppDynamics Controller
2. Navigate to **Servers → Servers**
3. Look for your newly deployed hosts
4. Verify Smart Agent is reporting metrics

## Installing Additional Agents

Once Smart Agent is deployed, you can install specific agent types using the other pipelines.

### Install Machine Agent

1. Go to **Install-Machine-Agent** pipeline
2. Click **Build with Parameters**
3. Review parameters:
   - **AGENT_NAME**: `machine-agent`
   - **SSH_PORT**: `22`
4. Click **Build**

The pipeline will SSH to each host and execute:
```bash
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl install --component machine
```

### Install Database Agent

1. Go to **Install-Database-Agent** pipeline
2. Click **Build with Parameters**
3. Configure database connection parameters
4. Click **Build**

The pipeline will install and configure the Database Agent on all hosts.

### Verify Agent Installation

After installing agents, verify they appear:

```bash
cd /opt/appdynamics/appdsmartagent
sudo ./smartagentctl list
```

**Expected output:**
```
Installed agents:
- machine-agent (running)
- db-agent (running)
```

## Common Deployment Scenarios

### Scenario 1: Initial Deployment

**Workflow:**
1. Run **Deploy-Smart-Agent** pipeline
2. Wait for completion and verify
3. Run **Install-Machine-Agent** if needed
4. Run **Install-Database-Agent** if needed

### Scenario 2: Update Smart Agent

To update Smart Agent to a new version:

1. Download new Smart Agent ZIP
2. Place it in Jenkins at configured path
3. Run **Deploy-Smart-Agent** pipeline again

The pipeline automatically:
- Stops existing Smart Agent
- Removes old files
- Installs new version
- Restarts Smart Agent

### Scenario 3: Add New Hosts

To add Smart Agent to new hosts:

1. Update the `deployment-hosts` credential in Jenkins
2. Add new IP addresses (one per line)
3. Run **Deploy-Smart-Agent** pipeline

The pipeline will:
- Skip already-configured hosts (if idempotent)
- Deploy to new hosts only

### Scenario 4: Complete Removal

To completely remove Smart Agent from all hosts:

1. Go to **Cleanup-All-Agents** pipeline
2. Click **Build with Parameters**
3. **Check** the `CONFIRM_CLEANUP` checkbox
4. Click **Build**

{{% notice style="danger" %}}
This will permanently delete `/opt/appdynamics/appdsmartagent` directory from all hosts. This action cannot be undone.
{{% /notice %}}

## Troubleshooting Deployments

### Build Fails at Preparation Stage

**Symptom**: Pipeline fails when loading host list

**Cause**: Missing or incorrect `deployment-hosts` credential

**Solution**:
1. Go to **Manage Jenkins → Credentials**
2. Verify `deployment-hosts` credential exists
3. Check format (one IP per line, no commas)
4. Ensure no trailing spaces

### SSH Connection Failures

**Symptom**: "Permission denied" or "Connection refused" errors

**Solutions**:

**Check security group:**
```bash
# Verify Jenkins agent can reach target
ping 172.31.1.243
telnet 172.31.1.243 22
```

**Test SSH manually:**
```bash
# From Jenkins agent machine
ssh -i /path/to/key ubuntu@172.31.1.243
```

**Verify SSH key:**
1. Ensure `ssh-private-key` credential is correct
2. Verify public key is in `~/.ssh/authorized_keys` on target hosts

### Smart Agent Fails to Start

**Symptom**: Deployment completes but Smart Agent not running

**Solution**:

**Check logs on target host:**
```bash
cd /opt/appdynamics/appdsmartagent
cat log.log
```

**Common issues:**
- **Invalid access key**: Check `account-access-key` credential
- **Network connectivity**: Verify outbound HTTPS to Controller
- **Permission issues**: Ensure APPD_USER has correct permissions

### Partial Deployment Success

**Symptom**: Some hosts succeed, others fail

**Solution**:

1. **Check Console Output** - Identifies which hosts failed
2. **Investigate failed hosts** - SSH and test manually
3. **Re-run pipeline** - Jenkins tracks which hosts need retry

## Pipeline Best Practices

### 1. Test on Single Host First

Always test new configurations on a single host before deploying to production:

```
1. Create deployment-hosts-test credential (1 IP)
2. Create test pipeline pointing to this credential
3. Verify success
4. Deploy to full host list
```

### 2. Use Descriptive Build Descriptions

After triggering a build, add a description:

1. Go to build page
2. Click **Edit Build Information**
3. Add description: "Production deployment - Q4 2024"

### 3. Monitor Build History

Regularly check build history for patterns:
- Failed builds
- Duration trends
- Error messages

### 4. Schedule Deployments During Maintenance Windows

For production systems:
- Use Jenkins scheduled builds
- Deploy during low-traffic periods
- Have rollback plan ready

### 5. Keep Credentials Updated

- Rotate SSH keys quarterly
- Update host lists as infrastructure changes
- Verify AppDynamics access key validity

## Next Steps

Now let's explore scaling and operational considerations for large deployments.
