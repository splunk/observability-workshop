---
title: GitHub Actions Automation
weight: 3
time: 2 minutes
description: Learn how to automate AppDynamics Smart Agent deployment using GitHub Actions with self-hosted runners.
---

## Introduction

This workshop demonstrates how to use **GitHub Actions** with a self-hosted runner to automate the deployment and lifecycle management of **AppDynamics Smart Agent** across multiple EC2 instances. Whether you're managing 10 hosts or 10,000, this guide shows you how to leverage GitHub Actions workflows for scalable, secure, and repeatable Smart Agent operations.

![GitHub Actions and AppDynamics](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white) ![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## What You'll Learn

In this workshop, you'll learn how to:

- **Deploy Smart Agent** to multiple hosts using GitHub Actions workflows
- **Configure GitHub secrets and variables** for secure credentials management
- **Set up a self-hosted runner** in your AWS VPC
- **Implement automatic batching** to scale to thousands of hosts
- **Manage the complete agent lifecycle** - install, uninstall, stop, and cleanup
- **Monitor workflow execution** and troubleshoot issues

## Key Features

- 🚀 **Parallel Deployment** - Deploy to multiple hosts simultaneously
- 🔄 **Complete Lifecycle Management** - 11 workflows covering all agent operations
- 🏗️ **Infrastructure as Code** - All workflows version-controlled in GitHub
- 🔐 **Secure** - SSH keys stored as GitHub secrets, private VPC networking
- 📈 **Massively Scalable** - Deploy to thousands of hosts with automatic batching
- 🎛️ **Self-hosted Runner** - Executes within your AWS VPC

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  GitHub Actions-based Deployment                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Developer ──▶ GitHub.com ──▶ Self-hosted Runner (AWS VPC)     │
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

1. **Architecture & Design** - Understanding the GitHub Actions workflow architecture
2. **GitHub Setup** - Configuring secrets, variables, and self-hosted runners
3. **Workflow Creation** - Understanding and using the 11 available workflows
4. **Deployment Execution** - Running workflows and verifying installations

## Available Workflows

This solution includes **11 workflows** for complete Smart Agent lifecycle management:

| Category | Workflows | Description |
|----------|-----------|-------------|
| **Deployment** | 1 | Deploy and start Smart Agent |
| **Agent Installation** | 4 | Install Node, Machine, DB, and Java agents |
| **Agent Uninstallation** | 4 | Uninstall specific agent types |
| **Agent Management** | 2 | Stop/clean and complete cleanup |

All workflows support automatic batching for scalability!

## Prerequisites

- GitHub account with repository access
- AWS VPC with Ubuntu EC2 instances
- Self-hosted GitHub Actions runner in the same VPC
- SSH key pair for authentication
- AppDynamics Smart Agent package

## GitHub Repository

All workflow code and configuration files are available in the GitHub repository:

**[https://github.com/chambear2809/github-actions-lab](https://github.com/chambear2809/github-actions-lab)**

The repository includes:
- 11 complete workflow YAML files
- Detailed setup documentation
- Architecture diagrams
- Troubleshooting guides

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
The easiest way to navigate through this workshop is by using:

* the left/right arrows (**<** | **>**) on the top right of this page
* the left (◀️) and right (▶️) cursor keys on your keyboard
{{% /notice %}}
