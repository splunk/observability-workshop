---
title: 6.2 Test Attribute Processor
linkTitle: 6.2 Test Attribute Processor
weight: 2
---

In this exercise, we will **delete** the `user.account_password`, **update** the `user.phone_number` **attribute** and **hash** the `user.email` in the span data before it is exported by the **Agent**.

{{% notice title="Exercise" style="green" icon="running" %}}

**Start the Gateway**: In the **Gateway** terminal window navigate to the `[WORKSHOP]/6-sensitive-data` directory and run:

```sh { title="Gateway" }
../otelcol --config=gateway.yaml
```

**Start the Agent**: In the **Agent** terminal window navigate to the `[WORKSHOP]/6-sensitive-data` directory and run:

```sh { title="Agent" }
../otelcol --config=agent.yaml
```

**Send a span**:

1. In the **Test** terminal window change into the `6-sensitive-data` directory.
2. Send the span containing **sensitive data** by running the `curl` command to send `trace.json`.
```sh
curl -X POST -i http://localhost:4318/v1/traces -H "Content-Type: application/json" -d "@trace.json"
```

**Check the debug output**: For both the **Agent** and **Gateway** debug output, confirm that `user.account_password` has been removed, and both `user.phone_number` & `user.email` have been updated.

{{% tabs %}}
{{% tab title="New Debug Output" %}}

  ```text
       -> user.name: Str(George Lucas)
       -> user.phone_number: Str(UNKNOWN NUMBER)
       -> user.email: Str. (62d5e03d8fd5808e77aee5ebbd90cf7627a470ae0be9ffd10e8025a4ad0e1287)
       -> user.mastercard: Str(5555 5555 5555 4444)
       -> user.visa: Str(4111 1111 1111 1111)
       -> user.amex: Str(3782 822463 10005)
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

**Check file output**: In the new `gateway-traces.out` file confirm that `user.account_password` has been removed, and `user.phone_number` & `user.email` have been updated:

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
                  "key": "user.amex",
                  "value": {
                    "stringValue": "3782 822463 10005"
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
                  "key": "user.amex",
                  "value": {
                    "stringValue": "3782 822463 10005"
                  }
                } 
              ]
  ```

{{% /tab %}}
{{% /tabs %}}

{{% /notice %}}

Stop the **Agent** and **Gateway** using `Ctrl-C`.
