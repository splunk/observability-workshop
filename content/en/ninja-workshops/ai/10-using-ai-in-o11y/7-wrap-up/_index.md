---
title: Wrap-Up and Next Steps
linkTitle: 7. Wrap-Up
weight: 7
---

## Workshop Summary

Congratulations! You've completed the "Using AI in Splunk Observability Cloud" workshop. Let's recap what you've learned about AI and ML capabilities in the platform.

## Key Takeaways

### 1. Related Content
- AI surfaces contextually relevant dashboards, detectors, and resources
- Accelerates navigation and discovery during investigations
- Learns from usage patterns and metadata relationships
- **Best practice**: Use consistent tagging and naming conventions

### 2. AutoDetect and ML-Driven Detectors
- Machine learning automatically creates intelligent detectors
- Adapts to your environment's unique patterns and seasonality
- Reduces alert noise with dynamic thresholds
- **Best practice**: Allow 1-2 weeks for baseline establishment

### 3. Tag Spotlight
- AI-powered root cause analysis across all tag dimensions
- Automatically identifies which tags contribute to performance issues
- Saves hours of manual filtering and investigation
- **Best practice**: Apply comprehensive, consistent tags to all resources

### 4. Log Observer AI
- Pattern detection groups similar logs automatically
- Anomaly detection highlights unusual log entries
- Intelligent filtering suggests relevant fields
- **Best practice**: Use structured logging with consistent field names

### 5. APM AI Assistant
- Intelligent guidance for troubleshooting application issues
- Automatic bottleneck and anomaly detection in traces
- Natural language insights and summaries
- **Best practice**: Enrich traces with comprehensive tags and attributes

### 6. Predictive Analytics
- ML models forecast future trends and capacity needs
- Proactive identification of potential issues
- Traffic forecasting for capacity planning
- **Best practice**: Maintain consistent historical data for accurate predictions

## The AI-Powered Investigation Workflow

Here's how all these AI features work together:

```text
1. Issue Detected
   ├─→ AutoDetect ML Detector triggers alert
   └─→ Anomaly clearly identified with dynamic baseline

2. Context Gathering
   ├─→ Related Content surfaces relevant dashboards
   ├─→ APM AI Assistant provides service health summary
   └─→ Log Observer AI shows correlated log patterns

3. Root Cause Analysis
   ├─→ Tag Spotlight identifies problematic tag values
   ├─→ APM AI analyzes traces and highlights bottlenecks
   └─→ Log patterns confirm findings

4. Impact Assessment
   ├─→ AI estimates scope (which customers/regions affected)
   ├─→ Historical comparison shows severity
   └─→ Dependency analysis shows downstream impact

5. Resolution
   ├─→ AI suggests potential fixes based on similar past issues
   ├─→ Monitor AI metrics to confirm resolution
   └─→ AI learns from the incident for future detection
```

## Maximizing AI Effectiveness

### Data Quality is Key

AI is only as good as the data you provide. Ensure:

- **Comprehensive tagging**: Tag all resources consistently
- **Rich metadata**: Include business and technical context
- **Structured logs**: Use JSON or key-value formatted logs
- **Complete traces**: Instrument all services and dependencies
- **Consistent naming**: Use standard naming conventions

### Start Simple, Scale Up

1. **Begin with one AI feature**: Master AutoDetect or Tag Spotlight first
2. **Validate and tune**: Review alerts and adjust sensitivity
3. **Add more features**: Gradually incorporate additional AI capabilities
4. **Integrate workflows**: Combine multiple AI features in investigations
5. **Automate**: Build runbooks and automation based on AI insights

### Continuous Improvement

- **Review AI suggestions regularly**: Are they accurate and helpful?
- **Tune sensitivity levels**: Adjust based on alert quality
- **Expand tagging**: Add new dimensions as you discover their value
- **Update baselines**: Ensure ML models reflect current normal
- **Share knowledge**: Document patterns AI helps you discover

## Common Pitfalls to Avoid

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Insufficient historical data | Poor baseline, inaccurate anomaly detection | Wait 1-2 weeks before judging effectiveness |
| Inconsistent tagging | Tag Spotlight can't correlate properly | Standardize tag names and values |
| Too-high sensitivity | Alert fatigue from false positives | Start with medium, tune based on results |
| Ignoring AI suggestions | Missing valuable insights | Investigate suggestions, provide feedback |
| Unstructured logs | Limited pattern detection capability | Migrate to structured logging formats |
| Over-reliance on AI | Missing context-specific issues | Combine AI insights with domain expertise |

## Measuring AI Impact

Track these metrics to measure AI effectiveness:

### Detection Metrics
- **MTTD (Mean Time to Detect)**: Are you finding issues faster?
- **False positive rate**: Are AutoDetect alerts accurate?
- **Coverage**: What percentage of incidents were AI-detected?

### Investigation Metrics
- **MTTR (Mean Time to Resolve)**: Are you resolving faster?
- **Time to root cause**: How quickly does Tag Spotlight identify the issue?
- **Investigation steps**: Fewer manual steps needed?

### Efficiency Metrics
- **Alerts reviewed**: More signal, less noise?
- **Dashboard usage**: Finding right dashboards faster?
- **Team velocity**: Solving more issues with same resources?

## Additional Resources

### Documentation
- [Splunk Observability Cloud Documentation](https://docs.splunk.com/observability)
- [AutoDetect Documentation](https://docs.splunk.com/observability/alerts-detectors-notifications/autodetect.html)
- [Tag Spotlight Guide](https://docs.splunk.com/observability/apm/tag-spotlight.html)
- [Log Observer Documentation](https://docs.splunk.com/observability/logs/intro-logconnect.html)

### Training and Certification
- Splunk Observability Cloud Certification
- Advanced APM Training
- ML and AI in Observability webinars

### Community
- Splunk Community Forums
- Splunk Observability Cloud User Group
- Splunk Answers

### Stay Updated
- Subscribe to Splunk product updates
- Follow Splunk AI/ML feature releases
- Join preview programs for new AI capabilities

## Hands-On Practice

### Next Steps for Learning

1. **Create AutoDetect detectors** for your critical services
2. **Configure Tag Spotlight** with Troubleshooting MetricSets
3. **Explore log patterns** in your actual log data
4. **Build AI-aware runbooks** that leverage these features
5. **Share with your team** and establish best practices

### Challenge Exercises

Ready for more? Try these advanced exercises:

#### Challenge 1: Build an AI-Powered Runbook
Create a runbook that combines multiple AI features:
- AutoDetect detector triggers
- Tag Spotlight identifies scope
- Related Content finds relevant dashboards
- Log Observer AI confirms root cause

#### Challenge 2: Optimize Your Tagging Strategy
- Audit current tags across services
- Identify gaps where Tag Spotlight would struggle
- Implement additional dimensions
- Measure improvement in investigation speed

#### Challenge 3: Tune ML Detectors
- Deploy AutoDetect for a critical metric
- Monitor for 2 weeks
- Analyze alert quality (true vs. false positives)
- Adjust sensitivity and compare results

#### Challenge 4: Create AI-Enhanced Dashboards
- Build a dashboard combining:
  - ML-predicted values
  - Anomaly indicators
  - Tag Spotlight insights
  - Related Content links

## Providing Feedback

Your feedback helps improve AI features:

- Report inaccurate AI suggestions through Splunk Support
- Share success stories with your Splunk account team
- Participate in preview programs for new AI capabilities
- Contribute to community discussions

## Thank You!

Thank you for participating in this workshop. AI and ML are transforming observability, making it easier to manage complex systems at scale. By mastering these tools, you're positioning yourself and your organization for success in modern, cloud-native environments.

### Questions?

- Reach out to your Splunk account team
- Visit [Splunk Community](https://community.splunk.com/)
- Check [Splunk Docs](https://docs.splunk.com/)

{{% notice title="Next Workshop" style="primary" icon="forward" %}}
Ready for more? Check out other [Splunk4Ninjas workshops](/ninja-workshops/) to deepen your expertise in specific areas of Splunk Observability Cloud.
{{% /notice %}}

---

**Workshop completed!** We hope you found this valuable. Now go forth and let AI enhance your observability practice!
