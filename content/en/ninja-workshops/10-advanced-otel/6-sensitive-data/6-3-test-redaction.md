---
title: 6.3 Test Redaction Processor
linkTitle: 6.3 Test Redaction Processor
weight: 3
---

The `redaction` processor gives precise control over which attributes and values are **permitted** or **removed** from telemetry data.  

Earlier we configured the agent collector to:

**Block sensitive data**: Any values (in this case Credit card numbers) matching the provided regex patterns (Visa and MasterCard) are automatically detected and redacted.

This is achieved using the `redaction` processor you added earlier, where we define `regex` patterns to filter out unwanted data:

```yaml
  redaction/redact:               # Processor Type/Name
    allow_all_keys: true          # False removes all key unless in allow list 
    blocked_values:               # List of regex to check and hash
        # Visa card regex.  - Please note the '' around the regex
      - '\b4[0-9]{3}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b'
        # MasterCard card regex - Please note the '' around the regex
      - '\b5[1-5][0-9]{2}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b' 
    summary: debug  # Show detailed debug information about the redaction 
```

### Test the Redaction Processor

In this exercise, we will **redact** the `user.visa` & `user.mastercard` **values** in the span data before it is exported by the **Agent**.
{{% notice title="Exercise" style="green" icon="running" %}}

**Prepare the terminals**: Delete the `*.out` files and clear the screen.

**Enable the `redaction/redact` processor**: Edit `agent.yaml` and remove the `#` we inserted in the previous exercise.

**Start the Gateway**: In the **Gateway** terminal window navigate to the `[WORKSHOP]/6-sensitive-data` directory and run:

```sh { title="Gateway" }
../otelcol --config=gateway.yaml
```

**Start the Agent**: In the **Agent** terminal window navigate to the `[WORKSHOP]/6-sensitive-data` directory and run:

```sh { title="Agent" }
../otelcol --config=agent.yaml
```

**Send a span**: Run the `curl` command and in the **Test** terminal window to send `trace.json`.
```sh
curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
```

**Check the debug output**: For both the **Agent** and **Gateway** confirm the values for `user.visa` & `user.mastercard` have been updated. Notice `user.amex` attribute value was NOT redacted because a matching regex pattern was not added to `blocked_values`

{{% tabs %}}
{{% tab title="New Debug Output" %}}

  ```text
       -> user.name: Str(George Lucas)
       -> user.phone_number: Str(UNKNOWN NUMBER)
       -> user.email: Str. (62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287)
       -> user.mastercard: Str(****)
       -> user.visa: Str(****)
       -> user.amex: Str(3782 822463 10005)
       -> redaction.masked.keys: Str(user.mastercard,user.visa)
       -> redaction.masked.count: Int(2)
  ```

{{% /tab %}}
{{% tab title="Original Debug Output" %}}

 ```text
       -> user.name: Str(George Lucas)
       -> user.phone_number: Str(+1555-867-5309)
       -> user.email: Str(george@deathstar.email)
       -> user.account_password: Str(LOTR>StarWars1-2-3)
       -> user.mastercard: Str(5555 5555 5555 4444)
       -> user.visa: Str(4111 1111 1111 1111)
       -> user.amex: Str(3782 822463 10005)
  ```

{{% /tab %}}
{{% /tabs %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
By including `summary:debug` in the redaction processor, the debug output will include summary information about which matching keys values were redacted, along with the count of values that were masked.

```text
     -> redaction.masked.keys: Str(user.mastercard,user.visa)
     -> redaction.masked.count: Int(2)
 ```

{{% /notice %}}

**Check file output**: In the newly created `gateway-traces.out` file to verify confirm that `user.visa` & `user.mastercard` have been updated.

{{% tabs %}}
{{% tab title="New File Output" %}}

  ```json
  "attributes": [
                {
                  "key": "user.name",
                  "value": {
                    "stringValue": "George Lucas"
                  }
                },
                {
                  "key": "user.phone_number",
                  "value": {
                    "stringValue": "UNKNOWN NUMBER"
                  }
                },
                {
                  "key": "user.email",
                  "value": {
                    "stringValue": "62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287"
                  }
                },
                {
                  "key": "user.mastercard",
                  "value": {
                    "stringValue": "****"
                  }
                },
                {
                  "key":"user.visa",
                  "value":{
                    "stringValue":"****"
                    }
                 },
                {
                  "key":"user.amex",
                  "value":{
                    "stringValue":"3782 822463 10005"
                    }
                 }
              ]
  ```

{{% /tabs %}}
{{% tab title="Original File Output" %}}

  ```json
"attributes": [
                {
                  "key": "user.name",
                  "value": {
                    "stringValue": "George Lucas"
                  }
                },
                {
                  "key": "user.phone_number",
                  "value": {
                    "stringValue": "+1555-867-5309"
                  }
                },
                {
                  "key": "user.email",
                  "value": {
                    "stringValue": "george@deathstar.email"
                  }
                },
                {
                  "key": "user.account_password",
                  "value": {
                    "stringValue": "LOTR>StarWars1-2-3"
                  }
                },
                {
                  "key": "user.mastercard",
                  "value": {
                    "stringValue": "5555 5555 5555 4444"
                  }
                },  
                {
                  "key": "user.visa",
                  "value": {
                    "stringValue": "4111 1111 1111 1111"
                  }
                },
                {
                  "key":"user.amex",
                  "value":{
                    "stringValue":"3782 822463 10005"
                    }
                 }
              ]
  ```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}
<!--
**(Optional) Redact Amex CC number**:

Add the Amex card regex to `blocked_values` and restart **Agent** collector.

```yaml
'\b3[47][0-9]{2}[\s-]?[0-9]{6}[\s-]?[0-9]{5}\b'
```
-->
These are just a few examples of how `attributes` and `redaction` processors can be configured to protect sensitive data.

Stop the **Agent** and **Gateway** using `Ctrl-C`.
