---
title: And introduction to
linkTitle: Intro to Synthetics

weight: 10
---
{{% button icon="clock" %}}15 minutes{{% /button %}}

## Why use Splunk Synthetics

So far we have have tested the performance of our Website by visiting and running manual test scenarios to see how our web site performed. However, this is not something you can do 24 hours a day, 7 days a week!

If you were not testing your website performance and behavior manually in production the likely source telling you that your site is slow or not performant would be Social Media or Down Detector.

![social media](../images/social-media-post.png?width=40vw)

But, what if we didn't have to do it manually and avoid waiting on your customers/users to let you know the behavior of your site and could instead test the frontend whenever we wanted, in both production and pre-production?

This is where Splunk Synthetics comes in.

![Synthetics overview](../images/synthetic-tests.png?width=40vw)

As the image above tries to shows, Synthetics (a part of the Splunk Observability Cloud offering) acts like a set of "Robot" users to run different test against your sites, from various locations and allows you to set up Detectors that warn you if the behavior of your site(s) changes.

Let's move on and look at the UI and create  our own test.
