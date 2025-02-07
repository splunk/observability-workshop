---
title: 8.3 Setup Environment
linkTitle: 8.3 Setup Environment
weight: 3
---

In this section, we will test the `routing` rule configured for the **Gateway**. The expected result is that the`span` from the `security.json` file will be sent to the `gateway-traces-security.out` file.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In the **Gateway** terminal window navigate to the `[WORKSHOP]/8-routing` directory and run:

```sh
../otelcol --config=gateway.yaml
```

**Start the Agent**: In the **Agent** terminal window navigate to the `[WORKSHOP]/8-routing` directory and run:

```sh
../otelcol --config=agent.yaml
```

**Create new security trace**: In the **Tests** terminal window navigate to the `[WORKSHOP]/8-routing` directory.
  
The following JSON contains attributes which will trigger the routing rule. Copy the content from the tab below and save into a file named `security.json`.

{{% tabs %}}
{{% tab title="security.json" %}}

```json
{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"password_check"}},{"key":"deployment.environment","value":{"stringValue":"security_applications"}}]},"scopeSpans":[{"scope":{"name":"my.library","version":"1.0.0","attributes":[{"key":"my.scope.attribute","value":{"stringValue":"some scope attribute"}}]},"spans":[{"traceId":"5B8EFFF798038103D269B633813FC60C","spanId":"EEE19B7EC3C1B174","parentSpanId":"EEE19B7EC3C1B173","name":"I'm a server span","startTimeUnixNano":"1544712660000000000","endTimeUnixNano":"1544712661000000000","kind":2,"attributes":[{"keytest":"my.span.attr","value":{"stringValue":"some value"}}]}]}]}]}
```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}
