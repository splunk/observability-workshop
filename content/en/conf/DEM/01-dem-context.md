---
title: Understanding DEM
linkTitle: Context
description: What are RUM and Synthetics?
weight: 1
---

DEM = Digital Experience Monitoring: 

What are your end users doing? 

Do you know how they're interacting with your app, what the performance is, what errors are occuring, and why? 

How do your third party services impact the end user?

When do you find out about user-impacting issues - how fast are they addressed, and how does this affect your internal teams?

How does all of this affect your business?

---

Some examples of scenarios DEM can capture:

1. Slow page load due to large content size
1. Content jumping around the webpage
1. Spike in users abandoning their shopping cart
1. Unexpected dips or spikes in web traffic
1. Outages in third party providers that are blocking your users from submitting a form or making a payment
1. Javascript errors causing elements to not be clickable
1. A new release for iOS causes the mobile app to crash

## Real User Monitoring (RUM)
RUM captures **what real end users are experiencing in real time**, including where they are and what device and connection they are using. With no sampling, RUM captures all user sessions which helps not only understand trends in behavior and capture anomalies, but also helps with troubleshooting and replicating issues in production.

## Synthetics
Synthetics allows us to create controlled tests with specific configurations, to **proactively test performance** in both PROD and pre-PROD. This means we can test our first- and third-party services around the clock, without having to wait for real users to encounter an issue to capture it.