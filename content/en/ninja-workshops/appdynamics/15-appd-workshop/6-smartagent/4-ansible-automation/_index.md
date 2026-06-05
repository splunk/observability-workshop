---
title: Monitoring as Code with Smart Agent and Ansible
linkTitle: Ansible Automation
weight: 4
time: 10 minutes
description: Learn how to automate AppDynamics Smart Agent deployment using Ansible.
---

## Introduction

This guide details how to deploy the Cisco AppDynamics Smart Agent across multiple hosts using Ansible. By leveraging automation, you can ensure your monitoring infrastructure is consistent, robust, and easily scalable.

## Architecture Overview

The deployment architecture leverages an Ansible Control Node to orchestrate the installation and configuration of the Smart Agent on target hosts.

```mermaid
graph TD
    CN[Ansible Control Node<br/>(macOS/Linux)] -->|SSH| H1[Target Host 1<br/>(Debian/RedHat)]
    CN -->|SSH| H2[Target Host 2<br/>(Debian/RedHat)]
    CN -->|SSH| H3[Target Host N<br/>(Debian/RedHat)]
    
    subgraph "Target Host Configuration"
        SA[Smart Agent Service]
        Config[config.ini]
        Package[Installer .deb/.rpm]
    end
    
    H1 --> SA
    H2 --> SA
    H3 --> SA
```

### Key Components

*   **Ansible Control Node**: The machine where you run the playbooks (e.g., your laptop or a jump host).
*   **Target Hosts**: The servers where the Smart Agent will be installed.
*   **Inventory**: A list of target hosts and their connection details.
*   **Playbook**: The YAML file defining the deployment tasks.

## Prerequisites

Before beginning, ensure you have:
*   Access to the target hosts via SSH.
*   Sudo privileges on the target hosts.
*   The Smart Agent installation packages (`.deb` or `.rpm`) downloaded.
*   Account details for your AppDynamics Controller (Access Key, Account Name, URL).

## Step 1: Install Ansible on macOS

To start, we need to install Ansible on your control node.

1.  **Install Homebrew** (if not already installed):

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2.  **Install Ansible**:

    ```bash
    brew install ansible
    ```

3.  **Verify the Installation**:

    ```bash
    ansible --version
    ```

    You should see output indicating the installed version of Ansible.
