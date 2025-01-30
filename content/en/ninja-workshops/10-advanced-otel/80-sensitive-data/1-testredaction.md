---
title: Testing The Redaction Rules
linkTitle: 8.1. Test Redaction
weight: 1
---

### Step 2: Verify the Redaction

Ensure that the `agent` is started the `[WORKSHOP]/6-sensitive-data` folder using the correct agent configuration yaml. Next, update and use the **cURL** command we used earlier to send the `health.json` payload, and send the `trace.json` data created above.

After the collector processes the data, verify that:

- The user_id field is deleted.
- The amex cc number field is redacted with the word redacted.
- The account_password field is deleted.
- The account_email field is hashed.
- Sensitive credit card numbers (Visa, MasterCard) are properly masked using regex.
- Check the exported trace data in the file or backend you're using.

### Step 3: Debugging and Monitoring

If you're unsure whether the redaction is working correctly, the summary field in the redaction/update processor will provide helpful debug information.

- Set summary: debug in the configuration.
- This will show detailed diagnostic information about which attributes are redacted, deleted, or updated.

```yaml
summary: debug  # Provides debug-level details on redactions
```

This will log information about each redacted or deleted attribute, helping you troubleshoot if something is missing.

### Step 4: Advanced Configuration (Optional)

#### 4.1 Redacting More Data

You can easily extend the configuration to redact additional sensitive information. For example, if you need to redact phone numbers, social security numbers, or other personally identifiable information (PII), you can add more blocked_values in the redaction processor.

Example:

```yaml
blocked_values:
  - "(\\+\\d{1,2}\\s?)?\\(?\\d{3}\\)?\\s?-?\\d{3}-?\\d{4}"  # Phone number regex
```

#### 4.2 Using Multiple Redaction Strategies

You can combine different strategies for redaction, such as:

-Replacing values with a fixed string ("REDACTED").
-Hashing values for anonymity.
-Deleting values to remove them completely from telemetry data.

### Conclusion

Congratulations! You've successfully configured the OpenTelemetry Collector to remove tags and redact sensitive data. By following the steps in this workshop, you've ensured that any sensitive information in your telemetry data is properly handled and protected. This configuration is critical for adhering to privacy standards and ensuring secure handling of data in your observability pipelines.

Feel free to extend this configuration to suit your own use cases, and explore more advanced redaction patterns based on your requirements.
