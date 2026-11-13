---
title: 6. Root Cause and Wrap-Up
weight: 6
---

You have followed a slow application dependency into the database and identified the work behind it. Turn that evidence into a useful handoff to the development team.

{{% exercise title="Write your incident handoff" %}}

Using your observations, prepare a short explanation that includes:

1. **Symptom:** Which service and database dependency were slow, in which environment and time window?
2. **Evidence:** Which query did you identify, what was its observed duration, and what did the plan reveal? Label estimates as estimates.
3. **Root cause:** Explain how the missing product-to-tag join relationship creates a Cartesian product and increases the work before the final limit.
4. **Proposed fix:** Restore the intended join predicate, then review additional tuning suggestions with the database owner.
5. **Validation:** Describe how you would test result correctness and compare query duration, intermediate rows, execution plans, and application latency under comparable load after the fix.

{{% /exercise %}}

## What we learned

| Investigation step | What it established |
| --- | --- |
| APM service map | The recommendation service had a slow PostgreSQL dependency. |
| Database Monitoring queries | A product recommendation query took seconds per execution. |
| SQL and execution plan | The missing join relationship produced excessive intermediate combinations and an expensive sort. |
| AI assistance | A proposed join correction and additional tuning ideas to assess. |
| Validation plan | How to check correctness and measure improvement before declaring the incident resolved. |

{{% notice title="Congratulations" style="blue" icon="wine-bottle" %}}
You have completed **Finding issues in the database**. You can now move from a slow application dependency to a specific SQL query, explain its execution plan, and propose an evidence-backed remediation. A successful query can still be inefficient; observing both application and database behavior helps reveal why.
{{% /notice %}}

{{< pager next="/en/splunk4rookies/o11y-rookies-26/modules/" nextLabel="Back to Modules" >}}
