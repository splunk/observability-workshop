---
title: 5. Deploy and validate the configuration
linkTitle: 5. Deploy and validate
time: 10 minutes
weight: 8
---

Your Config Builder project now contains the changes for all three scenarios.
In this chapter, you download the generated YAML, replace the agent
configuration, and restart the agent with every processor active.

You will then verify:

- Noisy `/_healthz` spans are dropped.
- Sensitive span attributes are updated, hashed, deleted, or masked.
- JSON logs have useful fields and OpenTelemetry severity values.
- Traces and metrics reach Splunk Observability Cloud when cloud export is
  enabled.

You can complete all local checks in any supported workshop environment.
