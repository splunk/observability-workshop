---
title: Run the test and read the results
linkTitle: 3. Run the test and read the results
weight: 3
time: 7 minutes
---

Our test now runs every five minutes, but we do not have to wait five minutes to see results. **Run now** triggers a scheduled-quality run on demand.

{{% exercise title="Trigger runs on demand" %}}

* On our test's page, select {{% button style="grey" %}}Run test now{{% /button %}}. We can also do this from the Synthetics test list, using the vertical dots **⋮** next to the test.
* Trigger **three or four** runs, waiting for each to finish before starting the next. Because roughly half of all checkouts fail, a handful of runs gives us a mix of passes and failures to look at.
* Runs triggered this way are labelled **Manual** in the results list, to distinguish them from the scheduled ones.

{{< notice >}}
Unlike **Try now**, these runs are stored and counted. They move our uptime numbers and they consume subscription usage, so on a production test we use them deliberately — typically to confirm that a fix worked rather than to satisfy curiosity. The limit is 100 on-demand runs per test per 10 minutes.
{{< /notice >}}

{{% /exercise %}}

## Read the test history

{{% exercise title="Interpret our own test" %}}

Stay on our test's page and work through it from the top.

* **Uptime trends** — the headline number. Uptime is the percentage of runs that did not fail, averaged across the window, so a 50% uptime means half our runs never produced an order.
* **Availability** — the same information over time and split by location. Look for whether failures cluster in one location (a regional problem) or appear everywhere (an application problem). Ours should fail everywhere, because the defect is in the `payment` service, not the network.
* **Performance KPIs** — a chart we can point at any of the 40-plus metrics a browser test collects. Change the metric selector and compare **Run duration** against **Largest contentful paint**.
* **Recent runs** — individual runs with location, duration, and result.

<!-- TODO screenshot: Browser test history page showing Uptime trends, Availability, and Performance KPIs -->
![Browser test history with uptime, availability, and performance KPIs](../images/synth-test-history.png)

{{< quiz question="Which of your seven steps fails, and is the failure in the click or in the assertion?" >}}
{{< quiz-option correct=true >}}Step 7, Order confirmed. The assertion fails. The click works.{{< /quiz-option >}}
{{< quiz-option >}}Step 6, Place the order. The click itself fails.{{< /quiz-option >}}
{{< quiz-option >}}Step 3, Open a product. The product card selector does not match.{{< /quiz-option >}}
{{< quiz-feedback >}}
Step 7, **Order confirmed**, fails, and it is the **assertion** that fails, not a click. The **Place the order** click works; the button is there and it responds. What never arrives is the order confirmation. A test that stopped at step 6 would report 100% uptime through a total checkout outage.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{< quiz question="Browse succeeds on every run while Checkout fails on about half. What does that tell you before you open a trace?" >}}
{{< quiz-option correct=true >}}The shop is healthy through add-to-cart. Only completing the purchase fails.{{< /quiz-option >}}
{{< quiz-option >}}The whole shop is down, including the home page.{{< /quiz-option >}}
{{< quiz-option >}}The failure is a network problem at one synthetic location.{{< /quiz-option >}}
{{< quiz-feedback >}}
The split localises the problem before you open APM. Everything up to and including adding an item to the cart is healthy, so the front end, the product catalog, and the cart are all fine. Only the act of completing a purchase fails.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

## The transaction payoff

This is where naming our transactions pays off.

{{% exercise title="Compare Browse against Checkout" %}}

* Open one of our failed runs and use the **Filter by a synthetic transaction, page, or step** control to switch between **Browse** and **Checkout**.
* Note that each transaction reports its own **duration**, **requests**, and **size**. A run-level duration would have averaged these together and hidden which half of the journey degraded.

{{< notice tip >}}
This is the level we should set an SLA at. "The checkout transaction completes in under 8 seconds" is a commitment a business understands and an engineer can act on. "The test run takes under 45 seconds" is neither, because it changes every time somebody adds a step.
{{< /notice >}}

{{% /exercise %}}

## Lab data next to real data

A synthetic run also collects **Web Vitals**, the same LCP, CLS, and INP we looked at in RUM on page 1 — plus **Total Blocking Time**, a lab stand-in for INP that synthetic runs can measure reliably because they control the interaction.

{{% exercise title="Cross over into real user data" %}}

* In a run's metrics panel, find the **Web Vitals** section. Each value is shown against its acceptable range.
* Select the flashlight {{% icon icon="search" %}} icon next to a Web Vital to open the matching sessions in **Tag Spotlight**.
* Check the **visits** count. We are now looking at how many *real users* and *synthetic runs* hit that same URL — our controlled measurement and our customers' actual experience, in one view.

{{% /exercise %}}

This is the pairing the whole module is building toward: synthetic runs give us a clean, repeatable, always-on measurement, and RUM tells us whether that measurement matches reality. We will see both on a single dashboard shortly.

Learn more in [Interpret browser test results](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/browser-tests-for-webpages/interpret-browser-test-results) and [Compare run results to Web Vitals with Splunk RUM](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/view-synthetic-tests/compare-run-results-to-web-vitals-with-splunk-rum).

Right now, though, our test knows checkout is broken and nobody else does. Time to fix that.
