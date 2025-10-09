---
title: Enable Analytics on the Application
time: 2 minutes
weight: 2
description: In this exercise you will access your AppDynamics Controller from your web browser and enable the Agentless Analytics from there.

---

Analytics formerly required a separate agent that was bundled with Machine Agent. However, Analytics is now agentless and embedded in the APM Agent for both .NET Agent >= 20.10 and Java Agent >= 4.5.15 on Controllers >= 4.5.16

In this exercise you will access your AppDynamics Controller from your web browser and enable the Agentless Analytics from there.

## Login to the Controller
Log into the [AppDynamics SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) using your Cisco credentials.

## Navigate to the Analytics Configuration

1. ** Select the **Analytics** tab at the top left of the screen.
2. ** Select the **Configuration** Left tab.
3. ** Select the **Transaction Analytics - Configuration** tab.
4. ** **Mark the Checkbox** next to Your Application **Supercat-Trader-YOURINITIALS**
5. ** Click the **Save** button

![Enable Analytics](images/05-biq-transaction-analytics.png)


## Validate Transaction Summary

You want to verify that Analytics is working for that application and showing transactions.

1.  Select the **Analytics tab** tab on the left menu.
2.  Select the **Home** tab.
3.  Under **Transactions from** filter to your application **Supercar-Trader-YOURINITIALS**

![Validate Analytics](images/05-biq-transaction-analytics.png)
