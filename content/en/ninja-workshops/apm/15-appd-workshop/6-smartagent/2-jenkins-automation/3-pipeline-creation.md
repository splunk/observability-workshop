---
title: Pipeline Creation
weight: 3
time: 10 minutes
---

## Overview

The GitHub repository contains four main pipelines for managing the Smart Agent lifecycle:

1. **Deploy Smart Agent** - Installs and starts Smart Agent service
2. **Install Machine Agent** - Installs Machine Agent via smartagentctl
3. **Install Database Agent** - Installs Database Agent via smartagentctl  
4. **Cleanup All Agents** - Removes /opt/appdynamics directory

All pipeline code is available in the [sm-jenkins GitHub repository](https://github.com/chambear2809/sm-jenkins).

## Pipeline Files

The repository contains these Jenkinsfile pipeline definitions:

```
sm-jenkins/
└── pipelines/
    ├── Jenkinsfile.deploy                  # Deploy Smart Agent
    ├── Jenkinsfile.install-machine-agent  # Install Machine Agent
    ├── Jenkinsfile.install-db-agent       # Install Database Agent
    └── Jenkinsfile.cleanup                # Cleanup All Agents
```

## Creating Pipelines in Jenkins

For each Jenkinsfile you want to use, follow these steps to create a pipeline in Jenkins.

### Method 1: Pipeline from SCM (Recommended)

This method keeps your pipeline code in version control and automatically syncs changes.

#### Step 1: Fork or Clone the Repository

First, fork the repository to your own GitHub account or organization, or use the original repository directly.

**Repository URL**: `https://github.com/chambear2809/sm-jenkins`

#### Step 2: Create Pipeline in Jenkins

1. Go to **Jenkins Dashboard**
2. Click **New Item**
3. Enter item name (e.g., `Deploy-Smart-Agent`)
4. Select **Pipeline**
5. Click **OK**

#### Step 3: Configure Pipeline

In the pipeline configuration page:

**General Section:**
- **Description**: `Deploys AppDynamics Smart Agent to multiple hosts`
- Leave **Discard old builds** unchecked (or configure as desired)

**Build Triggers:**
- Leave unchecked for manual-only execution
- Or configure webhook/polling if desired

**Pipeline Section:**
- **Definition**: Select `Pipeline script from SCM`
- **SCM**: Select `Git`
- **Repository URL**: `https://github.com/chambear2809/sm-jenkins`
- **Credentials**: Add if using a private repository
- **Branch Specifier**: `*/main` (or `*/master`)
- **Script Path**: `pipelines/Jenkinsfile.deploy`

#### Step 4: Save

Click **Save** to create the pipeline.

#### Step 5: Repeat for Other Pipelines

Repeat steps 2-4 for each pipeline you want to create, using the appropriate script path:

| Pipeline Name | Script Path |
|---------------|-------------|
| Deploy-Smart-Agent | `pipelines/Jenkinsfile.deploy` |
| Install-Machine-Agent | `pipelines/Jenkinsfile.install-machine-agent` |
| Install-Database-Agent | `pipelines/Jenkinsfile.install-db-agent` |
| Cleanup-All-Agents | `pipelines/Jenkinsfile.cleanup` |

### Method 2: Direct Pipeline Script

Alternatively, you can copy the Jenkinsfile content directly into Jenkins.

1. **Create New Item** (same as Method 1)
2. In **Pipeline** section:
   - **Definition**: Select `Pipeline script`
   - **Script**: Copy/paste the entire Jenkinsfile content from GitHub
3. **Save**

{{% notice style="tip" %}}
Method 1 (SCM) is recommended because it keeps your pipelines in version control and makes updates easier.
{{% /notice %}}

## Pipeline Parameters

Each pipeline accepts configurable parameters. Here are the key parameters for the main deployment pipeline:

### Deploy Smart Agent Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `SMARTAGENT_ZIP_PATH` | `/var/jenkins_home/smartagent/appdsmartagent.zip` | Path to Smart Agent ZIP on Jenkins server |
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | Installation directory on target hosts |
| `APPD_USER` | `ubuntu` | User to run Smart Agent process |
| `APPD_GROUP` | `ubuntu` | Group to run Smart Agent process |
| `SSH_PORT` | `22` | SSH port for remote hosts |
| `AGENT_NAME` | `smartagent` | Smart Agent name |
| `LOG_LEVEL` | `DEBUG` | Log level (DEBUG, INFO, WARN, ERROR) |

### Cleanup Pipeline Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `REMOTE_INSTALL_DIR` | `/opt/appdynamics/appdsmartagent` | Directory to remove |
| `SSH_PORT` | `22` | SSH port for remote hosts |
| `CONFIRM_CLEANUP` | `false` | Must be checked to proceed with cleanup |

{{% notice style="warning" %}}
The cleanup pipeline includes a confirmation parameter to prevent accidental deletion. You must check `CONFIRM_CLEANUP` to execute the cleanup.
{{% /notice %}}

## Understanding Pipeline Structure

Let's examine the key components of the deployment pipeline:

### 1. Agent Declaration

```groovy
agent { label 'linux' }
```

This ensures the pipeline runs on a Jenkins agent with the `linux` label.

### 2. Parameters Block

```groovy
parameters {
    string(name: 'SMARTAGENT_ZIP_PATH', ...)
    string(name: 'REMOTE_INSTALL_DIR', ...)
    // ... more parameters
}
```

Defines configurable parameters that can be set when triggering the build.

### 3. Stages

The deployment pipeline has these stages:

1. **Preparation** - Loads target hosts from credentials
2. **Extract Smart Agent** - Extracts ZIP file to staging directory
3. **Configure Smart Agent** - Creates config.ini template
4. **Deploy to Remote Hosts** - Copies files and starts Smart Agent on each host
5. **Verify Installation** - Checks Smart Agent status on all hosts

### 4. Credentials Binding

```groovy
withCredentials([
    sshUserPrivateKey(credentialsId: 'ssh-private-key', ...),
    string(credentialsId: 'account-access-key', ...)
]) {
    // Pipeline code with access to credentials
}
```

Securely loads credentials without exposing them in logs.

### 5. Post Actions

```groovy
post {
    success { ... }
    failure { ... }
    always { ... }
}
```

Defines actions to run after pipeline completion, regardless of success or failure.

## Pipeline Naming Convention

For clarity and organization, use a consistent naming convention:

**Recommended names:**
```
01-Deploy-Smart-Agent
02-Install-Machine-Agent
03-Install-Database-Agent
04-Cleanup-All-Agents
```

The numeric prefix helps maintain logical ordering in the Jenkins dashboard.

## Organizing Pipelines with Folders

For better organization, you can use Jenkins folders:

1. **Create Folder**:
   - Click **New Item**
   - Enter name: `AppDynamics Smart Agent`
   - Select **Folder**
   - Click **OK**

2. **Create Pipelines in Folder**:
   - Enter the folder
   - Create pipelines as described above

**Example structure:**
```
AppDynamics Smart Agent/
├── Deployment/
│   └── 01-Deploy-Smart-Agent
├── Agent Installation/
│   ├── 02-Install-Machine-Agent
│   └── 03-Install-Database-Agent
└── Cleanup/
    └── 04-Cleanup-All-Agents
```

## Viewing Pipeline Code

You can view the complete pipeline code in the GitHub repository:

**Main deployment pipeline:**
[https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.deploy)

**Other pipelines:**
- [Jenkinsfile.install-machine-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-machine-agent)
- [Jenkinsfile.install-db-agent](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.install-db-agent)
- [Jenkinsfile.cleanup](https://github.com/chambear2809/sm-jenkins/blob/main/pipelines/Jenkinsfile.cleanup)

## Testing Pipeline Configuration

Before running a full deployment, test your pipeline configuration:

### 1. Dry Run with Single Host

1. Create a test credential `deployment-hosts-test` with only one IP
2. Temporarily modify your pipeline to use this credential
3. Run the pipeline and verify it works on a single host
4. Once verified, update to use the full host list

### 2. Check Syntax

Jenkins provides a built-in syntax validator:

1. Go to your pipeline
2. Click **Pipeline Syntax** link
3. Use the **Declarative Directive Generator** to validate syntax

## Next Steps

With pipelines created, you're ready to execute your first Smart Agent deployment!
