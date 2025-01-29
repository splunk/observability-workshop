---
title: Create a Troubleshooting MetricSet
linkTitle: 4. Create a Troubleshooting MetricSet
weight: 4
time: 5 minutes
---

## Index Tags

To use advanced features in **Splunk Observability Cloud** such as **Tag Spotlight**, we'll need to first index one or more tags.

To do this, navigate to **Settings** -> **MetricSets** and ensure the **APM** tab is selected.  Then click the **+ Add Custom MetricSet** button.

Let's index the `credit.score.category` tag by entering the following details (**note**: since everyone in the workshop is using the same organization, the instructor will do this step on your behalf):

![Create Troubleshooting MetricSet](../images/create_troubleshooting_metric_set.png)

Click **Start Analysis** to proceed.

The tag will appear in the list of **Pending MetricSets** while analysis is performed.

![Pending MetricSets](../images/pending_metric_set.png)

Once analysis is complete, click on the checkmark in the **Actions** column.

## Troubleshooting vs. Monitoring MetricSets

You may have noticed that, to index this tag, we created something called a **Troubleshooting MetricSet**. It's named this way because a Troubleshooting MetricSet, or TMS, allows us to troubleshoot issues with this tag using features such as **Tag Spotlight**.

You may have also noticed that there's another option which we didn't choose called a **Monitoring MetricSet** (or MMS).  Monitoring MetricSets go beyond troubleshooting and allow us to use tags for alerting and dashboards.  While we won't be 
exploring this capability as part of this workshop, it's a powerful feature that I encourage you to explore on your own. 
