---
title: Application Performance Monitoring (APM)
linkTitle: 4. APM
weight: 4
archetype: chapter
time: 20 minutes
description: In this section, we will use APM to drill down and identify where the problem is.
---

{{% notice icon="user" style="orange" title="Persona" %}}

You are a **back-end developer** and you have been called in to help investigate an issue found by the SRE. The SRE has identified a poor user experience and has asked you to investigate the issue.

{{% /notice %}}

> [!IMPORTANT]
> RUM is the client-side view; APM is the server-side view. Following a RUM trace into the matching APM trace is end-to-end visibility in action — and how we'll drill down to the back-end problem.

{{< webex chat="Pieter Hagen" date="Today • 28/01/2026" seenby="RC" >}}
{{< webex-msg from="PH" name="Pieter Hagen" time="09:42" color="#571bc0" >}}
Hey Robert, I've triaged a customer satisfaction issue with Astronomy Shop. RUM shows poor page load times. I traced a user session to the backend using Related Content — the latency is coming from the **paymentservice**.
{{< /webex-msg >}}

{{< webex-msg from="PH" name="Pieter Hagen" time="09:43" color="#571bc0" >}}
Can you dig into the back-end and find the root cause? I'll send you a link to the trace.
{{< /webex-msg >}}

{{< webex-msg me=true time="09:43" >}}
On it. I'll check APM and the service map. 👍
{{< /webex-msg >}}
{{< /webex >}}

{{% notice title="Tip: let AI do the first pass" style="tip" icon="robot" %}}
Before drilling in manually, you can ask the ✨ **AI Assistant**: *"Analyze services upstream and downstream of paymentservice to root cause the high error rate in the workshop environment."* It will correlate the services for you. In the AI lesson at the end, we'll also see the **AI Troubleshooting Agent** run this whole investigation automatically from a firing alert.
{{% /notice %}}
