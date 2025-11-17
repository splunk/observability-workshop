---
title: 2. Configuration
weight: 2
---

Smart Agent remote installation requires two key configuration files: `config.ini` for Smart Agent settings and `remote.yaml` for defining remote hosts and connection parameters.

## Configuration Files Overview

Both configuration files should be located in the Smart Agent installation directory:

```bash
cd /home/ubuntu/appdsm
```

The two files you'll configure:
- `config.ini` - Smart Agent configuration deployed to all remote hosts
- `remote.yaml` - Remote hosts and SSH connection settings

## config.ini - Smart Agent Configuration

The `config.ini` file contains the main Smart Agent configuration that will be deployed to all remote hosts.

**Location:** `/home/ubuntu/appdsm/config.ini`

### Controller Configuration

Configure your AppDynamics Controller connection:

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
ControllerPort   = 443
FMServicePort    = 443
AccountAccessKey = your-access-key-here
AccountName      = your-account-name
EnableSSL        = true
```

**Key Parameters:**
- `ControllerURL`: Your AppDynamics SaaS controller endpoint
- `ControllerPort`: HTTPS port for the controller (default: 443)
- `FMServicePort`: Flow Monitoring service port
- `AccountAccessKey`: Your AppDynamics account access key
- `AccountName`: Your AppDynamics account name
- `EnableSSL`: Enable SSL/TLS encryption (should be `true` for production)

### Common Configuration

Define the agent's identity and polling behavior:

```ini
[CommonConfig]
AgentName            = smartagent
PollingIntervalInSec = 300
Tags                 = environment:production,region:us-east
ServiceName          = my-application
```

**Parameters:**
- `AgentName`: Name identifier for the agent
- `PollingIntervalInSec`: How often the agent polls for data (in seconds)
- `Tags`: Custom tags for categorizing agents (comma-separated)
- `ServiceName`: Optional service name for logical grouping

### Telemetry Settings

Configure logging and profiling:

```ini
[Telemetry]
LogLevel  = DEBUG
LogFile   = /opt/appdynamics/appdsmartagent/log.log
Profiling = false
```

**Parameters:**
- `LogLevel`: Logging verbosity (`DEBUG`, `INFO`, `WARN`, `ERROR`)
- `LogFile`: Path where logs will be written on remote hosts
- `Profiling`: Enable performance profiling (`true`/`false`)

### TLS Client Settings

Configure proxy and TLS settings:

```ini
[TLSClientSetting]
Insecure        = false
AgentHTTPProxy  = 
AgentHTTPSProxy = 
AgentNoProxy    = 
```

**Parameters:**
- `Insecure`: Skip TLS certificate verification (not recommended for production)
- `AgentHTTPProxy`: HTTP proxy server URL (if required)
- `AgentHTTPSProxy`: HTTPS proxy server URL (if required)
- `AgentNoProxy`: Comma-separated list of hosts to bypass proxy

### Auto Discovery

Configure automatic application discovery:

```ini
[AutoDiscovery]
RunAutoDiscovery          = false
ExcludeLabels             = process.cpu.usage,process.memory.usage
ExcludeProcesses          = 
ExcludeUsers              = 
AutoDiscoveryTimeInterval = 4h
AutoInstall               = false
```

**Parameters:**
- `RunAutoDiscovery`: Automatically discover applications (`true`/`false`)
- `ExcludeLabels`: Metrics to exclude from discovery
- `ExcludeProcesses`: Process names to exclude from monitoring
- `ExcludeUsers`: User accounts to exclude from monitoring
- `AutoDiscoveryTimeInterval`: How often to run discovery (e.g., `4h`, `30m`)
- `AutoInstall`: Automatically install discovered applications

### Task Configuration

Configure native instrumentation:

```ini
[TaskConfig]
NativeEnable        = true
UserPortalUserName  = 
UserPortalPassword  = 
UserPortalAuth      = none
AutoUpdateLdPreload = true
```

**Parameters:**
- `NativeEnable`: Enable native instrumentation
- `AutoUpdateLdPreload`: Automatically update LD_PRELOAD settings

## remote.yaml - Remote Hosts Configuration

The `remote.yaml` file defines the remote hosts where Smart Agent will be installed and the connection parameters.

**Location:** `/home/ubuntu/appdsm/remote.yaml`

### Example Configuration

```yaml
max_concurrency: 4
remote_dir: "/opt/appdynamics/appdsmartagent"
protocol:
  type: ssh
  auth:
    username: ubuntu
    private_key_path: /home/ubuntu/.ssh/id_rsa
    privileged: true
    ignore_host_key_validation: true
    known_hosts_path: /home/ubuntu/.ssh/known_hosts
hosts:
  - host: "172.31.1.243"
    port: 22
    user: root
    group: root
  - host: "172.31.1.48"
    port: 22
    user: root
    group: root
  - host: "172.31.1.142"
    port: 22
    user: root
    group: root
  - host: "172.31.1.5"
    port: 22
    user: root
    group: root
```

### Global Settings

**max_concurrency:** Maximum number of hosts to process simultaneously
- Default: `4`
- Increase for faster deployment to many hosts
- Decrease if experiencing network or resource constraints

**remote_dir:** Installation directory on remote hosts
- Default: `/opt/appdynamics/appdsmartagent`
- Must be an absolute path
- User must have write permissions

### Protocol Configuration

**type:** Connection protocol
- Value: `ssh`

**auth.username:** SSH username for authentication
- Example: `ubuntu`, `ec2-user`, `centos`
- Must match the user configured on remote hosts

**auth.private_key_path:** Path to SSH private key
- Must be an absolute path
- Key must be accessible and have proper permissions (600)

**auth.privileged:** Run agent with elevated privileges
- `true`: Install as root/systemd service
- `false`: Install as a user process
- Recommended: `true` for production deployments

**auth.ignore_host_key_validation:** Skip SSH host key verification
- `true`: Skip verification (useful for testing)
- `false`: Validate host keys (recommended for production)

**auth.known_hosts_path:** Path to SSH known_hosts file
- Default: `/home/ubuntu/.ssh/known_hosts`
- Used when host key validation is enabled

### Host Definitions

Each host entry requires:

**host:** IP address or hostname of the remote machine
- Can be IPv4, IPv6, or hostname
- Must be reachable from the control node

**port:** SSH port
- Default: `22`
- Change if SSH is running on a non-standard port

**user:** User account that will own the Smart Agent process
- Typically `root` for system-wide installation
- Can be a regular user for user-specific installation

**group:** Group that will own the Smart Agent process
- Typically matches the user (e.g., `root`)

### Adding More Hosts

To add additional remote hosts, append to the `hosts` list:

```yaml
hosts:
  - host: "10.0.1.10"
    port: 22
    user: root
    group: root
  - host: "10.0.1.11"
    port: 22
    user: root
    group: root
```

{{% notice title="Tip" style="info" icon="info-circle" %}}
You can add as many hosts as needed. The `max_concurrency` setting controls how many are processed in parallel.
{{% /notice %}}

## Verifying Configuration

Before proceeding with installation, verify your configuration files:

### Review remote.yaml

```bash
cat /home/ubuntu/appdsm/remote.yaml
```

Check that:
- All host IP addresses are correct
- SSH key path is valid
- Remote directory path is appropriate

### Review config.ini

```bash
cat /home/ubuntu/appdsm/config.ini
```

Verify that:
- Controller URL and account information are correct
- Log file paths are valid
- Settings match your environment requirements

### Validate YAML Syntax

Ensure your YAML file is properly formatted:

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

If the command completes without errors, your YAML syntax is valid.

Once your configuration files are ready, you can proceed with the installation!
