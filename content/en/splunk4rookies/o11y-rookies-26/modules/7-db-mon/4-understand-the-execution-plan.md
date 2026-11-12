---
title: 4. Understand the Execution Plan
weight: 4
---

A **normalized query** replaces literal values with placeholders such as `?`, making it easier to group similar statements. An **execution plan** describes how PostgreSQL processes a query: reading tables, combining rows, sorting, and returning results.

{{% exercise title="Follow the work through the plan" %}}

1. Read the **Query statement** at the top of the details pane. Identify `products`, `product_tags`, the category and tag filters, and the ordering by relevance score.
2. Inspect the **JOIN** condition. How are the tables related?
3. See the **Explain plans**, select the available plan if necessary, and use the **List** and **Graph** to inspect it. Are there specific nodes that are taking up the bulk of the execution?

![Normalized query and execution-plan graph showing a high-cost Sort above a Nested Loop](../images/execution-plan.png)

{{% /exercise %}}

## Explain the row explosion

A join should connect each product to its associated tags. If that relationship is missing and the condition is always true, every qualifying product is paired with every qualifying tag: a **Cartesian product**. PostgreSQL then has a much larger intermediate result to sort before applying the limit.

For example, 1,000 qualifying products paired with 1,000 qualifying tags produce 1,000,000 combinations. This is an illustration, not an expected count for your environment.

The demo's plan and SQL together point to the missing relationship. A nested loop by itself is not a defect, and normalized placeholders alone do not reveal their original values. Look for the combination of the missing column relationship, the plan's row estimates, and the expensive downstream sort.

{{% notice title="Cost is not elapsed time" style="info" %}}
The screenshot labels the Sort with approximately **94% of plan cost**. This is not a measurement that 94% of elapsed time was spent sorting. Keep planner estimates separate from observed query duration and distinguish estimated row counts from actual rows processed.
{{% /notice %}}

{{< quiz question="Why can a query with LIMIT still be expensive?" >}}
{{< quiz-option correct=true >}}The database may need to combine and sort a large intermediate result before it can return the limited set of rows.{{< /quiz-option >}}
{{< quiz-option >}}LIMIT guarantees that only that many rows are processed throughout the plan.{{< /quiz-option >}}
{{< quiz-option >}}A Sort node always means the database is broken.{{< /quiz-option >}}
{{< quiz-feedback >}}
LIMIT restricts the final result. It does not guarantee that earlier operations avoid processing many more rows. Restoring the intended join relationship addresses the unnecessary combinations feeding the sort.
{{< /quiz-feedback >}}
{{< /quiz >}}
