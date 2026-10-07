---
title: Digital Experience (Synthetics)
linkTitle: 6. Digital Experience (Synthetics)
type: chapter
weight: 6
time: 15 minutes
description: In this section, you will learn how to use Splunk Synthetics to monitor the performance and availability of your applications.
---

{{< persona role="SRE" >}}
{{< persona-situation >}}You have been asked to review the synthetic monitoring configured for the Astronomy Shop.{{< /persona-situation >}}
{{< persona-goal >}}Confirm that the preconfigured test can detect availability and performance problems.{{< /persona-goal >}}
{{< /persona >}}

In this introduction, you will use a preconfigured test. If you wish to learn how to create your own, you can do that in a later lesson.

> [!IMPORTANT]
> **Synthetic Monitoring** runs scheduled tests that *simulate* user journeys, even when no real customers are using the application. You’ll examine a *prebuilt* test that runs every minute and checks the availability and performance of a typical journey through the *Astronomy Shop*.

{{< webex chat="Bill Grant" date="Today • 28/01/2026" seenby="BG" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
Hey Bill, now that we’ve resolved the `payment` service issue, let’s review our *synthetic monitoring* to ensure that we catch any future issues before they impact our customers.
{{< /webex-msg >}}

{{< /webex >}}
