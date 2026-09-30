---
title: Beyond the browser test
linkTitle: 5. Beyond the browser test
weight: 5
time: 5 minutes
---

A browser test is the most faithful simulation of a customer, and it is also the most expensive one to run and the most work to maintain. Real monitoring setups layer cheaper, narrower tests underneath it, so that when something breaks we can tell *how much* broke.

Our browser test proves a customer can buy something. An uptime test on the same store proves the store is answering at all. When both fail, the site is down. When only the browser test fails, the site is up and the checkout is broken — a completely different page in the runbook.

## Add an uptime test

An **uptime test** makes a single request and reports on the response. It records three metrics: response time, DNS time, and time to first byte. It takes about a minute to set up.

{{% exercise title="Create an HTTP uptime test" %}}

* From **Digital Experience** > **Synthetic tests**, select {{% button style="blue" %}}Create new test{{% /button %}} and choose **HTTP test**.
* In **Name**, enter:

  ```text
  [NAME OF WORKSHOP]-[YOUR INITIALS]-storefront-uptime
  ```

* Add the same custom properties we used before: `workshop:[NAME OF WORKSHOP]` and `owner:[YOUR INITIALS]`.
* In the **Request** section, set the method to **GET** and enter our Astronomy Shop URL, including `https://`.
* In **Validations**, add a check that the response code equals `200`. Without a validation, the test only tells us that *something* answered.
* Select {{% button style="grey" %}}Try now{{% /button %}} to confirm the request succeeds.
* In **Test configuration**, pick **one** location and a frequency of **5 minutes**.
* Select {{% button style="blue" %}}Create{{% /button %}}.

<!-- TODO screenshot: HTTP uptime test creation page with GET request, URL, and a 200 response code validation -->
![HTTP uptime test configuration](../images/synth-uptime-test.png)

{{< tabs >}}
{{% tab title="Question" %}}

Your browser test fails about half the time. What will this uptime test report?

{{% /tab %}}
{{% tab title="Answer" %}}

Close to 100% uptime. The storefront is serving pages perfectly well — it is only the payment step that fails, and this test never gets that far.

That contrast is the point. An uptime test is a cheap, reliable answer to "is it up?", and it is completely blind to "can customers actually buy?". If the storefront uptime test were the only monitoring in place, the entire checkout incident would have gone unnoticed.

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

## The five test types

| Test type | Answers | Costs | Reach for it when |
|---|---|---|---|
| **Browser** | Can a customer complete this journey, and how does it feel? | Highest | Revenue and conversion paths, logins, multi-step flows, anything running JavaScript |
| **HTTP uptime** | Is this URL answering, and how fast? | Lowest | Broad availability coverage across many endpoints |
| **Port uptime** | Is this TCP or UDP port accepting connections? | Lowest | Non-HTTP services: databases, mail, message brokers |
| **API** | Do these endpoints return correct data, including multi-step sequences? | Low | Back-end contracts, auth flows, anything a mobile app or partner depends on |
| **SSL certificate** | Is the certificate valid, trusted, and not about to expire? | Lowest | Every public hostname we own, to prevent a self-inflicted outage |

{{< notice tip >}}
SSL certificate tests are the highest-value, lowest-effort test on this list. An expired certificate takes a site down completely, is entirely predictable, and is one of the most common causes of avoidable outages. A CA certificate detector set to warn 30 days out costs nothing to run.
{{< /notice >}}

## Bonus: an API test

Have extra time? The Astronomy Shop's front end talks to its back end over a handful of JSON endpoints, and we can monitor those directly — no browser, no rendering, no selectors to maintain.

{{% exercise title="Test the product catalog endpoint" %}}

* Select {{% button style="blue" %}}Create new test{{% /button %}} and choose **API test**. Name it `[NAME OF WORKSHOP]-[YOUR INITIALS]-products-api`.
* Beside **Steps**, select **Add requests**.
* Name the first request `List products`, set the method to **GET**, and enter:

  ```text
  https://<YOUR SHOP URL>/api/products
  ```

* In the **Validation** section, assert that the response code is `200` and that the response body contains a product name we saw in the shop.
* Use {{% button style="grey" %}}Try now{{% /button %}} to confirm the endpoint responds, then save the steps and create the test.

{{< notice >}}
API tests can chain requests, saving a value from one response to use in the next — extract a token, then call an authenticated endpoint with it. That is what makes them useful for real back-end contracts rather than just health checks.
{{< /notice >}}

{{% /exercise %}}

## Two things to know before we do this at work

The Astronomy Shop is a workshop application on a public URL, which makes it unusually easy to test. Our own applications will raise two questions immediately:

- **Bot protection.** Our site may block the synthetic testing agent, which is a sign our security controls are working. Allowlist the [public locations](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/advanced-test-configurations/public-locations) for our realm, and check that our analytics tooling is configured to exclude synthetic traffic so it does not pollute our reporting.
- **Anything not on the public internet.** Internal applications, pre-production environments, and endpoints behind a firewall are reached with [private locations](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/advanced-test-configurations/private-locations) — a container we run on our own infrastructure that executes the tests from inside our network.

Learn more in [Set up an uptime test](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/uptime-tests-for-port-and-http/set-up-an-uptime-test) and [Set up an API test](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/api-tests-for-endpoints/set-up-an-api-test).
