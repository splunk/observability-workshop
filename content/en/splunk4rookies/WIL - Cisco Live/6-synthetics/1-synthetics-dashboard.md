---
title: 1. Synthetics Dashboard
weight: 1
---

{{% notice title="Exercise" style="green" icon="running" %}}

* In Splunk Observability Cloud from the main menu, click on **Digital Experience → Synthetics tests**. Click on **All** or **Browser tests** to see the list of active tests.

* During our investigation in the RUM section, we found there was an issue with the **Place Order** Transaction. Let's see if we can confirm this from the Synthetics test as well.

---

* Select the test **WIL - Cisco Live - LABOBS-1037 Online Boutique**.
* Click on **Go to all run results**.
* Change **All** to **Failure** **(1)**.

  ![Transaction Filter](../images/failed-run-results.png)

* Click on one of the failed results.

{{% /notice %}}
