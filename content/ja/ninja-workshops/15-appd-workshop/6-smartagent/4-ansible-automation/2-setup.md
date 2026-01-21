---
title: Setup & Configuration
weight: 2
time: 10 minutes
---

## Step 2: Prepare Your Files and Directory Structure

Create a project directory for your Ansible deployment. It should contain the following files:

```text
.
├── appdsmartagent_64_linux_24.6.0.2143.deb  # Debian package
├── appdsmartagent_64_linux_24.6.0.2143.rpm  # RedHat package
├── inventory-cloud.yaml                     # Inventory file
├── smartagent.yaml                          # Playbook
└── variables.yaml                           # Variables file
```

Ensure you have downloaded the correct Smart Agent packages for your target environments.

## Step 3: Understanding the Files

### 1. Inventory Files (`inventory-cloud.yaml`)

The inventory file lists the hosts where the Smart Agent will be deployed. Define your hosts and authentication details here.

```yaml
all:
  hosts:
    smartagent-host-1:
      ansible_host: 54.173.1.106
      ansible_username: ec2-user
      ansible_password: ins3965!
      ansible_become: yes
      ansible_become_method: sudo
      ansible_become_password: ins3965!
      ansible_ssh_common_args: '-o StrictHostKeyChecking=no'

    smartagent-host-2:
      ansible_host: 192.168.86.107
      ansible_username: aleccham
      ansible_password: ins3965!
      ansible_become: yes
      ansible_become_method: sudo
      ansible_become_password: ins3965!

    smartagent-host-3:
      ansible_host: 54.82.95.69
      ansible_username: ubuntu
      ansible_password: ins3965!
      ansible_become: yes
      ansible_become_method: sudo
      ansible_become_password: ins3965!
```

**Action**: Update the `ansible_host` IPs and credentials with your actual lab environment details.

### 2. Variables File (`variables.yaml`)

This file contains the configuration details for the Smart Agent.

```yaml
smart_agent:
  controller_url: 'CONTROLLER URL HERE, JUST THE BASE URL' # o11y.saas.appdynamics.com
  account_name: 'Account Name Here'
  account_access_key: 'YOUR ACCESS KEY HERE'
  fm_service_port: '443' # Use 443 or 8080 depending on your environment.
  ssl: true

smart_agent_package_debian: 'appdsmartagent_64_linux_24.6.0.2143.deb'  # or the appropriate package name
smart_agent_package_redhat: 'appdsmartagent_64_linux_24.6.0.2143.rpm'  # or the appropriate package name
```

**Action**: Update the `smart_agent` section with your specific controller URL, account name, and access key.

### 3. Playbook (`smartagent.yaml`)

The playbook orchestrates the deployment of the Cisco AppDynamics Distribution of OpenTelemetry Collector. Here is a concise summary of its tasks:

1. **Prerequisites**: Installs necessary packages (`yum-utils` for RedHat, `curl`/`apt-transport-https` for Debian).
2. **Directory Setup**: Ensures the `/opt/appdynamics/appdsmartagent` directory exists.
3. **Configuration**:
    * Checks if `config.ini` exists.
    * Creates a default `config.ini` using values from `variables.yaml` if missing.
    * Updates configuration keys (AccountAccessKey, ControllerURL, etc.) using `lineinfile` to ensure settings are correct.
4. **Package Management**:
    * Determines the correct package path based on OS family (Debian/RedHat).
    * Fails if the package is missing locally.
    * Copies the package to the target host's `/tmp` directory.
    * Installs the package using `dpkg` or `yum`.
5. **Service Management**: Restarts the `smartagent` service.
6. **Cleanup**: Removes the temporary package file.

The playbook uses `when: ansible_os_family == ...` conditionals to handle both RedHat and Debian systems within the same workflow.
