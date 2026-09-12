---
title: 3. Protect sensitive data
linkTitle: 3. Protect sensitive data
time: 6 minutes
weight: 6
---

Telemetry can contain personal, authentication, or payment information. In
this chapter, you configure two processors to protect that data:

- The [**Attributes Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/attributesprocessor/README.md)
  updates, hashes, or removes known span attributes.
- The [**Redaction Processor**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/redactionprocessor/README.md)
  masks values matching patterns such as payment-card numbers.

The original `/movie-validator` span includes:

```text
Attributes:
     -> user.name: Str(George Lucas)
     -> user.phone_number: Str(+1555-867-5309)
     -> user.email: Str(george@deathstar.email)
     -> user.password: Str(LOTR>StarWars1-2-3)
     -> user.visa: Str(4111 1111 1111 1111)
     -> user.amex: Str(3782 822463 10005)
     -> user.mastercard: Str(5555 5555 5555 4444)
```

You replace the phone number, hash the email address, remove the password, and
mask the Visa and Mastercard values. You leave the Amex value visible so you
can see what happens when a redaction policy is incomplete.

Continue editing the same Config Builder project from Chapter 2. Both
processors run in the agent before all trace exporters.
