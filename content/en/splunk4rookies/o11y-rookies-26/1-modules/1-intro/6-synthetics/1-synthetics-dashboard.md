---
title: 1. Synthetics Dashboard
weight: 1
---

{{% exercise title="Find Your Synthetic Test" %}}

* In Splunk Observability Cloud from the main menu, select **Digital Experience (1)**, then select **Synthetics tests (2)**. This opens the list of configured synthetic tests.

<img src="../images/get-to-synth.png" alt="Open Synthetics tests from the Digital Experience menu" style="display:block; width:auto; max-width:70%; max-height:300px; margin:1rem auto;">

* Earlier in the workshop, **RUM** and **APM** showed that users were experiencing failures during the *PlaceOrder* interaction. Let’s see whether the scheduled synthetic test detected the same problem.

  * Set **Test types** to **Browser (3)**.
  * In **Search**, enter **[NAME OF WORKSHOP] (4)** to display the browser tests for your workshop.
  * Set **Last run status** to **All (5)**. If the filter presents individual options, ensure that all statuses are selected. This prevents a successful latest run from hiding a test that also has earlier failed runs.
  * Select the **blue** name of your workshop’s **browser test (6)** to open its test results.

  ![Transaction Filter](../images/failed-run-results.png)

{{% /exercise %}}
