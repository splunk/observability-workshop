---
title: Tag Spotlight - AI-Powered Root Cause Analysis
linkTitle: 4. Tag Spotlight
weight: 4
---

## What is Tag Spotlight?

Tag Spotlight is an AI-powered analytics feature that helps you quickly identify the root cause of performance issues by automatically analyzing patterns across your tags and metadata. Instead of manually filtering through hundreds of tag combinations, Tag Spotlight uses machine learning to highlight which tag values are most strongly correlated with performance degradations.

## The Problem Tag Spotlight Solves

Imagine you have a service with:
- 10 different regions
- 5 availability zones per region
- 20 different service endpoints
- 3 deployment versions

That's potentially 3,000 different combinations to check manually! Tag Spotlight automatically analyzes all combinations and surfaces the problematic ones.

## How Tag Spotlight Works

Tag Spotlight uses several analytical techniques:

1. **Statistical Analysis**: Compares performance across all tag values
2. **Pattern Recognition**: Identifies unusual patterns in multi-dimensional data
3. **Contribution Analysis**: Calculates which tags contribute most to issues
4. **Correlation Scoring**: Ranks tags by their relevance to the problem

## Accessing Tag Spotlight

Tag Spotlight is available in two main areas:

### In APM Service Maps
1. Navigate to **APM** → **Services**
2. Select a service experiencing issues
3. Click on **Tag Spotlight** in the troubleshooting panel

### In Troubleshooting MetricSets
1. Create or access a Troubleshooting MetricSet (TMS)
2. Tag Spotlight is built into the TMS analysis view

## Hands-On Exercise: Using Tag Spotlight

{{% notice title="Exercise" style="primary" icon="tasks" %}}

### Step 1: Access Tag Spotlight in APM

1. Go to **APM** → **Services**
2. Select a service with multiple tags (e.g., different regions, versions, or endpoints)
3. Look for the **Tag Spotlight** or **Troubleshooting** section

### Step 2: Analyze the Results

Tag Spotlight will show you:
- **Tags ranked by contribution** to performance issues
- **Comparison charts** showing performance by tag value
- **Contribution percentage** for each tag
- **Statistical significance** indicators

### Step 3: Interpret the Findings

Look for:
- **High contribution tags**: Tags at the top have the most impact
- **Outlier values**: Specific tag values performing differently
- **Time correlation**: When did the divergence start?

### Step 4: Drill Down

1. Click on a highlighted tag value to filter the view
2. Examine the specific traces or metrics for that tag
3. Compare with well-performing tag values
4. Identify the root cause (code, infrastructure, configuration)

{{% /notice %}}

## Understanding Tag Spotlight Results

### Contribution Score
Shows what percentage of the performance issue is associated with each tag:

```text
Region: us-west-2    → 78% contribution
Version: v2.3.1      → 45% contribution
Endpoint: /checkout  → 23% contribution
```

Higher percentages indicate stronger correlation with the issue.

### Statistical Significance

Tag Spotlight also considers:
- **Sample size**: Are there enough data points?
- **Variance**: How consistent is the pattern?
- **Baseline comparison**: How does it compare to normal?

## Real-World Use Cases

### Use Case 1: Regional Performance Degradation
**Symptom**: Overall latency increased by 300ms

**Tag Spotlight reveals**:
- `aws_region: eu-central-1` → 92% contribution
- Other regions performing normally

**Root cause**: Database replication lag in EU region

### Use Case 2: Version Rollout Issues
**Symptom**: Error rate spiked after deployment

**Tag Spotlight reveals**:
- `version: v3.0.1` → 85% contribution
- `endpoint: /api/search` → 67% contribution

**Root cause**: New search endpoint introduced a memory leak

### Use Case 3: Customer Segment Impact
**Symptom**: Increased checkout latency

**Tag Spotlight reveals**:
- `tenant: enterprise-tier` → 71% contribution
- `payment_method: invoice` → 58% contribution

**Root cause**: New billing validation slowing down enterprise invoicing

## Best Practices for Tag Spotlight

### 1. Ensure Rich Tagging
Tag Spotlight is only as good as your tags. Include:
- **Infrastructure tags**: Region, AZ, cluster, node
- **Application tags**: Version, environment, feature flags
- **Business tags**: Tenant, customer tier, product line
- **Custom dimensions**: Anything relevant to your domain

### 2. Use Consistent Tag Names
- Use standard naming conventions across services
- Avoid synonyms (e.g., don't mix `region` and `aws_region`)
- Document your tagging strategy

### 3. Combine with Other Tools
Use Tag Spotlight alongside:
- **APM traces**: Verify findings with actual trace data
- **Metrics**: Confirm patterns in time-series data
- **Logs**: Find error messages for identified tags

### 4. Create Troubleshooting MetricSets
For critical services, pre-configure Troubleshooting MetricSets with:
- Key performance indicators (latency, error rate, throughput)
- Important dimensions (region, version, endpoint)
- Appropriate baseline comparison periods

## Troubleshooting MetricSets (TMS)

TMS are custom metric aggregations designed for Tag Spotlight:

### Creating a TMS
1. Navigate to **APM** → **Troubleshooting MetricSets**
2. Click **Create Troubleshooting MetricSet**
3. Select the service and metric
4. Choose dimensions to analyze
5. Save and activate

### When to Create TMS
- **Critical services**: Services with strict SLAs
- **Complex architectures**: Services with many dimensions
- **Recurring issues**: Services with frequent performance variations
- **Multi-tenant systems**: Where customer impact varies

## Limitations and Considerations

- **Requires sufficient data**: Needs enough samples per tag value
- **Correlation ≠ Causation**: Tag Spotlight shows correlation; verify root cause
- **Tag cardinality**: Very high cardinality tags (e.g., user IDs) may not be useful
- **Time window matters**: Choose appropriate comparison periods

{{% notice title="Tip" style="info" icon="lightbulb" %}}
Tag Spotlight works best when you have a clear performance degradation period to analyze. Define your baseline and comparison windows carefully for accurate results.
{{% /notice %}}

## Next Steps

Now that you understand Tag Spotlight, let's explore AI capabilities in Log Observer.
