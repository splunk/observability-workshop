---
title: AI-Assisted Troubleshooting
linkTitle:  7. AI-Assisted Troubleshooting
weight: 7
archetype: chapter
time: 10 minutes
description: Meet the newest members of the platform — the AI Assistant and the AI Troubleshooting Agent — and let them accelerate the root cause analysis you just did by hand.
---

{{% notice icon="user" style="orange" title="Persona" %}}

You are the **on-call SRE**. It's late, an alert just fired on the Astronomy Shop, and you'd like a second pair of hands. Splunk Observability Cloud now ships with exactly that — AI that troubleshoots alongside you.

{{% /notice %}}

>[!IMPORTANT]
> You've just found the root cause the classic way: **RUM → APM → Trace → Logs**. It works, but it takes knowledge and time. In this lesson you'll repeat the investigation with two AI capabilities that dramatically reduce **MTTI** (mean time to identify): the **AI Assistant** (ask in plain English) and the **AI Troubleshooting Agent** (automatic, evidence-backed root cause from a firing alert).

{{< webex chat="Bill Grant" date="Today • 28/01/2026" seenby="PH" >}}
{{< webex-msg from="BG" name="Bill Grant" time="10:05" >}}
Nice work finding the paymentservice issue! We're rolling out the new AI troubleshooting features — can you see if the AI reaches the same conclusion you did?
{{< /webex-msg >}}

{{< webex-msg me=true time="10:06" >}}
Good idea — let me put it to the test. If it can nail the root cause and suggest a fix, that's a huge time-saver for the whole on-call team. 🤖
{{< /webex-msg >}}
{{< /webex >}}

{{% notice title="Feature availability" style="note" icon="triangle-exclamation" %}}
The **AI Troubleshooting Agent & Remediation Plan** is rolling out realm-by-realm (initially **us1**) for detectors on standard APM-service and Kubernetes metrics. The **AI Assistant** is available more broadly across APM, RUM and Infrastructure. If a feature isn't enabled in your workshop org, your instructor will demo it live.
{{% /notice %}}
