---
title: 8.4 Conclusion
linkTitle: 8.4 Conclusion
weight: 3
---

## Conclusion

In this section, we successfully tested the routing connector in the gateway by sending different spans and verifying their destinations.

- **Regular spans** were correctly routed to `gateway-traces-standard.out`, confirming that spans without a matching `deployment.environment` attribute follow the default pipeline.

- **Security-related spans** were routed to `gateway-traces-security.out`, demonstrating that the routing rule based on `"deployment.environment": "security-applications"` works as expected.

By inspecting the output files, we confirmed that the OpenTelemetry Collector *correctly evaluates span attributes and routes them to the appropriate destinations*. This validates that routing rules can effectively separate and direct telemetry data for different use cases.

You can now extend this approach by defining additional routing rules to further categorize spans, metrics, and logs based on different attributes.

Stop the `agent` and `gateway` in their respective terminals using `Ctrl-C`.
