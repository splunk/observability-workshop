---
title: Why use Synthetics
weight: 10
---
{{% button icon="clock" %}}5 minutes{{% /button %}}

1. Goto Synthetics
2. Your instructor will highlight which Synthetic test to use
3. Click on the test
4. Note: be aware of screenshot for this step
5. Change to last hour
6. Deep dive into a datapoint must be successful and long run duration
7. Walk through, screenshots, video and highlight Synthetic vs RUM Web Vitals, Business Transactions, Waterfall, etc.
8. 5 steps/business trans
9. We know there is an issue placing orders, so click on place Order
10. Find POST checkout and click APM link
11. You are in an APM trace view
12. Validate you see errors
13. Click on related content log link
14. Repeat the exercise to filter down to errors only
15. View the error log to validate the failed payment due to invalid Token.
16. Go back to Synthetics and select the test again and click create detector
17. Ensure Run Duration is selected and static threshold
18. Set trigger threshold to be 30000ms, leave the rest as default
19. Click Activate
20. Let's go back to our War Room dashboard

So far we have tested the performance of our Website by visiting and running manual test scenarios to see how our website performed.  
However, this is not something you can/want to do 24 hours a day, 7 days a week!

However, if you are not constantly testing your website performance & behaviour in production, the likely source telling you that your site is slow or not performant would be via Social Media or Down Detector.

![social media](../images/social-media-post.png?width=40vw)

So, what if, we didn't have to do it manually and could avoid waiting on your customers/users to let you know the behaviour of your site and could instead test the front-end whenever we wanted, in both production and pre-production?

This is where Splunk Synthetics comes in.

Synthetics (a part of the Splunk Observability Cloud offering) acts like a set of "Robot" users that run a different test against your sites, from various locations across the globe and allow you to set up Detectors that warn you if the behaviour of your site(s) changes.

Let's move on and look at the UI and create our test.
