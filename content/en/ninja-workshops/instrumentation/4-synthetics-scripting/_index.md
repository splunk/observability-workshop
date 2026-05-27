---
title: Splunk Synthetic Scripting
description: Proactively find and fix performance issues across user flows, business transactions and APIs to deliver better digital experiences.
weight: 4
authors: ["Robert Castley"]
time: 45 minutes
aliases:
  - /ninja-workshops/4-synthetics-scripting/
---

Proactively monitor the performance of your web app before problems affect your users. With **Splunk Synthetic Monitoring**, technical and business teams create detailed tests to proactively monitor the speed and reliability of websites, web apps, and resources over time, at any stage in the development cycle.

**Splunk Synthetic Monitoring** offers the most comprehensive and in-depth capabilities for uptime and web performance optimization as part of the only complete observability suite, Splunk Observability Cloud.

Easily set up monitoring for APIs, service endpoints and end-user experience. With **Splunk Synthetic Monitoring**, go beyond basic uptime and performance monitoring and focus on proactively finding and fixing issues, optimizing web performance, and ensuring customers get the best user experience.

With **Splunk Synthetic Monitoring** you can:

- Detect and resolve issues fast across critical user flows, business transactions and API endpoints
- Prevent web performance issues from affecting customers with an intelligent web optimization engine
- And improve the performance of all page resources and third-party dependencies

## What you'll build in this workshop

This workshop is split into two complementary parts that mirror how teams actually adopt Splunk Synthetic Monitoring in production:

- **Part 1 — Real Browser Test.** You'll use the [**Chrome DevTools Recorder**](https://developer.chrome.com/docs/devtools/recorder/) to capture a real user journey through a demo Online Boutique storefront — browsing a product, adding it to the cart, placing an order. You'll export that journey as JSON, import it into Splunk Synthetic Monitoring, schedule it to run from multiple global locations, and learn how to read the resulting performance data.
- **Part 2 — API Test.** You'll build a multi-step API check against the Spotify Web API: authenticate using OAuth 2 client credentials, chain the resulting bearer token into a search request, and validate the response. This is the same pattern you'd use to monitor your own backend SLOs end to end.

By the end of the 45 minutes you should be comfortable creating, configuring, and interpreting both check types — and you'll know when to reach for which.

## Prerequisites

- Google Chrome installed locally (for the recorder portion).
- Access to a Splunk Observability Cloud organisation with the **Synthetics** tab enabled.
- Approximately 45 minutes; tests will keep running in the background after the workshop ends, so leave them in place if you'd like to watch trends accumulate.

> Synthetic Monitoring also offers a third check type — **Uptime Tests** — for lightweight port and HTTP availability checks. We won't build one in this workshop, but you'll see it referenced in the UI; the [Uptime test documentation](https://docs.splunk.com/Observability/synthetics/uptime-test/uptime-test.html) is a good follow-on read.
