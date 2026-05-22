---
title: Jenkins Setup
weight: 2
time: 10 minutes
---

## Prerequisites

Before you begin, ensure you have:

- Jenkins server (version 2.300 or later)
- A Jenkins agent in the same AWS VPC as your target EC2 instances
- SSH key pair for authentication to target hosts
- AppDynamics Smart Agent package
- Target Ubuntu EC2 instances with SSH access

## Required Jenkins Plugins

Install these plugins via **Manage Jenkins → Plugins → Available Plugins**:

1. **Pipeline** (core plugin, usually pre-installed)
2. **SSH Agent Plugin**
3. **Credentials Plugin** (usually pre-installed)
4. **Git Plugin** (if using SCM)

To install:
1. Navigate to **Manage Jenkins → Plugins**
2. Click **Available** tab
3. Search for each plugin
4. Select and click **Install**

## Configure Jenkins Agent

Your Jenkins agent must be able to reach target EC2 instances via private IPs. There are two main options:

### Option A: EC2 Instance as Agent

1. **Launch EC2 instance in same VPC** as your target hosts

2. **Install Java** (required by Jenkins):
   ```bash
   sudo apt-get update
   sudo apt-get install -y openjdk-11-jdk
   ```

3. **Add agent in Jenkins**:
   - Go to **Manage Jenkins → Nodes → New Node**
   - Name: `aws-vpc-agent` (or your preferred name)
   - Type: **Permanent Agent**
   - Configure:
     - **Remote root directory**: `/home/ubuntu/jenkins`
     - **Labels**: `linux` (must match pipeline agent label)
     - **Launch method**: Launch agent via SSH
     - **Host**: EC2 private IP
     - **Credentials**: Add SSH credentials for agent

### Option B: Use Existing Linux Agent

- Ensure agent has label `linux`
- Verify network connectivity to target hosts
- Confirm SSH client is installed

### Configure Agent Labels

{{% notice style="warning" %}}
All pipelines in this workshop use the `linux` label. Make sure your agent is configured with this label.
{{% /notice %}}

To set or modify labels:
1. Go to **Manage Jenkins → Nodes**
2. Click on your agent
3. Click **Configure**
4. Set **Labels** to `linux`
5. Click **Save**

## Credentials Setup

Navigate to: **Manage Jenkins → Credentials → System → Global credentials (unrestricted)**

You'll need to create three credentials for the pipelines to work.

### 1. SSH Private Key for Target Hosts

This credential allows Jenkins to SSH into your target EC2 instances.

**Type**: SSH Username with private key

- **ID**: `ssh-private-key` (must match exactly)
- **Description**: `SSH key for EC2 target hosts`
- **Username**: `ubuntu` (or your SSH user)
- **Private Key**: Choose one:
  - **Enter directly**: Paste your PEM file content
  - **From file**: Upload PEM file
  - **From Jenkins master**: Specify path

**Example format**:
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
...
-----END RSA PRIVATE KEY-----
```

### 2. Deployment Hosts List

This credential contains the list of all target hosts where Smart Agent should be deployed.

**Type**: Secret text

- **ID**: `deployment-hosts` (must match exactly)
- **Description**: `List of target EC2 host IPs`
- **Secret**: Enter newline-separated IPs

**Example**:
```
172.31.1.243
172.31.1.48
172.31.1.5
172.31.10.20
172.31.10.21
```

{{% notice style="important" %}}
**Format Requirements:**
- One IP per line
- No commas
- No spaces
- No extra characters
- Use Unix line endings (LF, not CRLF)
{{% /notice %}}

### 3. AppDynamics Account Access Key

This credential contains your AppDynamics account access key for Smart Agent authentication.

**Type**: Secret text

- **ID**: `account-access-key` (must match exactly)
- **Description**: `AppDynamics account access key`
- **Secret**: Your AppDynamics access key

**Example**: `abcd1234-ef56-7890-gh12-ijklmnopqrst`

{{% notice style="tip" %}}
You can find your AppDynamics access key in the Controller under **Settings → License → Account**.
{{% /notice %}}

## Credential Security Best Practices

Follow these best practices for credential management:

- ✅ Use Jenkins credential encryption (built-in)
- ✅ Restrict access via Jenkins role-based authorization
- ✅ Rotate SSH keys periodically
- ✅ Use least-privilege IAM roles for EC2 instances
- ✅ Enable audit logging for credential access
- ✅ Never commit credentials to version control

## Smart Agent Package Setup

The Smart Agent ZIP file should be placed in a location accessible to Jenkins. The recommended approach is to store it in the Jenkins home directory.

### Download Smart Agent

```bash
# Download from AppDynamics
curl -o appdsmartagent_64_linux.zip \
  "https://download.appdynamics.com/download/prox/download-file/smart-agent/latest/appdsmartagent_64_linux.zip"

# Verify the download
ls -lh appdsmartagent_64_linux.zip
```

### Storage Location

The pipelines reference the Smart Agent ZIP at: `/var/jenkins_home/smartagent/appdsmartagent.zip`

You can either:
1. Place the ZIP at this exact location
2. Modify the `SMARTAGENT_ZIP_PATH` pipeline parameter to point to your ZIP location

## Verify Configuration

Before proceeding to pipeline creation, verify your setup:

### 1. Check Agent Status

1. Go to **Manage Jenkins → Nodes**
2. Verify your agent shows as "online"
3. Confirm label is set to `linux`

### 2. Test SSH Connectivity

Create a simple test pipeline to verify SSH works:

```groovy
pipeline {
    agent { label 'linux' }
    stages {
        stage('Test SSH') {
            steps {
                withCredentials([
                    sshUserPrivateKey(credentialsId: 'ssh-private-key', 
                                     keyFileVariable: 'SSH_KEY', 
                                     usernameVariable: 'SSH_USER'),
                    string(credentialsId: 'deployment-hosts', variable: 'HOSTS')
                ]) {
                    sh '''
                        echo "Testing SSH credentials..."
                        echo "$HOSTS" | head -1 | while read HOST; do
                            ssh -i $SSH_KEY \
                                -o StrictHostKeyChecking=no \
                                -o ConnectTimeout=10 \
                                $SSH_USER@$HOST \
                                "echo 'Connection successful'"
                        done
                    '''
                }
            }
        }
    }
}
```

### 3. Verify Credentials Exist

1. Go to **Manage Jenkins → Credentials**
2. Confirm all three credentials are listed:
   - `ssh-private-key`
   - `deployment-hosts`
   - `account-access-key`

## Troubleshooting Common Issues

### Agent Not Available

**Symptom**: "No agent available" error when running pipelines

**Solution**:
- Check: **Manage Jenkins → Nodes**
- Ensure agent is online
- Verify agent has `linux` label
- Test agent connectivity

### SSH Connection Failures

**Symptom**: Cannot connect to target hosts via SSH

**Solution**:
```bash
# Test from Jenkins agent machine
ssh -i /path/to/key ubuntu@172.31.1.243 -o ConnectTimeout=10

# Check security group allows SSH from agent
# Verify private key matches public key on target
```

### Credential Not Found

**Symptom**: "Credential not found" error

**Solution**:
- Verify credential IDs exactly match:
  - `ssh-private-key`
  - `deployment-hosts`
  - `account-access-key`
- Check credential scope is set to **Global**

### Permission Denied on Target Hosts

**Symptom**: SSH succeeds but commands fail with permission denied

**Solution**:
```bash
# On target host, verify user is in sudoers
sudo visudo
# Add line:
ubuntu ALL=(ALL) NOPASSWD: ALL
```

## Next Steps

Now that Jenkins is configured with credentials and agents, you're ready to create the deployment pipelines!
