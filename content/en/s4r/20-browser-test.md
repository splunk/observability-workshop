---
title: 20. Browser test
weight: 41
---

{{% notice style="grey" title="Change to your browser tab with the recently failed test run containing long POST checkout request" %}}
![Synthetics test run details](../img/test-run.png?width=50vw)

{{% /notice %}}

{{% notice style="blue" title="Say" icon="user" %}}
Synthetics can test uptime and APIs, but in this example let's look at a browser test, where we are emulating real user behavior of shopping and checking out on the desktop site for my retail application.

We see the details of this test run, what the front end looks like visually, as well as a waterfall of all requests broken down by URL. Because this is a Synthetic test, we can define the test frequency, device type, and locations, as well as the critical user transactions that we want to track.
{{% /notice %}}