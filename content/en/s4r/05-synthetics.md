---
title: Splunk Synthetics
weight: 40
---

## Use the Splunk Observability Suite to check the perfomance of your Website/API Endpoint

So far we have have tested the perfomance of our Website by visting and running manual testscenario's to see how our web site perfomed.

But what if we didn't have to wait for that, and could instead test the frontend whenever we want, in both production and pre-production? This is where Synthetics comes in.

![Synthetics overview](../images/SyntheticTests.png?width=50vw)

As part of this excersise we will clone an exsting Synthetic Test and  configure it to test against your website, and have it run automaticly. as part of this excercise we will also set up a detector that will will allow you to be automaticly informed/alerted if the perfomance of your webite is suboptimal.

Change to your browser tab with the recently failed test run containing long POST checkout request

![Synthetics test run details](../images/test-run.png?width=50vw)

Synthetics can test uptime and APIs, but in this example let's look at a browser test, where we are emulating real user behavior of shopping and checking out on the desktop site for my retail application.

We see the details of this test run, what the front end looks like visually, as well as a waterfall of all requests broken down by URL. Because this is a Synthetic test, we can define the test frequency, device type, and locations, as well as the critical user transactions that we want to track.

Click the last Transaction or Page tab, scroll through the filmstrip to show the images, and scroll down to the long checkout request

![Checkout requests](../images/failed-run-example.png?width=50vw)

We see that this test run failed because it never got to confirm the Order ID. Looking at the requests in the checkout, we see a long POST request to checkout with an APM link. Familiar, right?

Click the APM link on the long POST checkout request

![Checkout requests](../images/syn-apm.png?width=50vw)

Now if we follow the APM link as we did before in RUM, we see the same issue with an error in the payment service requests, and can follow the same workflow to investigate the issue.
