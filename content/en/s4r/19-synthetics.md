---
title: 19. Synthetics
weight: 40
---

## Use the Splunk Observability Suite to check the perfomance of your Website/API Endpoint

So far we have have tested the perfomance of our Website by visting and running manual testscenario's to see how our web site perfomed.

But that will not work in production, and the more licly way you get informed is by social media 

![Instagram](../images/cb-instagram-post.png?width=50vw)

if we didn't have to wait for that, and could instead test the frontend whenever we want, in both production and pre-production? This is where Synthetics comes in.

![Synthetics overview](../images/SyntheticTests.png?width=50vw)

As part of this excersise we will clone an exsting Synthetic Test and  configure it to test against your website, and have it run automaticly. as part of this excercise we will also set up a detector that will will allow you to be automaticly informed/alerted if the perfomance of your webite is suboptimal.
