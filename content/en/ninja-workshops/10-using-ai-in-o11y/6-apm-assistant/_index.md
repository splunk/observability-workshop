---
title: APM AI Assistant and Intelligent Troubleshooting
linkTitle: 6. APM AI Assistant
weight: 6
---

## What is the APM AI Assistant?

The APM AI Assistant is an intelligent feature that helps you troubleshoot application performance issues by providing contextual guidance, analyzing traces, and suggesting next steps during investigations. It acts as a virtual expert that understands your APM data and guides you toward solutions.

{{% notice title="Note" style="info" %}}
AI Assistant features may vary by Splunk Observability Cloud version and entitlement. Some capabilities described here may be in preview or require specific licensing.
{{% /notice %}}

## Key Capabilities

### 1. Trace Analysis
- **Automatic span analysis**: Identifies slow or problematic spans
- **Bottleneck detection**: Highlights performance bottlenecks in distributed traces
- **Error pattern recognition**: Groups and analyzes error traces
- **Dependency insights**: Understands service dependencies and call patterns

### 2. Guided Troubleshooting
- **Root cause suggestions**: Proposes likely root causes based on trace data
- **Investigation pathways**: Suggests what to examine next
- **Historical comparisons**: Compares current issues with past patterns
- **Resolution recommendations**: Offers potential fixes based on similar issues

### 3. Contextual Insights
- **Natural language summaries**: Explains complex traces in plain language
- **Impact assessment**: Estimates the scope and severity of issues
- **Service health insights**: Summarizes service performance trends
- **Anomaly explanations**: Describes why something is considered anomalous

## How AI Assistant Helps

### Scenario 1: Investigating a Slow Trace

**Traditional approach:**
1. Open trace waterfall
2. Manually scan all spans
3. Calculate durations
4. Identify slowest operations
5. Cross-reference with other traces
6. Form hypothesis about root cause

**With AI Assistant:**
1. Open trace
2. AI highlights: "Database query in checkout-service took 2.3s (95th percentile: 45ms)"
3. Suggests: "Check database index on orders table"
4. Links to similar traces with same pattern
5. Shows when pattern started

### Scenario 2: Understanding Error Patterns

**AI Assistant provides:**
- Grouping of similar errors
- Frequency analysis
- First occurrence timestamp
- Affected endpoints and services
- Common attributes across error traces
- Suggested investigation steps

## Hands-On Exercise: Using AI-Powered APM Features

{{% notice title="Exercise" style="primary" icon="tasks" %}}

### Step 1: Explore Service Insights

1. Navigate to **APM** → **Services**
2. Select a service with performance data
3. Look for AI-generated insights or summaries:
   - Service health score
   - Performance trends
   - Anomaly indicators
   - Top issues or bottlenecks

### Step 2: Analyze a Trace with AI Assistance

1. Go to **APM** → **Traces**
2. Filter for slow or error traces
3. Open a trace waterfall view
4. Look for AI-powered features:
   - Highlighted problematic spans
   - Automatic critical path identification
   - Comparison with baseline traces
   - Suggested root cause

### Step 3: Leverage Automatic Root Cause Detection

1. In the trace view, find the **Root Cause** or **Insights** panel
2. Review AI suggestions:
   - Which span is the bottleneck?
   - What changed compared to normal behavior?
   - Which tags or attributes correlate with the issue?
3. Follow the suggested investigation path
4. Drill down into the identified component

### Step 4: Use Trace Comparison

1. Select a problematic trace
2. Look for **Compare** or **Similar Traces** feature
3. AI will show:
   - Similar normal traces (baseline)
   - What's different in the slow trace
   - Statistical comparison
4. Identify the anomalous component

{{% /notice %}}

## Intelligent Trace Features

### Critical Path Highlighting

AI automatically identifies the critical path through a distributed trace:
- **Critical spans**: Spans that directly contributed to total latency
- **Parallelizable spans**: Spans that could be optimized through async processing
- **Waiting time**: Time spent waiting for downstream services

### Span Anomaly Detection

AI detects unusual spans by considering:
- **Duration**: Compared to historical baseline
- **Frequency**: How often this span appears
- **Error rate**: Errors in this span vs. normal
- **Context**: Tags and attributes that differ from norm

### Service Dependency Intelligence

AI understands your service architecture:
- **Dependency mapping**: Automatically maps service relationships
- **Impact analysis**: Predicts how service issues affect dependents
- **Circular dependency detection**: Identifies problematic call patterns
- **Optimization suggestions**: Recommends architectural improvements

## AI-Powered APM Alerts

### Smart Alert Prioritization

AI helps prioritize alerts by:
- **Business impact scoring**: Estimates user/revenue impact
- **Historical context**: Compares with past similar alerts
- **Correlation analysis**: Groups related alerts
- **Noise reduction**: Suppresses likely false positives

### Adaptive Thresholds

For APM-based detectors:
- **Dynamic baselines**: Adjusts thresholds based on traffic patterns
- **Seasonal awareness**: Accounts for time-of-day/day-of-week patterns
- **Deployment awareness**: Recognizes deployment events
- **Traffic-proportional alerting**: Adjusts for traffic volume changes

## Natural Language Capabilities

### Asking Questions (Where Available)

Some AI Assistant implementations allow natural language queries:

**Example questions:**
- "Why is checkout-service slow?"
- "What changed in the last hour?"
- "Which endpoints are experiencing errors?"
- "Show me traces from customer tier enterprise"
- "Compare current performance with last week"

**AI provides:**
- Natural language answers
- Relevant traces and metrics
- Visualization of the data
- Suggested next steps

## Best Practices for AI Assistant

### 1. Provide Rich Context
Help AI help you:
- Use descriptive span names
- Add relevant tags and attributes
- Include error details in spans
- Tag deployment events

### 2. Trust but Verify
- Use AI suggestions as starting points
- Validate findings with actual data
- Cross-reference with metrics and logs
- Apply domain knowledge

### 3. Learn from AI Patterns
- Note common root causes AI identifies
- Observe which tags are most useful
- Study the investigation paths AI suggests
- Build automation based on repeated patterns

### 4. Provide Feedback
If your AI Assistant supports feedback:
- Mark helpful suggestions
- Report incorrect analyses
- The system learns from your feedback

## Combining AI Assistant with Other AI Features

### Integrated Workflow

1. **Alert fires** (AutoDetect ML detector)
2. **Tag Spotlight** narrows down the problem
3. **APM AI Assistant** analyzes affected traces
4. **Related Content** surfaces relevant dashboards
5. **Log Observer AI** shows correlated log patterns
6. **Resolution** with full context

### Example Investigation Flow

```text
Alert: "Latency increased on payment-service"
   ↓
Tag Spotlight: "Region: us-west-1 (87% contribution)"
   ↓
APM AI: "Database span duration increased 450%"
   ↓
Trace Analysis: "Connection pool exhausted"
   ↓
Log Observer AI: Pattern "Connection pool timeout" increased
   ↓
Related Content: Dashboard "Database Connection Health"
   ↓
Root Cause: Recent traffic spike exceeded DB connection limits
```

## Limitations and Considerations

- **Learning period**: AI needs historical data for comparisons
- **Data quality**: Accuracy depends on trace completeness and tagging
- **Context boundaries**: AI doesn't know your business logic
- **Preview features**: Some capabilities may be evolving
- **Privacy**: Ensure sensitive data is not included in trace attributes

{{% notice title="Tip" style="info" icon="lightbulb" %}}
The APM AI Assistant is most effective when your applications are well-instrumented with comprehensive tags and attributes. The richer your trace data, the better the AI insights.
{{% /notice %}}

## Next Steps

Let's wrap up the workshop with a summary and additional resources.
