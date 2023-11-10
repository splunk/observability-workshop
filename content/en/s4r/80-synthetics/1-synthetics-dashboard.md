---
title: 1. Synthetics Dashboard
weight: 1
---

1. Goto Synthetics
2. Your instructor will highlight which Synthetic test to use
3. Click on the test
4. Note: be aware of screenshot for this step
5. Change to last hour

So far we have tested the performance of our Website by visiting and running manual test scenarios to see how our website performed.  
However, this is not something you can/want to do 24 hours a day, 7 days a week!

However, if you are not constantly testing your website performance & behaviour in production, the likely source telling you that your site is slow or not performant would be via Social Media or Down Detector.

![social media](../images/social-media-post.png?width=40vw)

So, what if, we didn't have to do it manually and could avoid waiting on your customers/users to let you know the behaviour of your site and could instead test the front-end whenever we wanted, in both production and pre-production?

This is where Splunk Synthetics comes in.

Synthetics (a part of the Splunk Observability Cloud offering) acts like a set of "Robot" users that run a different test against your sites, from various locations across the globe and allow you to set up Detectors that warn you if the behaviour of your site(s) changes.

Lets find the the provisioned Browser test in the Synthetics page of as part of this exercise we will also set up a detector that will allow you to be automatically informed/alerted if the performance of your website is suboptimal.

Change to your browser tab with the recently failed test run containing long POST checkout request

![Synthetics test run details](../images/test-run.png?width=50vw)

Synthetics can test uptime and APIs, but in this example let's look at a browser test, where we are emulating real user behaviour of shopping and checking out on the desktop site for my retail application.

We see the details of this test run, what the front end looks like visually, as well as a waterfall of all requests broken down by URL. Because this is a Synthetic test, we can define the test frequency, device type, and locations, as well as the critical user transactions that we want to track.

Click the last Transaction or Page tab, scroll through the filmstrip to show the images, and scroll down to the long checkout request

![Checkout requests](../images/failed-run-example.png?width=50vw)

We see that this test run failed because it never got to confirm the Order ID. Looking at the requests in the checkout, we see a long POST request to checkout with an APM link. Familiar, right?

Click the APM link on the long POST checkout request

![Checkout requests](../images/syn-apm.png?width=50vw)

Now if we follow the APM link as we did before in RUM, we see the same issue with an error in the payment service requests, and can follow the same workflow to investigate the issue.