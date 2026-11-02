---
title: Beyond the browser test
linkTitle: 5. Beyond the browser test
weight: 5
time: 5 minutes
---

Browser tests prove a customer can complete a workflow, regardless of the resources and endpoints involved.

Uptime tests focus on the health of critical **endpoints** that are required for your end users to complete their tasks. These tests are much more lightweight and can be run much more frequently, so that while our browser tests are evaluating health of workflows, uptime tests are pinpointing health of individual pieces of those workflows.

## Add an uptime test

An **uptime test** makes a single request and reports on the response, with optional additional validations. It records three metrics: response time, DNS time, and time to first byte.

{{% exercise title="Create an HTTP uptime test" %}}

* From **Digital Experience** > **Synthetic tests**, select {{% button style="blue" %}}Create new test{{% /button %}} and choose **HTTP test**.
* In **Name**, enter:

  ```text
  [NAME OF WORKSHOP]-[YOUR INITIALS]-storefront-uptime
  ```

* Add the same custom properties we used before: `workshop:[NAME OF WORKSHOP]` and `owner:[YOUR INITIALS]`.
* In the **Request** section, set the method to **GET** and enter our Astronomy Shop URL, including `https://`.
* Select {{% button style="grey" %}}Try now{{% /button %}} to confirm the request succeeds.
* In **Test configuration**, pick **one** location and a frequency of **1 minute**.
* Select {{% button style="blue" %}}Create{{% /button %}}.

<!-- TODO screenshot: HTTP uptime test creation page with GET request, URL, and a 200 response code validation -->
![HTTP uptime test configuration](../images/synth-uptime-test.png)

{{< quiz question="Your browser test fails about half the time. What will this uptime test report?" >}}
{{< quiz-option correct=true >}}Close to 100% uptime. This test never reaches the payment step.{{< /quiz-option >}}
{{< quiz-option >}}About 50% uptime, the same as the browser test.{{< /quiz-option >}}
{{< quiz-option >}}0% uptime, because the shop is down.{{< /quiz-option >}}
{{< quiz-feedback >}}
The storefront is serving pages perfectly well — it is only the payment step that fails, and this test never gets that far. An uptime test is a cheap, reliable answer to "is it up?" If this were the only monitoring in place, the entire checkout incident would have gone unnoticed.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}
Learn more in [Set up an uptime test](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/uptime-tests-for-port-and-http/set-up-an-uptime-test)
## When to use which test type

| Test type | Answers | Use for |
|---|---|---|---|
| **Browser** | Can an end user complete this workflow, and how does it feel? | Revenue and conversion paths, logins, multi-step flows, anything running JavaScript |
| **HTTP uptime** | Is this URL answering, and how fast? | Broad availability coverage across many endpoints |
| **Port uptime** | Is this TCP or UDP port accepting connections? | Non-HTTP services: databases, mail, message brokers |
| **API** | Do these endpoints return correct data, including multi-step sequences? | Back-end contracts, auth flows, anything a mobile app or partner depends on |
| **SSL certificate** | Is the certificate valid, trusted, and not about to expire? | Every hostname we own, to prevent a self-inflicted outage |

{{< notice tip >}}
Certain test types like Uptime and SSL are cheaper to run, and therefore easier to **run more frequently** to monitor critical endpoints and certificates. Balance these with more complex Browser and API tests to get proactive coverage for your end users' success.
{{< /notice >}}

## Bonus: an API test

Have extra time? The Astronomy Shop's front end talks to its back end over a handful of JSON endpoints, and we can monitor those directly — no browser, no rendering.

{{% exercise title="Test the product catalog endpoint" %}}

* Select {{% button style="blue" %}}Create new test{{% /button %}} and choose **API test**. Name it `[NAME OF WORKSHOP]-[YOUR INITIALS]-products-api`.
* Beside **Steps**, select **Add requests**.
* Name the first request `List products`, set the method to **GET**, and enter:

  ```text
  https://<YOUR SHOP URL>/api/products
  ```

* In the **Validation** section, assert that the response body contains a product name we saw in the shop.
* Use {{% button style="grey" %}}Try now{{% /button %}} to confirm the endpoint responds, then save the steps and create the test.

{{< notice >}}
API tests can chain requests, saving a value from one response to use in the next — extract a token, then call an authenticated endpoint with it. That is what makes them useful for real back-end contracts rather than just health checks.
{{< /notice >}}

{{% /exercise %}}
Learn more in [Set up an API test](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/api-tests-for-endpoints/set-up-an-api-test).
## Know before you go

Keep these things in mind when you start testing your own application and endpoints.

- **Bot protection.** Your site may block the synthetic testing agent, which is a sign your security controls are working. Allowlist the [public locations](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/advanced-test-configurations/public-locations) for your Observability Cloud realm, and check that your analytics tooling is configured to exclude synthetic traffic so it does not pollute your reporting.
- **Anything not on the public internet.** Internal applications, pre-production environments, and endpoints behind a firewall can be reached with [private locations](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/advanced-test-configurations/private-locations) — a container you run on your own infrastructure that executes the tests from inside your network.
