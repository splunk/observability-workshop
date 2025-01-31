---
title: Testing the Attribute Processor
linkTitle: 6.1 Test Attribute Processor
time: 10 minutes
weight: 1
---

### Test the Tag Deletion

Fnd your `gateway` terminal window, navigate to the `[WORKSHOP]/6-sensitive-data` directory, start the `gateway` collector and wait until it is ready to receive data.

Next, to test the Tag deletion, find your `agent` terminal window, navigate to the `[WORKSHOP]/6-sensitive-data` directory and start the agent.

{{% notice title="Exercise" style="green" icon="running" %}}
In this exercise, we will **remove the** `user.account_password` **attribute** from span data before it is exported by the `agent`.

- **Ensure there are no existing** `.out` **files** in this directory. Delete them if necessary.
- **Send a span containing `Sensitive data`** by running the **cURL** command to send `trace.json`.
- **Check the debug output** of both the `Agent` and `Gateway` to confirm that `user.account.password` has been removed.

{{% tabs %}}
{{% tab title="New Debug Output" %}}

  ```text
     -> user.email: Str(george@deathstar.email)
     -> user.visa: Str(4111 1111 1111 1111) 
  ```

{{% /tab %}}
{{% tab title="Original Debug Output" %}}

  ```text
     -> user.email: Str(george@deathstar.email)
     -> user.account_password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111) 
  ```

{{% /tab %}}
{{% /tabs %}}

- **Check** the new `gateway-traces.out` file to verify it does not contain the `user.account_password`:

{{% tabs %}}
{{% tab title="New File Output" %}}

  ```json
  "attributes": [
                  {
                    "key": "user.email",
                    "value": {
                      "stringValue": "george@deathstar.email"
                    }
                  },
                  {
                    "key": "user.visa",
                    "value": {
                      "stringValue": "4111 1111 1111 1111"
                    }
                  }
                ]
  ```

{{% /tabs %}}
{{% tab title="Original File Output" %}}

  ```json
  "attributes": [
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
                    "key": "user.visa",
                    "value": {
                      "stringValue": "4111 1111 1111 1111"
                    }
                  }
                ]
  ```

{{% /tab %}}
{{% /tabs %}}

{{%/notice%}}

### Test the Tag Update

Stop the `gateway` so you can delete the `*.out` files and to clear the screen.   Restart your `gateway` terminal window, and wait until it is ready to receive data.

{{% notice title="Exercise" style="green" icon="running" %}}
In this exercise, we will **update the** `user.phone_number` **attribute** & hash the `user.account_email` in the  span data before it is exported by the `agent`.

- **Stop the `Agent` Collector**,

- **Send a span containing `Sensitive data`** by running the **cURL** command to send `trace.json`.
- **Check the debug output** of both the `Agent` and `Gateway` to confirm that `user.account.password` has been removed.

{{% tabs %}}
{{% tab title="New Debug Output" %}}

  ```text
         -> user.email: Str(george@deathstar.email)
         -> user.visa: Str(4111 1111 1111 1111) 
  ```

{{% /tab %}}
{{% tab title="Original Debug Output" %}}

 ```text
       -> user.email: Str(george@deathstar.email)
       -> user.account_password: Str(LOTR>StarWars1-2-3)
       -> user.visa: Str(4111 1111 1111 1111) 
  ```

{{% /tab %}}
{{% /tabs %}}

- **Check** the new `gateway-traces.out` file to verify it does not contain the `user.account_password`:

{{% /notice %}}
