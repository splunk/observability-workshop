---
title: 5. Deploy and Validate
linkTitle: 5. Deploy and Validate
time: 10 minutes
weight: 8
---

Your Config Builder project now contains the solutions for all three
scenarios. In this chapter, you will download the generated YAML, replace the
Agent configuration, and start the Agent once with every processor active.

You will then verify:

- Noisy `/_healthz` spans are dropped.
- Sensitive span attributes are updated, hashed, deleted, or masked.
- JSON logs have useful fields and OpenTelemetry severity values.
- Traces and metrics reach Splunk Observability Cloud when cloud export is
  enabled.
- Transformed logs are visible through Log Observer Connect when the optional
  Splunk HEC and log connection are available.

Local validation is available in every supported environment.
