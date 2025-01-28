---
title: Removing Tags and Redacting Sensitive Data in OpenTelemetry Collector
linkTitle: 6. Sensitive Data
time: 10 minutes
weight: 6
---

In this section, you'll learn how to configure the OpenTelemetry Collector to remove specific tags and redact sensitive data from your telemetry (traces). This is essential when dealing with sensitive information such as credit card numbers, personal data, or other security-related information that needs to be protected or anonymized.

We'll walk through how to configure several processors in the OpenTelemetry Collector, including:

- **Removing Tags**.
- **Redacting Sensitive Data** (such as credit card numbers and account credentials).
- **Using regular expressions to block sensitive data**.

By the end of this workshop, you'll have a working OpenTelemetry Collector configuration that securely handles sensitive telemetry data.

Here’s a breakdown of the main components:

Processors: These will handle the data removal and redaction.
Batch Processor: We'll use it to control how traces are batched and exported.
Memory Limiter: Ensures that the collector does not consume too much memory.
Redaction Processor: A dedicated processor for redacting sensitive data, including credit card numbers and account details.

### Step 1: Review the YAML Configuration

Let's look at the YAML configuration for this workshop. This file contains various processors and how they are configured to remove and redact sensitive data.

```yaml
processors:
  # Batch processor to control batch size and metadata keys
  batch:
    metadata_keys:
      - X-SF-Token
  
  # Memory Limiter processor to prevent excessive memory usage
  memory_limiter:
    check_interval: 2s
    limit_mib: 512
  
  # Resource detection processor to detect system resource attributes
  resourcedetection:
    detectors: [system]
    override: true
  
  # Resource processor to add a new mode attribute
  resource/add_mode:
    attributes:
      - action: insert
        value: "agent"
        key: otelcol.service.mode
  
  # Attributes processor to remove specific tags (attributes) from traces
  attributes/removetags:
    actions:
      - key: SPAN_TAG_KEY
        action: delete

  # Attributes processor to update or redact sensitive data
  attributes/update:
    actions:
      - key: cc_number
        value: redacted
        action: update  # Redacts credit card numbers with the word 'redacted'
      - key: account_password
        action: delete  # Deletes account password attribute
      - key: account_email
        action: hash  # Hashes the account email for privacy
  
  # Redaction processor to apply custom redaction rules
  redaction/update:
    allow_all_keys: false  # Block non-allowed keys
    allowed_keys:
      - description
      - group
      - id
      - name
    ignored_keys:
      - safe_attribute  # Safe attributes that won’t be redacted
    blocked_values:
      - "4[0-9]{12}(?:[0-9]{3})?"  # Regular expression for Visa credit card numbers
      - "(5[1-5][0-9]{14})"        # Regular expression for MasterCard numbers
    summary: debug  # Diagnostic summary of redacted attributes
```

### Breakdown of Key Configurations

#### 1. Remove Tags (Attributes)

The `attributes/removetags` processor allows you to delete specific attributes (tags) from spans. In this case, we're removing the tag `SPAN_TAG_KEY`:

```yaml
attributes/removetags:
  actions:
    - key: SPAN_TAG_KEY
      action: delete
```

#### 2. Update Sensitive Data

The attributes/update processor is used to update or redact sensitive data. We perform the following actions:

Redacting credit card numbers: Replace the cc_number with the word "redacted".
Deleting the account_password field to remove passwords from traces.
Hashing the account_email to anonymize email addresses.

```yaml
attributes/update:
  actions:
    - key: cc_number
      value: redacted
      action: update
    - key: account_password
      action: delete
    - key: account_email
      action: hash
```

#### 3. Redaction Processor

The redaction/update processor provides fine-grained control over which attributes are allowed or blocked from traces. We configure this processor to:

Allow specific keys: `description`, `group`, `id`, and name are the only allowed attributes.
Block sensitive data: Credit card numbers matching the provided regex patterns (Visa and MasterCard) will be blocked and redacted.

```yaml
redaction/update:
  allow_all_keys: false
  allowed_keys:
    - description
    - group
    - id
    - name
  ignored_keys:
    - safe_attribute  # Attributes that will not be redacted
  blocked_values:
    - "4[0-9]{12}(?:[0-9]{3})?"  # Visa card regex
    - "(5[1-5][0-9]{14})"         # MasterCard card regex
  summary: debug  # Show detailed debug information about redactions
```

### Step 2: Apply and Test the Configuration

#### 2.1 Save the Configuration

Save the YAML configuration above into a file called otel-collector-config.yaml.

#### 2.2 Run the OpenTelemetry Collector

To run the OpenTelemetry Collector with your configuration file, use the following command:

```bash
otelcol --config=otel-collector-config.yaml
```

### 2.3 Generate Some Sample Data

To test the configuration, generate some sample telemetry data (traces) that includes sensitive attributes such as:

- cc_number (credit card number),
- account_password (password),
- account_email (email address).

You can use a test application or OpenTelemetry instrumentation to simulate these traces.

### 2.4 Verify the Redaction

After the collector processes the data, verify that:

- The cc_number field is redacted with the word redacted.
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
