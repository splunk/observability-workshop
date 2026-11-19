---
title: 2. Follow the Slow Request
weight: 2
---

Start with the customer symptom: recommendations sometimes take too long to appear. APM helps locate the dependency contributing to that delay.

{{% exercise title="Locate the slow database call" %}}

1. Open **APM Overview** and set the environment to `[NAME OF WORKSHOP]-workshop`.
2. Open the **Service Map** and locate the **recommendation** service.
3. Find its connection to the PostgreSQL database, shown as **postgresql:astroshop** in the example.
4. Select that connection and inspect its latency and request/error charts.

![APM service map with the recommendation-to-PostgreSQL connection selected and its latency charts displayed](../images/service-map.png)

The example shows calls taking several seconds. Your values may differ. Other services may also have faults enabled; keep this investigation focused on the recommendation database dependency.

{{< quiz question="The database call is slow but shows no errors. What should you do next?" >}}
{{< quiz-option correct=true >}}Investigate the query and its execution plan; successful calls can still have a performance regression.{{< /quiz-option >}}
{{< quiz-option >}}Close the incident because the requests succeeded.{{< /quiz-option >}}
{{< quiz-option >}}Assume the database needs more CPU without examining its queries.{{< /quiz-option >}}
{{< quiz-feedback >}}
A successful response does not establish that the work was efficient. The service map identifies a slow dependency; Database Monitoring helps explain the database work behind it.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}
