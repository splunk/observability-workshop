---
title: Related Content
linkTitle: 2. Related Content
weight: 2
---

## What is Related Content?

Related Content is an AI-powered feature in Splunk Observability Cloud that automatically surfaces contextually relevant information as you navigate through your observability data. Instead of manually searching for related dashboards, detectors, or traces, the AI engine analyzes your current context and presents the most relevant resources.

## How Related Content Works

The AI engine considers multiple factors:

- **Current viewing context**: What service, host, or metric you're examining
- **Metadata and tags**: Common dimensions and properties
- **User behavior patterns**: What other users typically view in similar contexts
- **Temporal relationships**: Time-based correlations between resources
- **Semantic relationships**: Named entities and their logical connections

## Key Benefits

1. **Faster Navigation**: Jump directly to related resources without manual searching
2. **Discover Hidden Relationships**: Find connections you might not have known existed
3. **Streamlined Investigations**: Follow the AI-suggested path during incident response
4. **Knowledge Discovery**: Learn about dashboards and detectors created by other teams

## Where You'll Find Related Content

Related Content appears in several places throughout the platform:

- **Dashboard pages**: See related dashboards and detectors
- **APM service pages**: View related traces, logs, and infrastructure
- **Detector pages**: Find related dashboards and other detectors
- **Chart pages**: Discover related visualizations and metrics

## Hands-On Exercise

{{% notice title="Exercise" style="primary" icon="tasks" %}}

### Explore Related Content in APM

1. Navigate to **APM** → **Services** in your Splunk Observability Cloud organization
2. Select any service from the list
3. Look for the **Related Content** section (typically on the right sidebar or bottom of the page)
4. Notice the types of resources suggested:
   - Related dashboards
   - Related detectors
   - Connected services
   - Infrastructure components
5. Click on one of the suggested items and observe how the context changes
6. Check the Related Content in the new view - notice how it adapts to your current context

{{% /notice %}}

## Understanding the Recommendations

When you see Related Content suggestions, consider:

- **Why is this related?**: Look at common tags, naming patterns, or dependencies
- **Strength of relationship**: Items at the top are typically more strongly related
- **Coverage**: If you don't see expected content, it may need better tagging or metadata

## Best Practices

To get the most from Related Content:

1. **Use consistent naming conventions** for services, dashboards, and detectors
2. **Apply comprehensive tags** to your resources
3. **Leverage custom properties** to create semantic relationships
4. **Follow the suggestions** during investigations to discover new insights

{{% notice title="Tip" style="info" icon="lightbulb" %}}
The more you use Splunk Observability Cloud with consistent tagging and naming, the better the Related Content AI becomes at surfacing relevant information.
{{% /notice %}}

## Next Steps

Now that you understand Related Content, let's explore how AutoDetect uses ML to automatically create intelligent detectors.
