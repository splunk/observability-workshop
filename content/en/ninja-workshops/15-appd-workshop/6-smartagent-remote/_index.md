---
title: SmartAgent Remote Installation
weight: 6
time: 2 minutes
description: Learn how to install and manage AppDynamics Smart Agent on multiple remote hosts using smartagentctl.
---

## Introduction

This workshop demonstrates how to use the **smartagentctl** command-line tool to install and manage **AppDynamics Smart Agent** on multiple remote hosts simultaneously. This approach is ideal for quickly deploying Smart Agent to a fleet of servers using SSH-based remote execution, without the need for additional automation tools like Jenkins or GitHub Actions.

![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## What You'll Learn

In this workshop, you'll learn how to:

- **Configure remote hosts** using the `remote.yaml` file
- **Configure Smart Agent settings** using `config.ini`
- **Deploy Smart Agent** to multiple hosts simultaneously via SSH
- **Start and stop agents** remotely across your infrastructure
- **Check agent status** on all remote hosts
- **Troubleshoot** common installation and connectivity issues

## Key Features

- 🚀 **Direct SSH Deployment** - No additional automation platform required
- 🔄 **Complete Lifecycle Management** - Install, start, stop, and uninstall agents
- 🏗️ **Configuration as Code** - YAML and INI-based configuration files
- 🔐 **Secure** - SSH key-based authentication
- 📈 **Concurrent Execution** - Configurable concurrency for parallel deployment
- 🎛️ **Simple CLI** - Easy-to-use smartagentctl command-line interface

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  Remote Installation Architecture                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Control Node (smartagentctl) ──▶ SSH Connection               │
│                                          │                       │
│                                          ├──▶ Host 1 (SSH)      │
│                                          ├──▶ Host 2 (SSH)      │
│                                          ├──▶ Host 3 (SSH)      │
│                                          └──▶ Host N (SSH)      │
│                                                                  │
│  All hosts send metrics ──▶ AppDynamics Controller             │
└─────────────────────────────────────────────────────────────────┘
```

## Workshop Components

This workshop includes:

1. **Prerequisites** - Required access, tools, and permissions
2. **Configuration** - Setting up `config.ini` and `remote.yaml`
3. **Installation & Startup** - Deploying and starting Smart Agent on remote hosts
4. **Troubleshooting** - Common issues and solutions

## Prerequisites

- Control node with smartagentctl installed
- SSH access to all remote hosts
- SSH private key configured for authentication
- Sudo privileges on the control node
- Remote hosts with SSH enabled
- AppDynamics account credentials

## Available Commands

The `smartagentctl` tool supports the following remote operations:

- `start --remote` - Install and start Smart Agent on remote hosts
- `stop --remote` - Stop Smart Agent on remote hosts
- `status --remote` - Check Smart Agent status on remote hosts
- `install --remote` - Install Smart Agent without starting
- `uninstall --remote` - Remove Smart Agent from remote hosts
- `--service` flag - Install as systemd service

All commands support the `--verbose` flag for detailed logging.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
The easiest way to navigate through this workshop is by using:

* the left/right arrows (**<** | **>**) on the top right of this page
* the left (◀️) and right (▶️) cursor keys on your keyboard
{{% /notice %}}
