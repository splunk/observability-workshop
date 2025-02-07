---
title: 4.4 Simulate Recovery
linkTitle: 4.4 Simulate Recovery
weight: 4
---

In this exercise, we’ll test how the **OpenTelemetry Collector** recovers from a network outage by restarting the **Gateway**. When the **Gateway** becomes available again, the **Agent** will resume sending data from its last checkpointed state, ensuring no data loss.

{{% notice title="Exercise" style="green" icon="running" %}}

**Restart the Gateway**: In the **Gateway** terminal window run:

```sh
../otelbin --config=gateway.yaml
```

**Restart the Agent**: In the **Agent** terminal window run:

```sh
../otelbin --config=gateway.yaml
```

**Inspect the Agent logs**: Once the **Gateway** is up and running the **Agent** will resume sending data from the last checkpointed state, ensuring no data is lost. You should see the **Gateway** begin receiving the previously missed traces without requiring any additional action on your part.

{{% /notice %}}
{{% notice title="Tip" style="primary" icon="lightbulb" %}}
Note that only the **Gateway** will show that the checkpointed traces have arrived. The agent will not display any indication that data new or old has been sent.
{{% /notice %}}

### Conclusion

This exercise demonstrated how to enhance the resilience of the OpenTelemetry Collector by configuring the `file_storage` extension, enabling retry mechanisms for the `otlp` exporter, and using a file-backed queue for temporary data storage.

By implementing file-based checkpointing and queue persistence, you ensure the telemetry pipeline can gracefully recover from temporary interruptions, making it a more robust and reliable for production environments.

If you want to know more about the `FileStorage` extension, you can find it [**here**](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/storage/filestorage).

Stop the **Agent** and **Gateway** using `Ctrl-C`.
