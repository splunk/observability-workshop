---
title: Finding the needle in the Logs
weight: 6
layout: chapter
time: 45 minutes
description: Start from logs alone to triage an incident — filter, group, and spot patterns to find the root cause.
params:
  images:
    - images/lo.webp
---

{{< persona role="SRE on-call" >}}
{{< persona-situation >}}You have an alert for increased error rates in the Astronomy Shop. Logs are your only starting point: no traces, and no metrics dashboards.{{< /persona-situation >}}
{{< persona-goal >}}Name the service behind the errors and the pattern those errors share.{{< /persona-goal >}}
{{< /persona >}}

> [!splunk] **Log Observer** is Splunk Observability Cloud's no-code interface for exploring and analyzing log data. In this module, you will learn to use it as a standalone investigation tool, starting directly from logs rather than arriving from APM or RUM.

This module contains two scenarios:

- **Scenario 1: Log-First Triage** — A full walkthrough of investigating an incident starting from Log Observer
- **Scenario 2: TBD** — A second investigation scenario (under development)

<!-- TODO screenshot: Log Observer hero image -->

{{< pager prev="/en/splunk4rookies/o11y-rookies-26/modules/"  prevLabel="Back to Lessons" >}}
