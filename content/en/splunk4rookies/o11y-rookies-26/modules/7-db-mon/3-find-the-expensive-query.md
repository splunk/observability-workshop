---
title: 3. Find the Expensive Query
weight: 3
---

Database Monitoring lets you move from an instance-level view to the queries responsible for its workload.

{{% exercise title="Identify the recommendation query" %}}

1. Click on the Postgres database
2. Under **Database Instances** on the right, click on the database instance. (If there are more than one, click the one with the longest average duration).
3. Compare **Total duration**, **Avg. duration**, and **Executions**. Look for the product recommendation query beginning with the following text:

```sql
SELECT p.product_id, p.name, p.price, pt.tag, pt.relevance_score
FROM products
```

4. Note  its average duration and execution count, then select the query to open its details.

![Queries table highlighting the product recommendation query and its multi-second average duration](../images/queries.png)

{{< quiz question="Why compare average duration with execution count and total duration?" >}}
{{< quiz-option correct=true >}}A frequently executed fast query can consume substantial total time, while an infrequent slow query can explain individual slow requests.{{< /quiz-option >}}
{{< quiz-option >}}The query with the most executions is always the cause of slow requests.{{< /quiz-option >}}
{{< quiz-option >}}Total duration and average duration always mean the same thing.{{< /quiz-option >}}
{{< quiz-feedback >}}
Use these measurements together. Here, the recommendation query's multi-second duration makes it a candidate for the slow dependency seen in APM. Matching the environment, time window, and query purpose strengthens the investigation, but does not by itself prove a specific trace executed that query.
{{< /quiz-feedback >}}
{{< /quiz >}}

{{% /exercise %}}
