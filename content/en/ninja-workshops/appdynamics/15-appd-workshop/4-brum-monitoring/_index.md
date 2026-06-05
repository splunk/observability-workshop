---
title: Browser Real User Monitoring (BRUM)
time: 2 minutes
weight: 4
description: In this Learning Lab you learn how to use AppDynamics to monitor the health of your browser-based application.
---

## Objectives 
In this Learning Lab you learn how to use AppDynamics to monitor the health of your browser-based application.

When you have completed this lab, you will be able to:

- Create a browser application in the Controller
- Configure the Browser Real User Monitoring (BRUM) agent to monitor your web application’s health.
- Troubleshoot performance issues and find the root cause, whether it occurs on the browser side or the server side of the transaction.


## Workshop Environment

The workshop environment has two hosts:

- The first host runs the AppDynamics Controller and will be referred to from this point on as the Controller.
- The second host runs the Supercar Trader application used in the labs. It will be the host where you will install the AppDynamics agents and will be referred to from this point on as the Application VM.

## Controller
You will be using the [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) for this workshop.

![Controller](images/controller-vm.png)


## Application VM
Supercar Trader is a Java-based Web Application

The purpose of Supercar-Trader collection is to generate dynamic traffic (business transactions) for AppDynamics Controller.

![Application VM](images/application-vm.png)

