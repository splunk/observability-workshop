---
title: 1. Prerequisites
weight: 1
---

Before you begin installing Smart Agent on remote hosts, ensure you have the following prerequisites in place:

## Required Access

- **SSH Access**: You must have SSH access to all remote hosts where you plan to install Smart Agent
- **SSH Private Key**: A configured SSH private key for authentication
- **Sudo Privileges**: The control node user needs sudo privileges to run smartagentctl
- **Remote SSH**: Remote hosts must have SSH enabled and accessible

## Directory Structure

The Smart Agent installation directory should be set up on your control node:

```bash
cd /home/ubuntu/appdsm
```

The directory contains:
- `smartagentctl` - Command-line utility to manage SmartAgent
- `smartagent` - The SmartAgent binary
- `config.ini` - Main configuration file
- `remote.yaml` - Remote hosts configuration file
- `conf/` - Additional configuration files
- `lib/` - Required libraries

## AppDynamics Account Information

You'll need the following information from your AppDynamics account:

- **Controller URL**: Your AppDynamics SaaS controller endpoint (e.g., `fso-tme.saas.appdynamics.com`)
- **Account Name**: Your AppDynamics account name
- **Account Access Key**: Your AppDynamics account access key
- **Controller Port**: Usually 443 for HTTPS connections

## Target Host Requirements

Your remote hosts should meet these requirements:

- **Operating System**: Ubuntu/Linux-based systems
- **SSH Server**: SSH daemon running and accepting connections
- **User Account**: User account with appropriate permissions (typically root)
- **Network Access**: Ability to reach the AppDynamics Controller
- **Disk Space**: Sufficient space for Smart Agent installation (typically under 100MB)

## Security Considerations

Before proceeding, review these security best practices:

1. **SSH Keys**: Use strong SSH keys (RSA 4096-bit or ED25519)
2. **Access Keys**: Store AccountAccessKey securely
3. **Host Key Validation**: For production, plan to validate host keys
4. **SSL/TLS**: Always use SSL/TLS for controller communication
5. **Log Files**: Restrict access to log files containing sensitive information

## Verifying Prerequisites

### Check SSH Connectivity

Test SSH connectivity to your remote hosts:

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@<remote-host-ip>
```

### Verify SSH Key Permissions

Ensure proper permissions on your SSH key:

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
```

### Check Network Connectivity

Verify that remote hosts can reach each other and the internet:

```bash
ping <remote-host-ip>
```

### Verify Sudo Access

Ensure you have sudo privileges:

```bash
sudo -v
```

If all prerequisites are met, you're ready to proceed with configuration!
