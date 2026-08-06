---
title: 1.1 Start and Verify the Agent
linkTitle: 1.1 Start the Agent
weight: 1
---

The Collector runs as a foreground process using `agent_config.yaml`. This
portable-binary approach works on both supported platforms.

{{% exercise title="Check Agent health" %}}

If you have not already started the Agent, run the command on the previous
page in the **Agent Console**.

Leave that process running. In the **Tests** terminal, check the Agent health
extension:

```bash
curl -fsS http://127.0.0.1:13133/ && \
echo "Collector is ready"
```

Treat the successful health response as the readiness checkpoint. Collector
startup logs can include `Everything is ready. Begin running and processing
data.`, but the exact text and formatting are version-specific and can scroll
out of view. In the **Agent Console**, confirm only that the Collector remains
running without configuration errors.

{{% /exercise %}}
