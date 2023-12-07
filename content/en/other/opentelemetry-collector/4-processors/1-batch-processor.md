---
title: OpenTelemetry Collector Processors
linkTitle: 4.1 Batch
weight: 1
---

## Batch Processor

By default, only the **batch** processor is enabled. This processor is used to batch up data before it is exported. This is useful for reducing the number of network calls made to exporters. For this workshop, we will inherit the following defaults which are hard-coded into the Collector:

- `send_batch_size` (default = 8192): Number of spans, metric data points, or log records after which a batch will be sent regardless of the timeout. send_batch_size acts as a trigger and does not affect the size of the batch. If you need to enforce batch size limits sent to the next component in the pipeline see send_batch_max_size.
- `timeout` (default = 200ms): Time duration after which a batch will be sent regardless of size. If set to zero, send_batch_size is ignored as data will be sent immediately, subject to only send_batch_max_size.
- `send_batch_max_size` (default = 0): The upper limit of the batch size. 0 means no upper limit on the batch size. This property ensures that larger batches are split into smaller units. It must be greater than or equal to send_batch_size.

For more information on the Batch processor, see the [Batch Processor documentation](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md).
