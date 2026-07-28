---
title: Frustration
linkTitle: 2. Frustration
weight: 2
archetype: chapter
time: 5 minutes
---

Now let's see how the same type of analysis can help us understand if our end users are experiencing friction interacting with the application.

{{% exercise title="Monitor friction" %}}

Return to the Project Analyses and open the Frustration timeseries.

Explore the chart, data table, and session replay.

![timeseries chart showing three frustration series](../images/frustration-timeseries.png)

{{< tabs >}}
{{% tab title="Questions" %}}

1. What does this chart tell us?
1. Can you tell why users are expressing frustration?

{{% /tab %}}
{{% tab title="Answers" %}}

1. This chart is tracking different types of frustration signals over time - such as rage clicks, errors, and dead clicks. Multiple users are experiencing points of friction!
1. Did you find the useless "Show all reviews" button? Some users try to click it, it does nothing, and then the user rage clicks.

![frustration replay](https://colony-recorder.s3.amazonaws.com/files/2026-03-19/13f755d5-8819-4d06-83b3-a0f159568b43/ascreenshot_e2b4eaaa95ca43139b275fbe4609f55c_text_export.jpeg)

{{% /tab %}}
{{< /tabs >}}

Because we are monitoring these frustration signals, we can take steps to improve our application and its content, and hopefully see those frustration signals drop over time. The better we can optimize our application, the happier our end users will be, and the more successful they will be.

{{% /exercise %}}

Speaking of frustration, let's now take a look at how to understand what's going on when our end users are not able to do what we expect them to do.