---
title: Beat social media to the issue
weight: 5
layout: chapter
time: 45 minutes
authors: ["Sarah Ware"]
description: Monitor real user experiences and set up proactive tests so you catch problems before your users complain online.
params:
  images:
    - images/rum.webp
---

{{< presenter >}}
Before the workshop begins:

* Open the *Astronomy Shop URL* provided for your workshop, append `/Feature`, and confirm **paymentFailure** is enabled at **50%** with the other demonstrations disabled. Roughly half of the checkout attempts must fail for this module to work.
* Confirm attendees can **create Synthetics tests and activate detectors** in the workshop org. This module has them save real tests.
* **Walk the browser test yourself once.** Build the test on page 2 exactly as written and run it. This confirms the `data-cy` selectors and the order confirmation wording still match the deployed build of the shop, and that the shop's certificate does not require turning off TLS/SSL validation. Give attendees any corrections up front — a wrong selector costs a beginner most of the module.
* Note the store's environment and application names so attendees can filter RUM on page 1, and confirm whether the combined dashboard on page 6 exists in this org.
* After the session, delete the attendee tests and detectors (search Synthetics for the workshop name). Every attendee leaves one browser test, one uptime test, and one detector behind.
{{< /presenter >}}

**Real User Monitoring (RUM)** tells us what our end users actually experienced. **Synthetic Monitoring** tells us what they *would* experience right now, whether or not anyone is using our app. Together, RUM and Synthetics help us get ahead of issues before we find out on socials.

{{< persona role="SRE" >}}
{{< persona-situation >}}You just finished cleaning up the Astronomy Shop `payment` service incident. The postmortem question landed on your desk: *how long would it have taken us to notice if nobody had complained?*{{< /persona-situation >}}
{{< persona-goal >}}Set up monitoring that notices a failing checkout before a customer does.{{< /persona-goal >}}
{{< /persona >}}

{{< webex chat="Shelly K." date="Today • 28/01/2026" seenby="SK" >}}
{{< webex-msg from="SK" name="Shelly K." time="14:10" >}}
Postmortem action item for us: a customer told us about the checkout failures before our monitoring did 😬 can you get proactive coverage on the checkout journey?
{{< /webex-msg >}}

{{< webex-msg me=true time="14:12" >}}
On it. I'll use RUM to figure out which journey matters most, then build a Synthetics browser test for it with an alert so we hear about it first next time. 👍
{{< /webex-msg >}}
{{< /webex >}}

> [!IMPORTANT]
> This module assumes you have completed the **Introduction** module, where you navigated the RUM Overview, used Tag Spotlight and User Sessions, and reviewed a *prebuilt* Synthetics browser test. Here you will build your **own** test and activate a real detector.

## Overview

In this hands-on module, we will:

- **See real user pain** in Web Vitals, per-page metrics, and custom workflows to choose the journey worth testing
- **Build a Synthetics browser test** for the checkout journey, with named steps and synthetic transactions
- **Test on demand** and interpret uptime, availability, and transaction-level results
- **Activate a detector** so a failing checkout pages you instead of surprising you
- **Check out the other test types** — uptime, port, API, and SSL certificate tests
- **Review a combined dashboard** that puts real user and synthetic signals side by side

{{% notice title="What you need" style="info" %}}
The Astronomy Shop URL for your workshop, and your Splunk Observability Cloud login. Your instructor will also give you the workshop name used to prefix test names.
{{% /notice %}}
