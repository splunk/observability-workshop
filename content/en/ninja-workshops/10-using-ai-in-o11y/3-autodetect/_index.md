---
title: AutoDetect and ML-Driven Anomaly Detection
linkTitle: 3. AutoDetect
weight: 3
---

## What is AutoDetect?

AutoDetect is a machine learning-powered feature that automatically creates intelligent detectors for your metrics without requiring manual threshold configuration. Instead of guessing at static thresholds, AutoDetect learns the normal behavior patterns of your metrics and alerts when deviations occur.

## How AutoDetect Works

AutoDetect uses several ML techniques:

1. **Baseline Learning**: Analyzes historical data to understand normal patterns
2. **Seasonal Awareness**: Recognizes daily, weekly, and monthly patterns
3. **Dynamic Thresholds**: Adjusts sensitivity based on metric volatility
4. **Contextual Anomalies**: Considers multiple signals together for smarter alerting

## Types of ML-Powered Detectors

### Sudden Change Detection
Alerts when a metric suddenly spikes or drops beyond learned patterns.

### Historical Anomaly Detection
Compares current values against historical norms, accounting for time-of-day and day-of-week patterns.

### Resource Detectors
Pre-configured ML detectors for common infrastructure resources (CPU, Memory, Disk).

## Hands-On Exercise: Create an AutoDetect Detector

{{% notice title="Exercise" style="primary" icon="tasks" %}}

### Step 1: Navigate to Detector Creation

1. Go to **Alerts & Detectors** → **Detectors**
2. Click **New Detector**
3. Select **AutoDetect** or **From Template**

### Step 2: Select a Metric

1. Choose a metric with consistent traffic (e.g., `demo.trans.latency` or `cpu.utilization`)
2. Add any relevant filters (environment, service, etc.)
3. Review the chart to ensure data is flowing

### Step 3: Configure ML Settings

1. Select **Sudden Change** or **Historical Anomaly** mode
2. Adjust the sensitivity:
   - **Low**: Fewer alerts, only major deviations
   - **Medium**: Balanced approach (recommended)
   - **High**: More sensitive, catches subtle changes
3. Set the observation window (how much history to consider)

### Step 4: Configure Alert Settings

1. Set the alert severity (Critical, Warning, Info)
2. Configure notification recipients
3. Customize the alert message
4. Review and activate the detector

{{% /notice %}}

## Understanding ML Detector Behavior

### Learning Period
AutoDetect detectors need time to establish baselines:

- **Minimum**: 24 hours of data
- **Recommended**: 1-2 weeks for stable baselines
- **Seasonal patterns**: 4+ weeks for weekly patterns

### Sensitivity Tuning

The sensitivity setting controls how aggressive the detector is:

```text
Low Sensitivity    → Fewer false positives, might miss subtle issues
Medium Sensitivity → Balanced (default)
High Sensitivity   → Catches more anomalies, more noise possible
```

## Best Practices

1. **Start with Medium Sensitivity**: Adjust based on alert volume
2. **Use Appropriate Metrics**: AutoDetect works best with:
   - Metrics with clear patterns (latency, request rates)
   - Stable, continuous data streams
   - Sufficient historical data
3. **Group by Relevant Dimensions**: Use tags to create focused detectors
4. **Allow Learning Time**: Don't judge effectiveness in the first 48 hours
5. **Review and Tune**: Regularly review triggered alerts and adjust sensitivity

## When to Use AutoDetect vs. Static Thresholds

| Use AutoDetect When... | Use Static Thresholds When... |
|------------------------|-------------------------------|
| Metrics have natural variance | You have known, fixed limits |
| Patterns change over time | Requirements are regulatory/contractual |
| Traffic is seasonal or cyclical | Simple binary conditions (up/down) |
| You don't know the "right" threshold | Thresholds are well-established |

## Monitoring AutoDetect Performance

After creating ML detectors:

1. **Review Alert History**: Check for false positives/negatives
2. **Adjust Sensitivity**: Fine-tune based on alert quality
3. **Update Baselines**: ML models automatically adapt to changes
4. **Compare with Traditional Detectors**: See if ML catches issues earlier

{{% notice title="Tip" style="info" icon="lightbulb" %}}
AutoDetect is particularly effective for metrics that vary by time of day or day of week, such as user traffic, transaction volumes, and API request rates.
{{% /notice %}}

## Common Pitfalls

- **Insufficient data**: Needs enough history to learn patterns
- **Too many dimensions**: Splitting by too many tags can dilute the ML model
- **Unstable metrics**: Highly erratic metrics may produce noisy alerts
- **Recent deployments**: New services lack baseline data

## Next Steps

Now that you understand AutoDetect, let's explore Tag Spotlight for AI-powered root cause analysis.
