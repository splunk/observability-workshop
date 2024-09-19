---
title: Container Orchestration
weight: 15
---
The development team wants to use a containerized [redis][redis] cache to improve performance of the service.

Stop any other running containers from this app or the OpenTelemetry Collector.

Add a [docker-compose.yaml][docker-compose] file for the python app to prepare us for running multiple containers.

A skeleton to run the service on port 8000 might look like this. What port do you need to map 8000 to for the service to work?

```docker
version: '3'

services:
  yourservicename:
    build: .
    expose:
      - "8000"
    ports:
      - "8000:XXXX"
```

Build the service:

{{< tabs >}}
{{% tab title="Shell Command" %}}
docker-compose build{{% /tab %}}
{{< /tabs >}}

Then run the whole stack:

{{< tabs >}}
{{% tab title="Shell Command" %}}
docker-compose up{{% /tab %}}
{{< /tabs >}}

Test the service with curl by hitting the exposed port.

The milestone for this task is `06docker-compose`.

[redis]: https://redis.io/
[docker-compose]: https://docs.docker.com/compose/
