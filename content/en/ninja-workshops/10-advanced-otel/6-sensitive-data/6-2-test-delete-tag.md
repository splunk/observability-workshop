---
title: 6.2 Test Attribute Processor
linkTitle: 6.2 Test Attribute Processor
weight: 2
---

### Test the Attribute Processor tag updates

Start your gateway agent from the `[WORKSHOP]/6-sensitive-data` directory in the **Gateway** terminal window, and wait until it is ready to receive data.

In this exercise, we will **delete** the `user.account_password`, **update** the `user.phone_number` **attribute** & **hash** the `user.email` in the span data before it is exported by the **Agent**.

{{% notice title="Exercise" style="green" icon="running" %}}

- **Disable the `redaction/redact` processor** in the `traces` pipeline by adding the comment character `#` in front of it and save the `agent.yaml`.
- **Start the **Agent** Collector** from the `[WORKSHOP]/6-sensitive-data` directory in the **Agent** terminal window.
- **Send a span containing `Sensitive data`** by running the **cURL** command from the `[WORKSHOP]/6-sensitive-data` directory in the **Test** terminal window to send `trace.json`.
- **Check the debug output** of both the **Agent** and **Gateway** to confirm that `user.account_password` has been removed, and both `user.phone_number` & `user.email` have been updated.
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

- **Check** the new `gateway-traces.out` file to confirm that `user.account_password` has been removed, and `user.phone_number` & `user.email` have been updated.

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
