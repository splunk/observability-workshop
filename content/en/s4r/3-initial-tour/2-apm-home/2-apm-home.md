---
title: Application Performance Monitoring Home page
linkTitle: 2. APM Home Page 
weight: 2
---
 
{{% button icon="clock" color="#ed0090" %}}2 minutes{{% /button %}}

Click **APM** in the main menu, the APM Home Page is made up of 3 distinct sections:

![APM page](../images/apm-main.png)

1. **Onboarding Pane Pane:** Training videos and links to documentation to get you started with Splunk APM.
2. **APM Overview Pane:** Real-time metrics for the Top Services and Top Business Workflows.
3. **Functions Pane:** Links for deeper analysis of your services, tags, traces, database query performance and code profiling.

{{% notice title=" About Environments" style="info" %}}
To easily differentiate between multiple applications, Splunk uses **environments**. The naming convention for workshop environments is **[NAME OF WORKSHOP]-workshop**. Your instructor will provide you with the correct one to select.

{{% /notice %}}

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* Verify that the time window we are working with is set to the last 15 minutes (**-15m**).
* Change the environment to the workshop one by selecting its name from the drop-down box and make sure that is the only one selected.
* Click on the Explore Tile in the Function Pane. This will bring us to the automatically generated map of our services. This map shows how the services interact together based on the trace data being sent to Splunk Observability Cloud.

{{% /notice %}}

We will revisit APM in more detail later. Next, let's check out Real User Monitoring (RUM).
