---
title: 4. Troubleshooting
weight: 4
---

This section covers common issues you may encounter when deploying Smart Agent to remote hosts and how to resolve them.

## SSH Connection Issues

### Problem: Cannot Connect to Remote Hosts

**Symptoms:**
- Connection timeout errors
- "Permission denied" messages
- Host key verification failures

**Solutions:**

#### 1. Verify SSH Key Permissions

SSH keys must have the correct permissions:

```bash
chmod 600 /home/ubuntu/.ssh/id_rsa
chmod 644 /home/ubuntu/.ssh/id_rsa.pub
chmod 700 /home/ubuntu/.ssh
```

#### 2. Test SSH Connectivity Manually

Test connection to each remote host:

```bash
ssh -i /home/ubuntu/.ssh/id_rsa ubuntu@172.31.1.243
```

If this fails, the issue is with SSH configuration, not smartagentctl.

#### 3. Check Remote Host Reachability

Verify network connectivity:

```bash
ping 172.31.1.243
telnet 172.31.1.243 22
```

#### 4. Verify SSH User

Ensure the username in `remote.yaml` matches the SSH user:

```yaml
protocol:
  auth:
    username: ubuntu  # Must match your SSH user
```

#### 5. Check Known Hosts

If host key validation is enabled, ensure hosts are in known_hosts:

```bash
ssh-keyscan 172.31.1.243 >> /home/ubuntu/.ssh/known_hosts
```

Or temporarily disable host key validation in `remote.yaml`:

```yaml
protocol:
  auth:
    ignore_host_key_validation: true
```

{{% notice title="Warning" style="danger" icon="exclamation-triangle" %}}
Disabling host key validation should only be used for testing. Always enable it in production environments.
{{% /notice %}}

## Permission Issues

### Problem: Permission Denied During Installation

**Symptoms:**
- "Permission denied" when creating directories
- Cannot write to `/opt/appdynamics/`
- Insufficient privileges errors

**Solutions:**

#### 1. Verify Sudo Access on Control Node

```bash
sudo -v
```

#### 2. Check Privileged Setting

Ensure `privileged: true` is set in `remote.yaml`:

```yaml
protocol:
  auth:
    privileged: true
```

#### 3. Verify Remote User Permissions

The remote user must have sudo privileges or be root. Test on remote host:

```bash
ssh ubuntu@172.31.1.243
sudo mkdir -p /opt/appdynamics/test
sudo rm -rf /opt/appdynamics/test
```

#### 4. Check Remote Directory Permissions

If using a custom installation directory, ensure it's writable:

```bash
ssh ubuntu@172.31.1.243
ls -la /opt/appdynamics/
```

## Agent Not Starting

### Problem: Agent Installation Succeeds But Agent Doesn't Start

**Symptoms:**
- Installation completes without errors
- Agent process not running on remote hosts
- No errors in control node logs

**Solutions:**

#### 1. Check Remote Host Logs

SSH to the remote host and check the agent logs:

```bash
ssh ubuntu@172.31.1.243
tail -100 /opt/appdynamics/appdsmartagent/log.log
```

Look for error messages indicating:
- Configuration errors
- Network connectivity issues
- Missing dependencies

#### 2. Verify Agent Process

Check if the agent process is running:

```bash
ssh ubuntu@172.31.1.243
ps aux | grep smartagent
```

If not running, try starting manually:

```bash
ssh ubuntu@172.31.1.243
cd /opt/appdynamics/appdsmartagent
sudo ./smartagent
```

#### 3. Check Configuration Files

Verify that `config.ini` was properly transferred:

```bash
ssh ubuntu@172.31.1.243
cat /opt/appdynamics/appdsmartagent/config.ini
```

Ensure:
- Controller URL is correct
- Account credentials are valid
- All required fields are populated

#### 4. Test Controller Connectivity

From the remote host, verify connectivity to the AppDynamics Controller:

```bash
ssh ubuntu@172.31.1.243
curl -I https://fso-tme.saas.appdynamics.com
```

#### 5. Check System Resources

Ensure the remote host has adequate resources:

```bash
ssh ubuntu@172.31.1.243
df -h  # Check disk space
free -m  # Check memory
```

## Configuration Errors

### Problem: Invalid Configuration

**Symptoms:**
- YAML parsing errors
- Invalid configuration parameter errors
- Agent fails to start with config errors

**Solutions:**

#### 1. Validate YAML Syntax

Check for YAML syntax errors in `remote.yaml`:

```bash
python3 -c "import yaml; yaml.safe_load(open('/home/ubuntu/appdsm/remote.yaml'))"
```

Common YAML issues:
- Incorrect indentation (use spaces, not tabs)
- Missing colons
- Unquoted special characters

#### 2. Verify INI File Format

Check `config.ini` for syntax errors:

```bash
cat /home/ubuntu/appdsm/config.ini
```

Common INI issues:
- Missing section headers (e.g., `[CommonConfig]`)
- Invalid parameter names
- Missing equals signs

#### 3. Validate Controller Credentials

Ensure your AppDynamics credentials are correct:
- **ControllerURL**: Should not include `https://` or `/controller`
- **AccountAccessKey**: Should be the full access key
- **AccountName**: Should match your account name exactly

Example correct format:

```ini
ControllerURL    = fso-tme.saas.appdynamics.com
AccountAccessKey = abc123xyz789
AccountName      = fso-tme
```

## Agent Not Appearing in Controller

### Problem: Agent Starts But Doesn't Appear in Controller UI

**Symptoms:**
- Agent process is running on remote hosts
- No errors in agent logs
- Agent doesn't appear in Controller UI

**Solutions:**

#### 1. Wait for Initial Registration

Agents may take 1-5 minutes to appear in the Controller after starting.

#### 2. Verify Controller Configuration

Check that the agent can reach the controller:

```bash
ssh ubuntu@172.31.1.243
ping fso-tme.saas.appdynamics.com
curl -I https://fso-tme.saas.appdynamics.com
```

#### 3. Check Agent Logs for Connection Errors

Look for controller connection errors:

```bash
ssh ubuntu@172.31.1.243
grep -i "error\|fail\|controller" /opt/appdynamics/appdsmartagent/log.log
```

#### 4. Verify SSL/TLS Settings

Ensure SSL is enabled in `config.ini`:

```ini
EnableSSL = true
```

#### 5. Check Firewall Rules

Verify that outbound HTTPS (port 443) is allowed from remote hosts to the Controller.

#### 6. Verify Account Credentials

Double-check that your AccountAccessKey and AccountName are correct in the Controller UI:
- Log into AppDynamics Controller
- Go to Settings → License
- Verify your account name and access key

## Performance and Scaling Issues

### Problem: Slow Deployment or Timeouts

**Symptoms:**
- Deployment takes too long
- Timeout errors when deploying to many hosts
- System resource exhaustion

**Solutions:**

#### 1. Adjust Concurrency

Reduce `max_concurrency` in `remote.yaml` if experiencing issues:

```yaml
max_concurrency: 2  # Lower value for slower, more stable deployment
```

Or increase for faster deployment if resources allow:

```yaml
max_concurrency: 8  # Higher value for faster deployment
```

#### 2. Deploy in Batches

For very large deployments, split hosts into multiple groups:

**remote-batch1.yaml:**
```yaml
hosts:
  - host: "172.31.1.1"
  - host: "172.31.1.2"
  - host: "172.31.1.3"
```

**remote-batch2.yaml:**
```yaml
hosts:
  - host: "172.31.1.4"
  - host: "172.31.1.5"
  - host: "172.31.1.6"
```

Then deploy each batch separately.

#### 3. Check Network Bandwidth

Monitor network usage during deployment:

```bash
iftop
```

If bandwidth is saturated, reduce concurrency or deploy during off-peak hours.

## Log Analysis

### Checking Control Node Logs

View detailed deployment logs:

```bash
tail -f /home/ubuntu/appdsm/log.log
```

Look for:
- SSH connection failures
- File transfer errors
- Permission denied errors
- Timeout messages

### Checking Remote Host Logs

View agent runtime logs on remote hosts:

```bash
ssh ubuntu@172.31.1.243
tail -f /opt/appdynamics/appdsmartagent/log.log
```

Look for:
- Controller connection errors
- Configuration errors
- Agent startup failures
- Network issues

### Increasing Log Verbosity

For more detailed logging, set `LogLevel` to `DEBUG` in `config.ini`:

```ini
[Telemetry]
LogLevel = DEBUG
```

## Getting Help

If you're still experiencing issues:

1. **Check Documentation**: Review the smartagentctl help:
   ```bash
   ./smartagentctl --help
   ./smartagentctl start --help
   ```

2. **Review AppDynamics Documentation**: Visit the AppDynamics documentation portal

3. **Check Log Files**: Always review both control node and remote host logs

4. **Test Components Individually**: 
   - Test SSH connectivity separately
   - Test agent startup on a single host manually
   - Verify controller connectivity independently

5. **Collect Diagnostic Information**:
   - Control node logs
   - Remote host logs
   - Configuration files (with sensitive data redacted)
   - Error messages and stack traces

## Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| "Permission denied (publickey)" | SSH key authentication failure | Verify SSH key path and permissions |
| "Connection refused" | SSH port not accessible | Check firewall rules and SSH daemon |
| "No such file or directory" | Missing configuration file | Verify config files exist and paths are correct |
| "YAML parse error" | Invalid YAML syntax | Validate YAML syntax with parser |
| "Controller unreachable" | Network connectivity issue | Test controller connectivity from remote host |
| "Invalid credentials" | Wrong account key or name | Verify AppDynamics credentials |

## Best Practices for Troubleshooting

1. **Always use --verbose flag**: Provides detailed output for debugging
2. **Test with a single host first**: Deploy to one host before scaling
3. **Check logs immediately**: Review logs right after deployment
4. **Verify prerequisites**: Ensure all requirements are met before deploying
5. **Test connectivity separately**: Verify SSH and network connectivity independently
6. **Use manual commands**: Test manual SSH and agent startup to isolate issues

{{% notice title="Tip" style="info" icon="lightbulb" %}}
When troubleshooting, start with the simplest tests first (e.g., ping, SSH connectivity) before moving to more complex issues.
{{% /notice %}}
