---
title: Why use Synthetics
weight: 10
---
{{% button icon="clock" %}}5 minutes{{% /button %}}

So far we have have tested the performance of our Website by visiting and running manual test scenarios to see how our web site performed.  
However, this is not something you can/want to do 24 hours a day, 7 days a week!

However, if you are not constantly testing your website performance & behaviour in production, the likely source telling you that your site is slow or not performant would be via Social Media or Down Detector.

![social media](../images/social-media-post.png?width=40vw)

So, what if, we didn't have to do it manually and can avoid waiting on your customers/users to let you know the behaviour of your site and could instead test the frontend whenever we wanted, in both production and pre-production?

This is where Splunk Synthetics comes in.

Synthetics (a part of the Splunk Observability Cloud offering) acts like a set of "Robot" users that run different test against your sites, from various locations across the globe and allows you to set up Detectors that warn you if the behaviour of your site(s) changes.

Let's move on and look at the UI and create our own test.
