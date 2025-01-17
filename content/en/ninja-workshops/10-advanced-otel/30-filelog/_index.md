---
title: Filelog Receiver
linkTitle: 3. Filelog Receiver
time: 10 minutes
weight: 3
---

The Filelog receiver is a receiver that reads log lines from a file. It is useful for testing and development purposes. The Filelog receiver is not recommended for production use, as it is not optimized for performance.

For this part of the workshop, there is script that will generate log lines in a file. The Filelog receiver will read these log lines and send them to the OpenTelemetry Collector.