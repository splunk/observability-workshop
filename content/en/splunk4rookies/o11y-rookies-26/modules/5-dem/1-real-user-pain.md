---
title: Which journey should we test?
linkTitle: 1. Which journey should we test?
weight: 1
time: 8 minutes
---

Before we start creating tests with Synthetics, let's look at what real users are doing to prioritize test coverage. RUM tells us which pages real end users interact with, how those pages feel, and where the experience breaks down.

{{% exercise title="Open our store and check the Web Vitals" %}}

* From the main menu, select **Digital Experience**, then **Overview** under **Real User Monitoring**.
* Set the filters to our own store:
  * **Time frame**: **-1h**
  * **Environment**: **[NAME OF WORKSHOP]-workshop**
  * **App**: **[NAME OF WORKSHOP]-store**
  * **Source**: **Browser**
* Select the **[NAME OF WORKSHOP]-store** link above the **Page Views / JavaScript Errors** chart to open the application view.
* On the **UX Metrics** tab, find the three **Core Web Vitals** charts.

<!-- TODO screenshot: RUM application view, UX Metrics tab, with the three Core Web Vitals charts visible -->
![Core Web Vitals in the RUM application view](../images/rum-web-vitals.png)

{{% /exercise %}}

## Reading Core Web Vitals

Core Web Vitals are Google's primary measures of front-end experience, and Google uses them for search ranking. 

| Web Vital | What it measures | Good | Needs improvement | Poor |
|---|---|---|---|---|
| **LCP** — Largest Contentful Paint | How quickly the main content appears | ≤ 2.5 s | 2.5 s – 4 s | > 4 s |
| **INP** — Interaction to Next Paint | How quickly the page reacts to a click or tap | ≤ 200 ms | 200 ms – 500 ms | > 500 ms |
| **CLS** — Cumulative Layout Shift | How much the layout jumps around while loading | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |

{{< notice tip >}}
LCP and INP answer *"is it fast and responsive?"*. CLS answers *"is it stable?"*; a high CLS is the page that loads an ad late into just where the user wanted to click, causing confusion, distraction, frustration, and distrust.
{{< /notice >}}

See [Core Web Vitals](https://web.dev/vitals/) for the full definitions and current thresholds.

{{% exercise title="Rank the pages, then check front-end health" %}}

* Select the **Pages** tab. This breaks the application down by page or URL group rather than treating the store as one blob.
* Sort by **Page Views** to see where our customers actually spend their time. In the Astronomy Shop the traffic concentrates on the home page, the `/product/...` detail pages, and `/cart`.
* Now compare the **performance and Web Vitals columns** across those same rows. A slow page nobody visits is a low priority; a slow page on the path to revenue is not.
* Select the **Front-end Health** tab and review:
  * **JavaScript errors** — broken code paths, grouped by error message and frequency.
  * **Long tasks** — single blocks of JavaScript that hold the main thread long enough that the page stops responding to input. Long tasks are usually what a customer means by "the site froze".

<!-- TODO screenshot: RUM Pages tab sorted by page views, showing performance and Web Vitals columns per page -->
![RUM Pages tab comparing traffic and performance per page](../images/rum-pages-tab.png)

{{< quiz question="Using traffic, performance, and business value together, which single journey would you pick for a 24/7 synthetic test?" >}}
{{< quiz-option correct=true >}}The checkout journey, from the home page through to a placed order.{{< /quiz-option >}}
{{< quiz-option >}}The home page only, because it has the most traffic.{{< /quiz-option >}}
{{< quiz-option >}}The slowest product page, even if almost nobody visits it.{{< /quiz-option >}}
{{< quiz-feedback >}}
The **checkout journey** carries high traffic, it is the only journey that produces revenue, and it is already the journey showing errors. A test on the home page alone would have stayed green through the entire `payment` service incident, because the home page never broke.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

## The gap RUM cannot close

RUM is honest but passive. Every chart we just read exists only because somebody was shopping.

- At 03:00, when nobody is shopping, there is nothing to monitor and nothing to alert on.
- In a region we have not launched in yet, a broken CDN edge produces no RUM data at all.
- Straight after a deploy, before traffic arrives, the charts still look exactly like the last known good state.

In each case the first signal that something is wrong comes from an end user. That is the gap **Synthetic Monitoring** closes: a scripted user that completes the checkout journey every few minutes from locations we choose, whether or not real end users are online.