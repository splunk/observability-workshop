---
title: Explore a Trace
linkTitle: 1. Explore a Trace
weight: 1
time: 10 minutes
---

{{% notice style="warning" title="TODO" %}}
Confirm which organization will be used for the workshop.
Add knowledge check
{{% /notice %}}

Open the console and work through a real trace from the traffic you just generated.

{{< exercise title="Investigate agent behavior" >}}

{{< step title="Open your project and log stream" >}}

**1.** In your browser, go to the Splunk Agent Observability console at `https://console.multitenant.galileocloud.io`

**2.** Confirm you're in the **`ORGANIZATION_PLACEHOLDER`** organization (top-left org switcher)

![Galileo Organization Page](../../images/galileo-organization.png?width=750px)

**3.** Open the project using the name you set in the **`galileo_project`** field in the previous step

**4.** Select the stream using the project/log stream configured in `secrets.toml` (**`local`** by default)

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

{{< /exercise >}}

{{% notice title="From investigation to automation" style="info" %}}

Reading individual traces is powerful for a single incident, but you can't manually inspect
millions of them. In the next chapter you'll enable **metrics** to score every trace
automatically, so problems like ungrounded medical advice surface on their own.

{{% /notice %}}

{{< checkpoint title="Knowledge Check" >}}


{{< details summary="Click here to see the answer" >}}

{{< /details >}}
