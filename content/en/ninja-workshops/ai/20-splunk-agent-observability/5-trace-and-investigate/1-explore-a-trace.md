---
title: Explore a Trace
linkTitle: 1. Explore a Trace
weight: 1
time: 5 minutes
---

Open the Splunk Agent Observability and work through a real trace from the traffic you just generated.

{{< exercise title="Investigate agent behavior" >}}

{{< step title="Open your project and log stream" >}}

**1.** In your browser, go to the Splunk Agent Observability console at `https://console.multitenant.galileocloud.io` and **`workshop`** org

**2.** Open the project using the name you set in the **`GALILEO_PROJECT`** field in the previous step, which is based on your participant number (for example, `project-44`)

**3.** Select the `default` log stream

![Project and log stream selection](../../images/galileo-project.png?width=750px)

{{< /step >}}

{{< step title="Scan the trace list" >}}

Review the list of recent traces, one per message you sent. Note the high-level signals
available at a glance, such as number of input tokens, output tokens, and spans.


![Trace list](../../images/galileo-traces.png?width=750px)

{{< /step >}}

{{< step title="Open a trace and read the span tree" >}}


Open the trace for the Lisinopril dosage question. You should see a single trace containing a
nested **LLM span** for the chatbot node and a **tool span** for `search_medicine_qa`
(retrieval). Expand the tree to follow the agent's path end to end.

![Trace detail with nested spans](../../images/galileo-trace-view.png?width=750px)

{{< /step >}}

{{< step title="Inspect a span" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact span-panel steps + screenshot once finalized -->

Select the **`Healthcare Assistant`** span and confirm it captured the **system and user messages**, the **Available
Tools**, the **Output**, **Token Counts**, **Latency**, and **Agent Cost**. This
is the detail that lets you explain *why* the agent answered the way it did.

![Span detail](../../images/galileo-llm-span.png?width=750px)

{{< /step >}}

{{< step title="View the Trace Graph" >}}

Next, click on the **`Trace graph`** tab, which provides a visual, step-by-step view of how 
this specific interaction executed across the system. 

![Trace Graph](../../images/galileo-trace-graph.png?width=750px)

{{< /step >}}

{{< /exercise >}}