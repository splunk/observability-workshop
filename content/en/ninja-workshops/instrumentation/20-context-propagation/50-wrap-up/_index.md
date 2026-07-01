---
title: Wrap-Up
linkTitle: 6. Wrap-Up
weight: 6
time: 5 minutes
description: Key takeaways & cleanup instructions.
---

## Summary

This workshop provided hands-on experience with:

- How **header-stripping reverse proxies** break W3C Trace Context propagation
- Deploying application services first, and validating the end-to-end request flow runs correctly.
- Then deploying the **Splunk Distribution of the OpenTelemetry Collector** and instrumenting the Python microservices to export telemetry to **Splunk Observability Cloud**
- Observing **fragmented traces** in Phase 1, and validating Infrastructure metrics
- Restoring **connected traces** in Phase 2 with manual inject/extract

## Reference Segments Commands

| Action | Command |
| ------ | ------- |
| Step 1 — Deploy Services | `start-lab.sh` |
| Step 2 — Deploy Collector | `deploy-collector.sh` |
| Step 3 - Continuous Load | `start-load.sh` |
| Step 4 - Manual Propagation (code guides) | manual-propagation.md |
| Step 5 - Stop & clean-Up Stack | `teardown.sh` |

## Clean Up

```bash
./scripts/teardown.sh
```
