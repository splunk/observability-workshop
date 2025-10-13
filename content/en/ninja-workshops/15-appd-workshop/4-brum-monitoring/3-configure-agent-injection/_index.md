---
title: Configure Agent Injection
time: 3 minutes
weight: 3
description: In this exercise you will enable JavaScript Injection and select BT for injection.
---

In this exercise you will complete the following tasks:

*   Enable JavaScript Agent injection.
*   Select Business Transactions for injection.

## Enable JavaScript Agent injection

While AppDynamics supports various methods for injecting the JavaScript Agent, you will be using the Auto-Injection method in this lab. Follow these steps to enable the Auto-Injection of the JavaScipt Agent.

1. Click the **Applications** tab on the left menu and drill into your Supercar-Trader-## application.
2. Click the **Configuration** tab on the left menu at the bottom.
3. Click the **User Experience App Integration** option.

![BRUM Dash 1](images/03-brum-app-integration.png)

4. Click the **JavaScript Agent Injection** tab.
5. Click **Enable** so that it turns blue.
6. Ensure that **Supercar-Trader-Web-##-####** is the selected browser app. Choose the application that you created in the previous section
7. Check the **Enable** check box under **Enable JavaScript Injection**
8. Click **Save**.

![BRUM Dash 2](images/03-brum-agent-injection.png)
  

It takes a few minutes for the Auto-Injection to discover potential Business Transactions. While this is happening, use these steps to enable the Business Transaction Correlation. For newer APM agents this is done automatically

9. Click the **Business Transaction Correlation** tab.
10. Click the **Enable** button under the **Manually Enable Business Transactions** section.
11. Click **Save**.

![BRUM Dash 3](images/03-brum-bt-manual.png)

## Select Business Transactions for injection

Use the following steps to select the Business Transactions for Auto-Injection.

1. Click the **JavaScript Agent Injection** tab.
2. Type **.do** in the search box.
3. Click the **Refresh List** link for the Business Transactions until all 9 BTs show up. 
4. Select all Business Transactions from the right list box.
5. Click the arrow button to move them to the left list box.
6. Ensure that all Business Transactions are moved into the left list box.
7. Click **Save**.

You can read more about configuring Automatic Injection of the JavaScript Agent [**here**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/inject-the-javascript-agent/automatic-injection-of-the-javascript-agent).

![BRUM Dash 5](images/03-brum-bts-auto-inject.png)

Wait a few minutes for load to start showing up in your Browser Application.  
