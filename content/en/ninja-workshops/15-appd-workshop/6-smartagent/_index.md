---
title: SmartAgent Deployment
weight: 6
time: 2 minutes
description: Learn multiple approaches to deploy and manage AppDynamics Smart Agent at scale across your infrastructure.
---

## Introduction

AppDynamics **Smart Agent** is a lightweight, intelligent agent that provides comprehensive monitoring capabilities for your infrastructure. This section covers three different deployment approaches, allowing you to choose the method that best fits your organization's needs and existing tooling.

![AppDynamics](https://img.shields.io/badge/AppDynamics-0078D4?style=flat)

## What is Smart Agent?

Smart Agent is AppDynamics' next-generation monitoring agent that provides:

- **Unified Monitoring**: Single agent for infrastructure, applications, and services
- **Lightweight Design**: Minimal resource footprint
- **Auto-Discovery**: Automatically discovers and monitors applications
- **Native Instrumentation**: Deep visibility into application performance
- **Flexible Deployment**: Multiple installation and management options

## Deployment Approaches

This section covers three distinct approaches to deploying Smart Agent at scale:

### 1. Remote Installation (smartagentctl)

The most direct approach using the `smartagentctl` CLI tool to deploy via SSH.

**Best for:**
- Quick deployments to a moderate number of hosts
- Environments without existing CI/CD infrastructure
- Testing and proof-of-concept scenarios
- Direct control over deployment process

**Key Features:**
- Direct SSH-based deployment
- Simple YAML configuration
- No additional tooling required
- Concurrent execution support

### 2. Jenkins Automation

Enterprise-grade deployment using Jenkins pipelines for complete lifecycle management.

**Best for:**
- Organizations already using Jenkins
- Complex deployment workflows
- Environments requiring approval gates
- Integration with existing CI/CD pipelines

**Key Features:**
- Parameterized pipelines
- Batch processing for thousands of hosts
- Complete lifecycle management
- Centralized logging and reporting

### 3. GitHub Actions Automation

Modern CI/CD approach using GitHub Actions workflows with self-hosted runners.

**Best for:**
- Teams using GitHub for version control
- Cloud-native environments
- GitOps workflows
- Distributed teams preferring web-based management

**Key Features:**
- 11 specialized workflows
- Self-hosted runner in your VPC
- GitHub secrets integration
- Automatic batching for scalability

## Choosing the Right Approach

| Factor | Remote Installation | Jenkins | GitHub Actions |
|--------|-------------------|---------|----------------|
| **Setup Complexity** | Low | Medium | Medium |
| **Scalability** | Good (100s of hosts) | Excellent (1000s) | Excellent (1000s) |
| **Prerequisites** | SSH access only | Jenkins server | GitHub account |
| **Learning Curve** | Minimal | Moderate | Moderate |
| **Automation Level** | Manual execution | Full automation | Full automation |
| **Best Use Case** | Quick deployments | Enterprise CI/CD | Modern DevOps |

## Common Features Across All Approaches

Regardless of which deployment method you choose, all approaches provide:

- ✅ **SSH-based deployment** to remote hosts
- ✅ **Concurrent execution** for faster deployment
- ✅ **Complete lifecycle management** (install, start, stop, uninstall)
- ✅ **Configuration management** for controller settings
- ✅ **Error handling** and logging
- ✅ **Scalability** to hundreds or thousands of hosts

## Workshop Structure

Each deployment approach has its own dedicated section:

1. **Remote Installation** - Direct CLI-based deployment
2. **Jenkins Automation** - Pipeline-based enterprise deployment
3. **GitHub Actions** - Modern workflow-based deployment

You can follow one or all approaches depending on your needs.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If you're new to Smart Agent deployment, we recommend starting with the **Remote Installation** approach to understand the basics before moving to more automated solutions.
{{% /notice %}}

## Prerequisites

Before proceeding with any deployment approach, ensure you have:

- AppDynamics account with controller access
- Account name and access key
- Target hosts with SSH access
- Network connectivity from hosts to AppDynamics Controller
- Appropriate permissions on target hosts

## Next Steps

Choose your preferred deployment approach and proceed to that section:

- **Start Simple**: Begin with Remote Installation to learn the fundamentals
- **Scale with Jenkins**: Move to Jenkins for enterprise-grade automation
- **Modernize with GitHub**: Adopt GitHub Actions for cloud-native workflows

Each section provides complete, hands-on guidance for deploying Smart Agent at scale!
