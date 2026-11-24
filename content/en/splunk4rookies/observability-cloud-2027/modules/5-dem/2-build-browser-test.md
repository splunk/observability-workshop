---
title: Build our browser test
linkTitle: 2. Build our browser test
weight: 2
time: 15 minutes
---

A **browser test** drives a real Google Chrome browser through a journey we script, from the locations we choose, on the schedule we set. In the Introduction module we reviewed a browser test somebody else had built. Now we build our own, for the checkout journey we just chose.

Two concepts do most of the work:

- A **step** is one interaction — go to a URL, click something, or assert that something is there. Steps have names, and those names are what we read when a test fails.
- A **synthetic transaction** is a named group of steps representing a business-critical flow. Each transaction gets its own **duration**, **requests**, and **size** metrics, which is how we end up able to say "checkout got slower" rather than just "the test got slower".

{{% notice title="Everyone shares one shop" style="warning" %}}
All of us in this workshop test the same Astronomy Shop, so each of us needs to put our own initials in the test name. Otherwise we will not be able to find our own test in the list, and neither will the instructor when it is time to clean up.
{{% /notice %}}

## Create the test

{{% exercise title="Start a new browser test" %}}

* From the main menu, select **Digital Experience**, then **Synthetic tests**.
* Select {{% button style="blue" %}}Create new test{{% /button %}} and choose **Browser test**.
* Set the configuration slider at the top of the page to **Advanced**. This reveals the custom properties and security settings we need.
* In **Name**, enter:

  ```text
  [NAME OF WORKSHOP]-[YOUR INITIALS]-checkout
  ```

* In **Custom properties**, add two key-value pairs:

  | Key | Value |
  |---|---|
  | `workshop` | `[NAME OF WORKSHOP]` |
  | `owner` | `[YOUR INITIALS]` |

<!-- TODO screenshot: Browser test creation page in Advanced mode, showing Name and Custom properties fields -->
![Browser test creation page with name and custom properties](../images/synth-create-test.png)

{{% /exercise %}}

{{< notice tip >}}
Custom properties become dimensions on every metric the test produces, so later we can build one chart that covers every test tagged `workshop:[NAME OF WORKSHOP]` instead of editing the chart each time somebody adds a test. 
{{< /notice >}}

## Add the steps and transactions

{{% exercise title="Script the checkout journey" %}}

* Select {{% button style="grey" %}}Edit steps or synthetic transactions{{% /button %}}.
* Create a synthetic transaction named **Browse**, and add these four steps to it.
* Then create a second synthetic transaction named **Checkout**, and add the remaining three steps to it.

For every step that uses a selector, set **Selector type** to **CSS Path** and paste the value from the table into **Selector path**.

| # | Transaction | Step name | Step type | Selector / value | Wait for navigation |
|---|---|---|---|---|---|
| 1 | Browse | Open the shop | **Go to URL** | `https://<YOUR SHOP URL>/` | — |
| 2 | Browse | Products are on the page | **Assert element present** | `[data-cy="product-card"]` | — |
| 3 | Browse | Open a product | **Click element** | `[data-cy="product-card"]` | Yes |
| 4 | Browse | Product page loaded | **Assert element present** | `[data-cy="product-add-to-cart"]` | — |
| 5 | Checkout | Add to cart | **Click element** | `[data-cy="product-add-to-cart"]` | Yes |
| 6 | Checkout | Place the order | **Click element** | `[data-cy="checkout-place-order"]` | Yes |
| 7 | Checkout | Order confirmed | **Assert text present**, using **contains** | `sent you a confirmation email` | — |

* On steps 2, 4, and 7, set **Wait up to** `10000` ms so the assertion tolerates a slow page instead of failing on a race.
* Leave the **device** at the default desktop viewport.

<!-- TODO screenshot: Step editor showing the Browse and Checkout synthetic transactions with their named steps -->
![Step editor with Browse and Checkout transactions](../images/synth-steps.png)

{{< notice >}}
We do not need steps to fill in the checkout form. The Astronomy Shop pre-populates the shipping address and payment details, so **Place Order** is clickable as soon as the cart page loads. Clicking **Add To Cart** takes the browser straight to `/cart`, where that button lives.
{{< /notice >}}

{{< notice tip >}}
Step 7 deliberately matches a **substring** rather than the full sentence on the confirmation page. Real pages use typographic apostrophes and curly quotes that are easy to get wrong when we retype them, and an assertion that fails on an invisible character difference is worse than no assertion at all. Match the shortest phrase that only ever appears when the thing we care about has happened.
{{< /notice >}}

{{% /exercise %}}

### Why these steps look the way they do

These are the browser test practices that matter most, drawn from [Running Synthetic browser tests](https://lantern.splunk.com/Observability_Use_Cases/Understand_Journeys/Running_Synthetic_browser_tests) on Splunk Lantern:

- **Name every step in plain language.** When this test fails at 03:00, the alert tells us *"Order confirmed"* failed. That is a sentence we can act on; `step 7` is not.
- **Group steps into transactions.** Without transactions we get one duration for the whole run. With them, we can tell a slow product page apart from a slow checkout.
- **Assert the goal, not the click.** Step 6 only proves the button was clickable. Step 7 is the step that actually proves a customer got an order — which is why it is the step that will catch the `payment` service breaking.
- **Prefer stable selectors.** `[data-cy="product-card"]` is an attribute the developers put there deliberately. A generated class name like `.css-4t2fjl` changes the next time somebody rebuilds the front end, and our test starts failing for no real reason.

{{< notice tip >}}
The Astronomy Shop home page shows several products, and step 3 clicks the **first** element that matches the selector. That is intentional here: it keeps every run comparable. When we need a specific product, we use a **Go to URL** step against that product's URL instead.
{{< /notice >}}

## Configure how and where it runs

{{% exercise title="Set locations, frequency, and retries" %}}

In the **Details** section:

* **Locations** — choose **one or two** public locations, ideally near us. More locations means more data, but in a shared workshop org it also means more noise for everyone.
* **Frequency** — **5 minutes**. In production a revenue journey like this would typically run every 1 to 5 minutes.
* **Auto retries** — leave **on**. A test that retries once before reporting a failure will not page us because of a single dropped packet.
* **Round-robin scheduling** — leave **off**, so both locations run at every interval rather than alternating.

In the **Security** section:

* Leave **TLS/SSL validation** at its default. If the instructor says the workshop shop uses a self-signed certificate, turn it **off** — otherwise every run fails on the certificate before it ever reaches the checkout.

{{% /exercise %}}

## Validate, then save

{{% exercise title="Try it before we trust it" %}}

* Select {{% button style="grey" %}}Try now{{% /button %}}. The test runs immediately and shows us each step's result.
* Work through any step that reports an error. The usual cause is a selector typo, or a missing **Wait for navigation** on a step that changes the page.
* Once the **Browse** transaction completes successfully, select {{% button style="blue" %}}Create{{% /button %}}.

{{< quiz question="Your Try now run failed at step 7. Is your test broken?" >}}
{{< quiz-option correct=true >}}No. If steps 1 through 6 passed, step 7 is catching the payment defect.{{< /quiz-option >}}
{{< quiz-option >}}Yes. A failed assertion always means the selector is wrong.{{< /quiz-option >}}
{{< quiz-option >}}Yes. Try now only fails when the test was not saved.{{< /quiz-option >}}
{{< quiz-feedback >}}
The Astronomy Shop is deliberately configured so that roughly half of all payment attempts fail, so about half of your runs will not reach an order confirmation. If steps 1 through 6 all pass and step 7 is the only failure, your test is working as designed — it is detecting a real defect. Run **Try now** again and you should see it pass roughly every other time.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}

{{% notice title="Try now vs. Run now" style="info" %}}
**Try now** runs are *temporary*: nothing is stored, no metrics are produced, and our uptime numbers are untouched. That is what makes it safe to use while we are still fixing selectors.

**Run now**, which we use in the next exercise, is *permanent*: results are stored, they count toward metrics and subscription usage, and they appear in the UI marked as **Manual**.
{{% /notice %}}

Learn more in [Set up a browser test](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/browser-tests-for-webpages/set-up-a-browser-test) and [Add synthetic transactions to your browser test](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/synthetic-monitoring/browser-tests-for-webpages/add-synthetic-transactions-to-your-browser-test).
