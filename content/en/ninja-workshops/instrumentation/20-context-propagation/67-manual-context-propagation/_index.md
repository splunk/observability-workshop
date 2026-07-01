---
title: "Phase 2: The OBI Magic"
linkTitle: 4. Docker with OBI
weight: 4
archetype: chapter
time: 20 minutes
description: Add the OBI eBPF agent to your Docker Compose stack. Without changing any application code, full distributed traces appear in Splunk APM.
---

In this phase you'll add a single container to your Docker Compose stack. Without changing any application code, full distributed traces will appear in Splunk APM across all three services.

{{% notice icon="user" style="orange" title="The Key Moment" %}}
This is the core demo of the workshop. You're about to go from **zero traces** to **full distributed tracing** by adding **one container** and changing **zero lines of application code**.
{{% /notice %}}
