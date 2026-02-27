---
title: "Phase 0: Python Warm-up"
linkTitle: 2. Python Warm-up
weight: 2
archetype: chapter
time: 15 minutes
description: Run a bare Python app on the host, prove connectivity to Splunk with a custom metric, then use the OBI binary to add APM tracing -- all without Docker.
---

This phase shows that OBI works at the **kernel level** on a raw Linux process. No containers, no sidecars, no SDKs -- just an eBPF binary watching your app from the kernel.

By the end of this section you will have:

1. A running Python Flask app with zero observability code
2. Proof that your Splunk org is receiving data (via a custom metric)
3. Full APM traces for the app -- added from the kernel with zero code changes
