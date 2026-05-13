---
title: Create Tests
linkTitle: 4.3 Create Tests
weight: 1
time: 10 minutes
description: Create Tests
---

## Summary

Now we will create tests to demonstrate this integration.

We will create two tests:
* A test from the ThousandEyes agent (inside the cluster); this would be useful if your application was not acceesible from the public internet
* A test from the public internet, using the public URL

### Step 1: HTTP Test (In Kubernetes Cluster)

1. In ThousandEyes, go to **Network & App Synthetics > Test Settings**.
2. Click **Add New Test** and choose **HTTP Server**.
3. Configure the test:
- **URL**: `http://api-gateway.default.svc.cluster.local:82/`
- **Test Name**: `[Name] Frontend Available (In Cluster)`
- **How often test runs**: 10 minutes
- **Agents**: Select the `Enterprise Agents` tab and select the agent you deployed earlier in this guide
- **Enable distributed tracing**: Enable
- **Verify Content**: Optional, use `PetClinic` if you want to validate the returned page content.
4. **Deploy** the test.
5. Click to **Check out test results**



### Step 2: API Test (In Kubernetes Cluster)

1. In ThousandEyes, go to **Network & App Synthetics > Test Settings**.
2. Click **Add New Test** and choose **API**.
3. Configure the test:
- **URL**: `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`
- **Test Name**: `[Name] Trace (In Cluster)`
- **How often test runs**: 30 minutes
- **Agents**: Select the `Enterprise Agents` tab and select the agent you deployed earlier in this guide
- **Enable distributed tracing**: Enable
![Distributed Testing check](../../images/test-distributed-tracing.png?width=45vw)
4. Click **Next**
5. Configure this page
- **Step Name**: Get Owners
- **Request URL**: `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`
6. **Deploy** the test.
7. Click to **Check out test results**
8. Click the **Service Map** tab

It may a little time but eventually the trace should show up. You can switch tabs a few times until the map shows up:

![ThousandEyes APM Service Map](../../images/apm-thousandeyes-map.png?width=45vw)

You can also click the link to the trace to see this in Splunk APM:

ADD IMAGE HERE

### Step 3: HTTP Test (Public)
1. In ThousandEyes, go to **Network & App Synthetics > Test Settings**.
2. Click **Add New Test** and choose **HTTP Server**.
3. Configure the test:
- **URL**: `http://i-069315f8160418ec0.splunk.show:81/#!/owners`
- **Test Name**: `[Name] Trace (public)`
- **How often test runs**: 10 minutes
- **Agents**: Select the `Cloud Agents` tab and select any agent
- **Enable distributed tracing**: Enable
4. **Deploy** the test.
5. Click to **Check out test results**
