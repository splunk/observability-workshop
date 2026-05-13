---
title: Create Tests
linkTitle: 4.3 Create Tests
weight: 1
time: 10 minutes
description: Create Tests
---

## Summary

Now we will create tests to demonstrate this integration.

We will create three tests:
* A test from the ThousandEyes agent (inside the cluster); this would be useful if your application was not acceesible from the public internet
* A more interesting trace (inside the cluster)
* A test from the public internet, using the public URL and with a ThousandEyes Cloud Agent

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
![ThousandEyes Script Settings](../../images/test-distributed-tracing.png?width=20vw)
4. Click **Instant Test**
6. Switch to the **Service Map** tab

It may take a little time for the service map view to show up in ThousandEyes, but you should be able to find the trace in Splunk Observability Cloud

7. Copy the trace
8. In Splunk Observability Cloud, navigate to **APM > Trace Analyzer**, paste in the trace, and **Go**

Ultimately you should see something like the following:

![Test 1 - ThousandEyes](../../images/test1-te.png?width=35vw)

![Test 1 - APM](../../images/test1-apm.png?width=35vw)

### Step 2: HTTP Test (In Kubernetes Cluster) - More interesting trace
Now let's repeat step 1, but using the url: `http://api-gateway.default.svc.cluster.local:82/api/customer/owners` (Owners List).

You can edit the same test you made, and run an instant test.

You should get more interesting maps.
![Test 2 - ThousandEyes](../../images/test2-te.png?width=35vw)

![Test 2 - APM](../../images/test2-apm.png?width=35vw)

{{% notice title="ThousandEyes Failure" style="note" %}}
Notice my test in ThousandEyes failed? That's because I didn't change the **Verify Content** based on the Owners List.
![Test 2 - ThousandEyes Verify Content Failure](../../images/test2-te-fail.png?width=20vw)
{{% /notice %}}

### Step 3: HTTP Test (Public)

Finally let's see if we can hit this page from the public.

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


