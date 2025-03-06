---
title: 8.3 Test Routing Connector
linkTitle: 8.3 Test Routing Connector
weight: 3
---

{{% notice title="Exercise" style="green" icon="running" %}}

In this section, we will test the `routing` rule configured for the **Gateway**. The expected result is that the`span` from the `security.json` file will be sent to the `gateway-traces-security.out` file.

**Start the Gateway**: In your **Gateway terminal** window start the `gateway`.

**Start the Agent**: In your **Agent terminal** window start the `agent`.

**Send a Regular Span**: In the **Spans terminal** window send a regular span using the `loadgen`:

```bash
../loadgen -count 1
```

Both the `agent` and `gateway` will display debug information. The gateway will also generate a new `gateway-traces-standard.out` file, as this is now the designated destination for regular spans.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If you check `gateway-traces-standard.out`, it will contain the `span` sent by `loadgen`. You will also see an empty `gateway-traces-security.out` file, as the routing configuration creates output files immediately, even if no matching spans have been processed yet.
{{% /notice %}}

**Send a Security Span**: In the **Spans terminal** window send a security span using the `security` flag:

```bash
../loadgen -security -count 1
```

Again, both the `agent` and `gateway` should display debug information, including the span you just sent. This time, the `gateway` will write a line to the `gateway-traces-security.out` file, which is designated for spans where the `deployment.environment` resource attribute matches `"security_applications"`.
The `gateway-traces-standard.out` should be unchanged.

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
If you verify the `./gateway-traces-security.out` it should only contain the spans from the `"security_applications"` deployment.environment.
{{% /notice %}}

You can repeat this scenario multiple times, and each trace will be written to its corresponding output file.
{{% /notice %}}
