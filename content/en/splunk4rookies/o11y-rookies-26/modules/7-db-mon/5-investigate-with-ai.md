---
title: 5. Investigate with AI Assistance
weight: 5
---

Use AI assistance to explain the query and develop a remediation proposal. Compare its suggestions with the SQL and plan you just inspected.

{{% exercise title="Summarize and evaluate the query" %}}

1. In **Query statement**, select **AI recommendations** and then **Generate recommendations**.
2. Read the **Query summarization** panel. Explain in your own words what the query is intended to return: products, tags, and relevance scores filtered by category and tag, ordered for recommendations.

![Query summarization describing the product recommendation statement](../images/query-summary.png)

3. Close the summary panel and open **AI recommendations**. Allow the recommendation to load.
4. Expand **Suggested query** if needed and compare **Original SQL query** with **Optimized SQL query**.
5. Find the proposed join relationship. In the example, it is:

```sql
ON p.product_id = pt.product_id
```

![AI recommendations comparing the original query with a rewrite joining on product_id](../images/ai-recommendations.png)

6. Expand **Recommendations**. Identify the finding about the **JOIN predicate**, then read any additional suggestions about indexes, parameter types, and database statistics.
7. Explain which finding addresses the root cause and which suggestions require further evaluation with the database owner.

![Expanded recommendations describing the missing JOIN predicate and additional tuning suggestions](../images/recommendation-details.png)

{{% /exercise %}}

The join predicate connects a tag to its product instead of pairing unrelated rows. Additional indexing or statistics changes may help the workload, but should be assessed against the schema, data, and application requirements.

{{% notice title="Review the proposal" style="info" %}}
AI responses can vary. Verify the suggested relationship against the schema and confirm that the rewrite preserves the intended results. This exercise ends with a remediation proposal; do not execute suggested SQL or change the shared database. If AI assistance is unavailable, use the example above and your plan evidence to explain the same proposed correction.
{{% /notice %}}

{{< quiz question="Which recommendation addresses the Cartesian product directly?" >}}
{{< quiz-option correct=true >}}Restore the join predicate relating products to their associated tags.{{< /quiz-option >}}
{{< quiz-option >}}Increase the LIMIT so the query returns more recommendations.{{< /quiz-option >}}
{{< quiz-option >}}Apply every suggested index before checking the join relationship.{{< /quiz-option >}}
{{< quiz-feedback >}}
The missing relationship creates the unnecessary combinations. Restoring it targets the cause; additional tuning can be evaluated after correctness and performance are measured.
{{< /quiz-feedback >}}
{{< /quiz >}}
