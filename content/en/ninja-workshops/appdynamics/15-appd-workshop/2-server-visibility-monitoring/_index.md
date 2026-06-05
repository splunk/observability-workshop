---
title: Server Visibility Monitoring
time: 2 minutes
weight: 2
description: In this Lab you learn about AppDynamics Server Visibility Monitoring and Service Availability Monitoring.
---

{{% notice title="Prerequsites" style="primary"  icon="lightbulb" %}}
This is a continuation of the Application Performance Monitoring lab. Verify that your application is running and has load for the past hour. If needed return to the Generate Application Load section to restart the load generator. 
{{% /notice %}}

## Objectives 
In this Lab you will learn about AppDynamics Server Visibility Monitoring and Service Availability Monitoring.

When you have completed this lab, you will be able to:

- Download the AppDynamics Server Visibility Agent.
- Install the AppDynamics Server Visibility Agent.
- Monitor server health.
- Understand the agent’s extended hardware metrics.
- Quickly see underlying infrastructure issues impacting your application performance.

## Workshop Environment
The lab environment has two hosts:

- The first host runs the AppDynamics Controller and will be referred to from this point on as the Controller.
- The second host runs the Supercar Trader application used in the labs. It will be the host where you will install the AppDynamics agents and will be referred to from this point on as the Application VM.

## Controller
You will be using the [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) for this workshop.

![Controller](images/controller-vm.png)


## Application VM
Supercar Trader is a Java-based Web Application

The purpose of Supercar-Trader collection is to generate dynamic traffic (business transactions) for AppDynamics Controller.

![Application VM](images/application-vm.png)