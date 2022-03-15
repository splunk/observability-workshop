---
title: Monitor Containerized Services
weight: 19
---
The development team has started using other containerized services with docker compose. Switch to the provided milestone `08docker-compose-redis` with the instructions from "Getting Started".

Add the [redis monitor][redis-mon] to the OpenTelemetry Collector configuration in `collector.yaml` to get metrics from the [redis cache].

Rebuild the docker-compose stack and run it.

Check that you are getting data in the Redis dashboard:

![Redis dashboard](../../../images/redis-dashboard.png)

The milestone for this task is `08docker-compose-redis-otel`.

[redis]: https://redis.io/
[redis-mon]: https://docs.splunk.com/Observability/gdi/redis/redis.html
