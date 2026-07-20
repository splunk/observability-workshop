---
title: 1.4 Settings
weight: 4
---

Every setting on this page maps directly to a real-world tradeoff between coverage, cost, signal quality, and load on the system you're monitoring. Before clicking through, here's what each control actually controls and the rule of thumb for choosing a value.

## Name

The display name for the test — used everywhere in the UI, in alert messages, in linked dashboards, and in detector titles. Bake context into it: include the service name, the journey, and (in shared organisations) your initials. **`<your initials>` - Online Boutique** works well for this workshop.

## Locations

The cloud regions Splunk runs the test from. There are over 50 to choose from, spread across all the major AWS regions. **Location choice matters more than people expect** because the metric you get back is the *measured* user experience from that location — network latency, TLS handshake time, and any geographic CDN routing are all baked in. A site that loads in 800 ms from N. Virginia might take 2.4 s from Mumbai if your CDN doesn't cache there.

Best practice: pick locations that match where your real users live. If you have a US-east customer base and a separate EMEA customer base, monitor from both — and add at least one location that's *far* from any user (e.g. Melbourne for a US-only product) as an early-warning canary for global routing or DNS issues.

For this workshop we'll use three locations spanning three continents:

- **AWS - N. Virginia**
- **AWS - London**
- **AWS - Melbourne**

Click in the **Locations** field and select each from the dropdown.

![Global Locations](../../img/global-locations.png)

## Device

Emulates a specific device profile, which sets the viewport dimensions, user agent string, and a *throttled* CPU and network profile that approximates that device. The viewport stays consistent regardless of which location the test runs from.

Why this matters: a fast-3G-throttled iPhone X with 4× CPU slowdown will surface real-user pain that an unthrottled desktop test would mask entirely. If your users are mostly on mobile, monitor on mobile.

## Frequency

How often the test runs from each location. The shorter the interval, the faster you'll catch a regression — but the more capacity you'll burn through and the more load you'll apply to the target site. Pick the lowest frequency that still gives your detectors a useful signal:

| Frequency | Typical use |
| --- | --- |
| 1 min | Critical user journeys for high-traffic, high-revenue sites |
| 5 min | Default for most production journeys (this workshop's setting) |
| 10–15 min | Pre-prod, staging, lower-priority flows |
| 30–60 min | Marketing pages, low-change static content |

Remember the alert math: a 5-minute frequency means it can take **up to 5 minutes** to *first* detect a regression, and most detectors require 2–3 consecutive failures to fire — so a 5-minute test may not alert for 10–15 minutes after an incident begins.

## Round-robin

If you've selected multiple locations, **round-robin** changes how they're scheduled. Off (the default) means all selected locations run on every interval — three locations × every 5 minutes = 36 runs/hour. On means Splunk rotates through the locations, running one per interval — three locations × every 5 minutes = 12 runs/hour, but each individual location is now only sampled every 15 minutes.

The tradeoff: round-robin slashes your run consumption and applies less load to the target, but dilutes per-location signal (so location-specific regressions are slower to surface). Leave it off for this workshop.

## Active

Toggles the test on or off. Leave it on. You can disable it later from the test list if you no longer want the run history accumulating.

---

Once you've set the name and selected the three locations, scroll down and click {{% button style="blue" %}}Submit{{% /button %}} to save the test.

The test is now scheduled to run every 5 minutes from N. Virginia, London, and Melbourne. The first run usually takes a couple of minutes to dispatch — the scheduler has to allocate a browser slot in each region — so don't worry if you don't see results immediately.

While we wait, click on {{% button %}}Edit test{{% /button %}} so we can take a look at the **Advanced** settings.
