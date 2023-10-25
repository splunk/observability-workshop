---
title: Our first Synthetic test
linkTitle: Create Your own test
description: This section of the workshop will equip you with the basic understanding of the SyntheticsUI
weight: 30
---
We are now going to setup a browser test that will provide you continuous insight in the behavior of your website. As part of this exercise we will clone an existing Synthetic Test and configure it to test against your website, and have it run automatically.

Lets find the the provisioned Browser test in the Synthetics page of as part of this exercise we will also set up a detector that will will allow you to be automatically informed/alerted if the performance of your website is suboptimal.

Change to your browser tab with the recently failed test run containing long POST checkout request

![Synthetics test run details](../images/test-run.png?width=50vw)

Synthetics can test uptime and APIs, but in this example let's look at a browser test, where we are emulating real user behavior of shopping and checking out on the desktop site for my retail application.

We see the details of this test run, what the front end looks like visually, as well as a waterfall of all requests broken down by URL. Because this is a Synthetic test, we can define the test frequency, device type, and locations, as well as the critical user transactions that we want to track.

Click the last Transaction or Page tab, scroll through the filmstrip to show the images, and scroll down to the long checkout request

![Checkout requests](../../images/failed-run-example.png?width=50vw)

We see that this test run failed because it never got to confirm the Order ID. Looking at the requests in the checkout, we see a long POST request to checkout with an APM link. Familiar, right?

Click the APM link on the long POST checkout request

![Checkout requests](../../images/syn-apm.png?width=50vw)

Now if we follow the APM link as we did before in RUM, we see the same issue with an error in the payment service requests, and can follow the same workflow to investigate the issue.

