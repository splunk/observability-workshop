---
title: AI-Powered Log Analysis
linkTitle: 5. Log Observer AI
weight: 5
---

## AI Capabilities in Log Observer

Splunk Observability Cloud's Log Observer includes several AI-powered features that help you make sense of large volumes of log data:

- **Pattern Detection**: Automatically identify common patterns in logs
- **Anomaly Highlighting**: Surface unusual log entries or patterns
- **Log Clustering**: Group similar log messages together
- **Intelligent Filtering**: AI-suggested filters based on context
- **Natural Language Queries**: Query logs using plain language (where available)

## Pattern Detection

### What is Log Pattern Detection?

Instead of viewing individual log lines, pattern detection groups logs by their structure, making it easier to:
- Identify frequent vs. rare patterns
- Spot new or unusual log patterns
- Focus on anomalous entries
- Reduce noise from repetitive logs

### How It Works

The AI engine:
1. Analyzes log message structures
2. Identifies variable portions (IDs, timestamps, values)
3. Creates pattern templates
4. Groups logs by template
5. Tracks pattern frequency and changes

## Hands-On Exercise: Explore Log Patterns

{{% notice title="Exercise" style="primary" icon="tasks" %}}

### Step 1: Access Log Observer

1. Navigate to **Log Observer**
2. Select a time range with active log data
3. Choose a service or index with varied logs

### Step 2: Enable Pattern View

1. Look for **Patterns** or **Pattern Analysis** view
2. Switch from individual log view to pattern view
3. Observe how logs are clustered

### Step 3: Analyze Patterns

Review the pattern list:
- **High-frequency patterns**: Normal, expected logs
- **New patterns**: Recently appeared (potential issues)
- **Rare patterns**: Infrequent, worth investigating
- **Error patterns**: Structured error messages

### Step 4: Investigate Anomalies

1. Click on a rare or new pattern
2. View example logs from that pattern
3. Compare with baseline/normal patterns
4. Determine if it indicates an issue

{{% /notice %}}

## Log Anomaly Detection

### Types of Anomalies Detected

1. **Frequency Anomalies**: Sudden increase/decrease in log volume
2. **Content Anomalies**: Unusual field values or message content
3. **Pattern Anomalies**: New patterns not seen in baseline
4. **Timing Anomalies**: Logs appearing at unusual times

### Configuring Anomaly Detection

Set up log-based detectors with ML:
1. Navigate to **Alerts & Detectors**
2. Create a new detector from Log Observer
3. Select **Anomaly Detection** mode
4. Configure:
   - Baseline period
   - Sensitivity level
   - Alert conditions
   - Notification channels

## Intelligent Log Filtering

### AI-Suggested Filters

As you investigate, Log Observer may suggest:
- **Related fields**: Tags or attributes worth filtering on
- **Common values**: Frequently occurring field values
- **Anomalous values**: Unusual field values deserving attention
- **Correlated attributes**: Fields that often appear together

### Using Suggested Filters

1. Look for filter suggestions in the UI
2. Click to apply suggested filters
3. Refine based on results
4. Save useful filter combinations

## Log Correlation with APM and Infrastructure

### Automatic Context Linking

AI helps connect logs to:
- **Traces**: Link log entries to distributed traces
- **Services**: Associate logs with APM services
- **Infrastructure**: Connect to hosts, containers, pods
- **Metrics**: Correlate log patterns with metric changes

### Following the AI Breadcrumbs

During investigations:
1. Start with a log entry or pattern
2. Look for **Related Content** suggestions
3. Jump to correlated traces, metrics, or infrastructure
4. Use Tag Spotlight to narrow down issues
5. Return to logs to verify findings

## Log Summarization and Insights

### Key Insights Panel

AI-generated insights may include:
- **Error rate summaries**: Grouped by error type
- **Service health**: Based on log severity
- **Trend analysis**: Changes in log patterns over time
- **Comparative analysis**: Current vs. baseline periods

### Example Insights

```text
⚠️ Error rate increased 340% in the last hour
   → Top error: "Database connection timeout" (1,247 occurrences)
   → Affected services: checkout-service, payment-service
   → Started at: 14:23 UTC

📊 New log pattern detected
   → "WARN: Cache miss for key {key}" appeared 892 times
   → First seen: 14:25 UTC
   → May indicate cache invalidation issue
```

## Best Practices for AI-Powered Log Analysis

### 1. Structure Your Logs
Help AI by using structured logging:
```json
{
  "timestamp": "2024-01-15T14:23:45Z",
  "level": "ERROR",
  "service": "checkout-service",
  "message": "Payment processing failed",
  "error_code": "PAYMENT_TIMEOUT",
  "transaction_id": "txn_123456",
  "customer_tier": "enterprise"
}
```

### 2. Use Consistent Field Names
- Standardize field naming across services
- Use common taxonomy (e.g., `service.name`, not `serviceName` vs `service_id`)
- Include essential context in every log

### 3. Set Appropriate Log Levels
- **DEBUG**: Detailed diagnostic info (development)
- **INFO**: General informational messages
- **WARN**: Potentially harmful situations
- **ERROR**: Error events that might still allow the app to continue
- **FATAL**: Severe errors causing premature termination

### 4. Leverage Log Sampling
For high-volume logs:
- Use AI to identify representative samples
- Focus on error logs and anomalies
- Apply intelligent sampling to reduce costs

### 5. Create Log-Based Detectors
Set up alerts for:
- Critical error patterns
- Unusual log volumes
- New error types
- Security-relevant patterns

## Use Cases

### Use Case 1: Identifying a Memory Leak
**Observation**: Pattern analysis shows increasing "GC pressure" warnings

**AI helps by**:
- Grouping GC-related log patterns
- Highlighting frequency increase
- Correlating with memory metrics
- Linking to affected service traces

### Use Case 2: Detecting Security Issues
**Observation**: New pattern "Authentication failed" appearing

**AI helps by**:
- Flagging as new/rare pattern
- Clustering by source IP
- Highlighting unusual access patterns
- Suggesting security-relevant filters

### Use Case 3: Database Performance Degradation
**Observation**: Slow query warnings increasing

**AI helps by**:
- Grouping queries by pattern
- Identifying slowest query types
- Correlating with database metrics
- Linking to application traces

## Limitations and Considerations

- **Pattern quality depends on log structure**: Unstructured logs are harder to pattern
- **High cardinality fields**: UUIDs and unique IDs can split patterns
- **Learning period**: AI needs baseline data for anomaly detection
- **Context is key**: Combine log AI with other observability signals

{{% notice title="Tip" style="info" icon="lightbulb" %}}
The most effective log analysis combines AI-powered pattern detection with your domain knowledge. Use AI to surface the signals, then apply your expertise to interpret them.
{{% /notice %}}

## Next Steps

Now that you understand AI capabilities in Log Observer, let's explore the APM AI Assistant for application troubleshooting.
