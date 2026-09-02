---
title: 4. Feature Adoption
weight: 4
time: 10 minutes
---

Remember the **Ask AI** feature on Astronomy Shop product detail pages? Product leadership wants to know whether customers are using it — including the quick prompts below the text input field.

![Ask AI feature with quick prompt buttons on an Astronomy Shop product detail page](../images/ask-ai-astronomy.png)

**Time series analyses** visualize trends over time and let you drill into specific periods with session replay. Adoption trends help product teams decide whether to invest in, redesign, or retire a feature. See [Create a time series analysis](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/analyses-in-digital-experience-analytics/create-a-time-series-analysis) for more.

{{% exercise title="Understand feature adoption" %}}

1. Navigate to the **Analyses** tab of the Astronomy Shop DXA project.
2. Open the time series analysis **`AI feature adoption`**.

<!-- TODO screenshot: AI feature adoption time series chart showing quick prompt usage over time -->

![Time series chart showing AI feature adoption and quick prompt usage over time](images/ai-feature-adoption-timeseries.png)

{{< tabs >}}
{{% tab title="Questions" %}}

1. Are all of the AI quick prompts used equally? Is there a least popular one?
1. Why might this chart be useful for a product team?

{{% /tab %}}
{{% tab title="Answers" %}}

1. Prompt popularity will depend on your workshop classmates' interactions during the shopping exercise!
1. A time series showing when users interact with a feature helps you understand whether adoption is growing, plateauing, or declining. That informs product investment decisions — whether to improve the feature, change its placement, or revisit the strategy entirely.

{{% /tab %}}
{{< /tabs >}}

3. Click a data point on the chart to load relevant **session replays**.
4. Open a session replay and watch the playback.

<!-- TODO screenshot: Session replay showing a user interacting with the Ask AI feature and quick prompts -->

![Session replay of a user interacting with the Ask AI feature on a product page](../images/ai-feature-adoption-replay.png)

{{< tabs >}}
{{% tab title="Questions" %}}

1. What do you see in the replay?
1. What value does session replay add when analyzing feature adoption?

{{% /tab %}}
{{% tab title="Answers" %}}

1. Session details appear at the top. Interactions are shown in the timeline on the left and on the playback bar. The pane on the right recreates what the end user saw and experienced.
1. Replay reveals *why* adoption might be lower than expected — for example, users scrolling past the feature, a popup obscuring it, or confusion about how to use the quick prompts. Metrics tell you adoption is low; replay shows you why.

{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}

Feature adoption tells you what users choose to engage with. Next, let's look at signals that reveal when the experience is going wrong.
