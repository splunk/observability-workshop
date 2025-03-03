---
title: 8.4 Test Routing Connector
linkTitle: 8.4 Test Routing Connector
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

**Send a Regular Span**:

1. Locate the **Spans terminal** and navigate to the `[WORKSHOP]/8-routing` directory.
2. Send a regular span using the `trace.json` file to confirm proper communication.

Both the `agent` and `gateway` should display debug information, including the span you just sent. The gateway will also generate a new `gateway-traces-standard.out` file, as this is now the designated destination for regular spans.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If you check `gateway-traces-standard.out`, it should contain the `span` sent using the `cURL` command. You will also see an empty `gateway-traces-security.out` file, as the routing configuration creates output files immediately, even if no matching spans have been processed yet.
{{% /notice %}}

**Send a Security Span**:

1. Ensure both the `agent` and `gateway` are running.
2. Send a security span using the `security.json` file to test the gateway’s routing rule.

Again, both the `agent` and `gateway` should display debug information, including the span you just sent. This time, the `gateway` will write a line to the `gateway-traces-security.out` file, which is designated for spans where the `deployment.environment` resource attribute matches `"security_applications"`.
The `gateway-traces-standard.out` should be unchanged.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If you verify the `./gateway-traces-security.out` it should only contain the spans from the `"security_applications"` deployment.environment.
{{% /notice %}}

You can repeat this scenario multiple times, and each trace will be written to its corresponding output file.
{{% /notice %}}

### Conclusion

In this section, we successfully tested the routing connector in the gateway by sending different spans and verifying their destinations.

- **Regular spans** were correctly routed to `gateway-traces-standard.out`, confirming that spans without a matching `deployment.environment` attribute follow the default pipeline.

- **Security-related spans** from `security.json` were routed to `gateway-traces-security.out`, demonstrating that the routing rule based on `"deployment.environment": "security_applications"` works as expected.

By inspecting the output files, we confirmed that the OpenTelemetry Collector *correctly evaluates span attributes and routes them to the appropriate destinations*. This validates that routing rules can effectively separate and direct telemetry data for different use cases.

You can now extend this approach by defining additional routing rules to further categorize spans, metrics, and logs based on different attributes.

Stop the **Agent**, `gateway` and the `log-gen` script in their respective terminals.
