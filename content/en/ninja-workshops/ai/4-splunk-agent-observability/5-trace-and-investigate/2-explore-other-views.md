---
title: Explore Other Views
linkTitle: 2. Explore Other Views
weight: 2
time: 5 minutes
---

Let's explore other views in Splunk Agent Observability using the traffic you just generated.

{{< exercise title="Investigate agent behavior" >}}

{{< step title="Open your project and log stream" >}}

Return to your project and the `default` log stream in Splunk Agent Observability.

{{< /step >}}

{{< step title="View the Agent Graph" >}}

Click on the **`Agent graph`** tab, which aggregates agent behavior
across all traces in the log stream. It shows the most common execution paths, along with latency and frequency patterns,
so you can quickly see how the agent is behaving with actual users.

![Agent Graph](../../images/galileo-agent-graph.png?width=750px)

{{< /step >}}

{{< step title="View Trends" >}}

We can also switch to the **`Trends`** tab to understand how the system is performing over time. For example, we can
see how the overall latency and token usage trends across requests.

![Trends](../../images/galileo-trends.png?width=750px)

{{< /step >}}

{{< /exercise >}}

{{% notice title="From investigation to automation" style="info" %}}

Reading individual traces is powerful for a single incident, but you can't manually inspect
millions of them. In the next chapter you'll enable **metrics** to score every trace
automatically, so problems like ungrounded medical advice surface on their own.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}


{{< details summary="Click here to see the answer" >}}

{{< /details >}}
