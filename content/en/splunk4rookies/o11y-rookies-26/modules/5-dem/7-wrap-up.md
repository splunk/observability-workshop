---
title: Wrap-up
linkTitle: 7. Wrap-up
weight: 7
time: 1 minute
---

## What we accomplished

1. **Used RUM to choose a target** — Core Web Vitals, per-page comparison, and front-end health, to pick the one journey worth monitoring around the clock
2. **Built a Synthetics browser test** with named steps and two synthetic transactions covering that journey
3. **Validated and ran it on demand**, and read uptime, availability, and transaction-level results
4. **Activated a detector** on the uptime metric, then watched it fire on a failing checkout
5. **Added an uptime test** and met the other test types, including SSL certificate tests
6. **Reviewed a combined dashboard** pairing lab measurements with real customer experience

## The habit worth taking away

Our checkout test asserts that an order was confirmed, not that a button was clickable. That single design choice is what turns a monitoring setup from decorative into useful. Everything else on this page is mechanics.

## Connecting signals to business outcomes

| Signal | What the business calls it |
|---|---|
| Synthetic uptime on a revenue journey | Lost orders per minute of downtime |
| Synthetic transaction duration | Conversion rate and cart abandonment |
| Core Web Vitals | Search ranking, bounce rate, customer satisfaction |
| Time from failure to alert | Mean time to detect, and whether we or our customer notices first |

{{< checkpoint "Congratulations, you have completed **Beat social media to the issue**. You can now find the journeys that matter in RUM, build and alert on your own Synthetics tests, and put both signals in one view." >}}

## What's next

- **Add a transaction-level detector.** Hold the `Checkout` transaction to its own duration SLA, scoped with the `transaction` dimension, so we alert on *slow* as well as *broken*.
- **Try comparative testing.** Clone a test, change exactly one variable — exclude a heavy resource, set a different device, add a header — and chart both versions side by side. This is how we build evidence for a performance change rather than an opinion. See [Using comparative testing to drive app performance](https://lantern.splunk.com/Observability_Use_Cases/Understand_Journeys/Using_comparative_testing_to_drive_app_performance).
- **Record instead of hand-building.** For long journeys, capture the flow with the Google Chrome DevTools Recorder and import the JSON, then rename the steps and group them into transactions.
- **Cover our certificates.** An SSL test with a 30-day expiry detector on every public hostname is the cheapest outage prevention available.
- **Test something of our own.** Sign up for the [Free Edition of Splunk Observability Cloud](https://www.splunk.com/en_us/download/observability-cloud-free-edition.html), point an uptime test at a URL our team owns, and keep it running.

## Documentation

- [Introduction to Splunk Synthetic Monitoring](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring)
- [Set up a browser test](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/browser-tests-for-webpages/set-up-a-browser-test)
- [Detectors and alerts](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/advanced-test-configurations/detectors-and-alerts)
- [Splunk RUM metrics reference](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/real-user-monitoring/splunk-rum-metrics-reference)
- [Running Synthetic browser tests](https://lantern.splunk.com/Observability_Use_Cases/Understand_Journeys/Running_Synthetic_browser_tests) on Splunk Lantern

{{< pager prev="/en/splunk4rookies/o11y-rookies-26/modules/" prevLabel="Back to Lessons" >}}
