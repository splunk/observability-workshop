---
title: Understanding Workflows
weight: 3
time: 10 minutes
---

## Available Workflows

The GitHub Actions lab includes **11 workflows** for complete Smart Agent lifecycle management. All workflow files are available in the repository at `.github/workflows/`.

**Repository**: [https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)

## Workflow Categories

### 1. Deployment (1 workflow)

#### Deploy Smart Agent (Batched)

- **File**: `deploy-agent-batched.yml`
- **Purpose**: Installs Smart Agent and starts the service
- **Features**:
  - Automatic batching (default: 256 hosts per batch)
  - Configurable batch size
  - Parallel deployment within each batch
  - Sequential batch processing
- **Inputs**:
  - `batch_size`: Number of hosts per batch (default: 256)
- **Trigger**: Manual only (`workflow_dispatch`)

### 2. Agent Installation (4 workflows)

All installation workflows use `smartagentctl` to install specific agent types:

#### Install Node Agent (Batched)

- **File**: `install-node-batched.yml`
- **Command**: `smartagentctl install node`
- **Batched**: Yes (configurable)

#### Install Machine Agent (Batched)

- **File**: `install-machine-batched.yml`
- **Command**: `smartagentctl install machine`
- **Batched**: Yes (configurable)

#### Install DB Agent (Batched)

- **File**: `install-db-batched.yml`
- **Command**: `smartagentctl install db`
- **Batched**: Yes (configurable)

#### Install Java Agent (Batched)

- **File**: `install-java-batched.yml`
- **Command**: `smartagentctl install java`
- **Batched**: Yes (configurable)

### 3. Agent Uninstallation (4 workflows)

All uninstallation workflows use `smartagentctl` to remove specific agent types:

#### Uninstall Node Agent (Batched)

- **File**: `uninstall-node-batched.yml`
- **Command**: `smartagentctl uninstall node`
- **Batched**: Yes (configurable)

#### Uninstall Machine Agent (Batched)

- **File**: `uninstall-machine-batched.yml`
- **Command**: `smartagentctl uninstall machine`
- **Batched**: Yes (configurable)

#### Uninstall DB Agent (Batched)

- **File**: `uninstall-db-batched.yml`
- **Command**: `smartagentctl uninstall db`
- **Batched**: Yes (configurable)

#### Uninstall Java Agent (Batched)

- **File**: `uninstall-java-batched.yml`
- **Command**: `smartagentctl uninstall java`
- **Batched**: Yes (configurable)

### 4. Smart Agent Management (2 workflows)

#### Stop and Clean Smart Agent (Batched)

- **File**: `stop-clean-smartagent-batched.yml`
- **Commands**:
  - `smartagentctl stop`
  - `smartagentctl clean`
- **Purpose**: Stops the Smart Agent service and purges all data
- **Batched**: Yes (configurable)

#### Cleanup All Agents (Batched)

- **File**: `cleanup-appdynamics.yml`
- **Command**: `sudo rm -rf /opt/appdynamics`
- **Purpose**: Completely removes the /opt/appdynamics directory
- **Batched**: Yes (configurable)
- **Warning**: This permanently deletes all AppDynamics components

{{% notice style="danger" %}}
The "Cleanup All Agents" workflow permanently deletes `/opt/appdynamics`. This action cannot be undone. Use with caution!
{{% /notice %}}

## Workflow Structure

All batched workflows follow a consistent two-job structure:

### Job 1: Prepare

```yaml
prepare:
  runs-on: self-hosted
  outputs:
    batches: ${{ steps.create-batches.outputs.batches }}
  steps:
    - name: Load hosts and create batches
      run: |
        # Load DEPLOYMENT_HOSTS variable
        # Split into batches of N hosts
        # Output as JSON array
```

**Purpose**: Loads target hosts from GitHub variables and creates batch matrix

### Job 2: Deploy/Install/Uninstall

```yaml
deploy:
  needs: prepare
  runs-on: self-hosted
  strategy:
    matrix:
      batch: ${{ fromJson(needs.prepare.outputs.batches) }}
  steps:
    - name: Setup SSH key
    - name: Execute operation on all hosts in batch (parallel)
```

**Purpose**: Runs in parallel for each batch, executing the specific operation on all hosts within the batch

## Batching Behavior

### How It Works

1. **Prepare Job** loads `DEPLOYMENT_HOSTS` and splits into batches
2. **Deploy Job** creates one matrix entry per batch
3. **Batches process sequentially** to avoid overwhelming the runner
4. **Within each batch**, all hosts deploy in parallel using background processes

### Configurable Batch Size

All workflows accept a `batch_size` input (default: 256):

```bash
# Via GitHub CLI
gh workflow run "Deploy Smart Agent" -f batch_size=128

# Via GitHub UI
Actions → Select workflow → Run workflow → Set batch_size
```

### Examples

- **100 hosts, batch_size=256**: 1 batch, ~3 minutes
- **500 hosts, batch_size=256**: 2 batches, ~6 minutes  
- **1,000 hosts, batch_size=128**: 8 batches, ~16 minutes
- **5,000 hosts, batch_size=256**: 20 batches, ~60 minutes

## Workflow Execution Order

### Typical Deployment Sequence

1. **Deploy Smart Agent** - Initial deployment
2. **Install Machine Agent** - Install specific agents as needed
3. **Install DB Agent** - Install database monitoring
4. (Use other install workflows as needed)

### Maintenance/Update Sequence

1. **Stop and Clean Smart Agent** - Stop services and clean data
2. **Deploy Smart Agent** - Redeploy with updated version
3. **Install agents again** - Reinstall required agents

### Complete Removal Sequence

1. **Stop and Clean Smart Agent** - Stop services
2. **Cleanup All Agents** - Remove /opt/appdynamics directory

## Viewing Workflow Code

You can view the complete workflow YAML files in the repository:

**Main deployment workflow:**
[https://github.com/chambear2809/github-actions-lab/blob/main/.github/workflows/deploy-agent-batched.yml](https://github.com/chambear2809/github-actions-lab/blob/main/.github/workflows/deploy-agent-batched.yml)

**All workflows:**
[https://github.com/chambear2809/github-actions-lab/tree/main/.github/workflows](https://github.com/chambear2809/github-actions-lab/tree/main/.github/workflows)

## Workflow Features

### Built-in Error Handling

- Per-host error tracking
- Failed host reporting  
- Batch-level failure handling
- Always-executed summary

### Parallel Execution

- All hosts within a batch deploy simultaneously
- Uses SSH background processes (`&`)
- Wait command ensures all complete
- Maximum parallelism within resource limits

### Security

- SSH keys never exposed in logs
- Credentials bound as environment variables
- Strict host key checking disabled for automation
- Keys removed after workflow completion

## Next Steps

Now that you understand the available workflows, let's execute your first deployment!
