---
title: 3. Installation & Startup
weight: 3
---

Now that your configuration files are ready, you can install and start Smart Agent on your remote hosts using the `smartagentctl` command-line tool.

## Installation Process Overview

The installation process involves:

1. **Connection**: Establishes SSH connections to all defined hosts
2. **Transfer**: Copies Smart Agent binaries and configuration to remote hosts
3. **Installation**: Installs Smart Agent in `/opt/appdynamics/appdsmartagent/` on each host
4. **Startup**: Starts the Smart Agent process on each remote host
5. **Logging**: Outputs detailed progress to console and log file

## Step 1: Navigate to Installation Directory

Change to the Smart Agent installation directory:

```bash
cd /home/ubuntu/appdsm
```

## Step 2: Verify Configuration Files

Before starting the installation, verify your configuration files are properly set up:

### Review remote hosts configuration

```bash
cat remote.yaml
```

Ensure all host IP addresses, ports, and SSH settings are correct.

### Review agent configuration

```bash
cat config.ini
```

Verify that controller URL, account credentials, and other settings are accurate.

## Step 3: Start Smart Agent on Remote Hosts

Run the following command to start Smart Agent on all remote hosts defined in `remote.yaml`:

```bash
sudo ./smartagentctl start --remote --verbose
```

### Command Breakdown

- `sudo`: Required for privileged operations
- `./smartagentctl`: The control utility
- `start`: Command to start the Smart Agent
- `--remote`: Deploy to remote hosts (reads from `remote.yaml`)
- `--verbose`: Enable detailed debug logging

{{% notice title="Note" style="warning" icon="triangle-exclamation" %}}
The `--verbose` flag is highly recommended as it provides detailed output about the installation progress and helps identify any issues.
{{% /notice %}}

## Step 4: Monitor the Installation

The `--verbose` flag provides detailed output including:

- SSH connection status
- File transfer progress
- Installation steps on each host
- Agent startup status
- Any errors or warnings

### Expected Output

You should see output similar to:

```
Starting Smart Agent deployment to remote hosts...
Connecting to 172.31.1.243:22...
Connection successful: 172.31.1.243
Transferring Smart Agent binaries...
Installing Smart Agent on 172.31.1.243...
Starting Smart Agent on 172.31.1.243...
Smart Agent started successfully on 172.31.1.243

Connecting to 172.31.1.48:22...
...
```

## Step 5: Verify Installation

After the installation completes, verify that Smart Agent is running on the remote hosts.

### Check Status Remotely

Use the status command to check all remote hosts:

```bash
sudo ./smartagentctl status --remote --verbose
```

This will query each host and report whether Smart Agent is running.

### Check Logs on Control Node

View logs on the control node:

```bash
tail -f /home/ubuntu/appdsm/log.log
```

### SSH to Remote Host and Check

You can also SSH to a remote host and check directly:

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
ps aux | grep smartagent
```

## Additional Commands

### Install Without Starting

To install Smart Agent without starting it:

```bash
sudo ./smartagentctl install --remote --verbose
```

This copies the binaries and configuration but doesn't start the agent process.

### Stop Smart Agent

To stop Smart Agent on all remote hosts:

```bash
sudo ./smartagentctl stop --remote --verbose
```

### Install as System Service

To install Smart Agent as a systemd service (recommended for production):

```bash
sudo ./smartagentctl start --remote --verbose --service
```

When installed as a service:

- Smart Agent will start automatically on system boot
- Can be managed using `systemctl` commands
- Better integration with system logging

### Uninstall Smart Agent

To completely remove Smart Agent from remote hosts:

```bash
sudo ./smartagentctl uninstall --remote --verbose
```

{{% notice title="Warning" style="danger" icon="exclamation-triangle" %}}
The uninstall command will remove all Smart Agent files from the remote hosts. Make sure you have backups of any important configuration or log files.
{{% /notice %}}

## Verifying in AppDynamics Controller

After starting Smart Agent on remote hosts:

1. **Log into AppDynamics Controller**: Navigate to your controller URL
2. **Go to Servers**: Check the Servers section in the Controller UI
3. **Verify Agents**: You should see your Smart Agents appear in the list
4. **Check Metrics**: Verify that metrics are being collected from each host

### Expected Timeline

- **Agent Registration**: Agents typically appear in the Controller within 1-2 minutes
- **Initial Metrics**: First metrics usually arrive within 5 minutes
- **Full Data**: Complete data collection starts after the first polling interval (configured in `config.ini`)

## Log File Locations

Logs are written to both the control node and remote hosts:

| Location | Path | Description |
|----------|------|-------------|
| **Control Node** | `/home/ubuntu/appdsm/log.log` | Installation and deployment logs |
| **Remote Hosts** | `/opt/appdynamics/appdsmartagent/log.log` | Agent runtime logs |

## Understanding Concurrency

The `max_concurrency` setting in `remote.yaml` controls parallel execution:

- **Lower values (1-2)**: Sequential processing, slower but safer
- **Default (4)**: Good balance for most environments
- **Higher values (8+)**: Faster deployment to many hosts, requires more resources

Example: With 12 hosts and `max_concurrency: 4`:

- First batch: Hosts 1-4 processed simultaneously
- Second batch: Hosts 5-8 processed simultaneously  
- Third batch: Hosts 9-12 processed simultaneously

## What Happens on Each Remote Host

When you run the start command, the following occurs on each remote host:

1. **Directory Creation**: Creates `/opt/appdynamics/appdsmartagent/`
2. **File Transfer**: Copies `smartagent` binary, `config.ini`, and libraries
3. **Permission Setting**: Sets appropriate file permissions
4. **Process Start**: Launches the Smart Agent process
5. **Verification**: Confirms the process is running

## Next Steps

After successfully installing and starting Smart Agent:

1. ✅ Verify agents appear in the AppDynamics Controller UI
2. ✅ Check that metrics are being collected
3. ✅ Configure application monitoring as needed
4. ✅ Set up alerts and dashboards
5. ✅ Monitor agent health and performance

If you encounter any issues, proceed to the Troubleshooting section.
