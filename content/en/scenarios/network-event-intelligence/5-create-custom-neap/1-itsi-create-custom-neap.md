---
title: ITSI Create Custom NEAP
linkTitle: 5.1 ITSI Create Custom NEAP
weight: 1
time: 10 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

Because you configured the inbound notification rules for Catalyst Center and Solarwinds in the previous step, you should soon see episodes being generated for those sources. You may notice ITSI is applying the default aggregation policy, which provides quick aggregation value by grouping alerts by source. However, for this dataset we want episodes grouped by location. This enables correlation between Catalyst Center and SolarWinds alerts, a differentiating feature of ITSI event management.

{{% notice title="Exercise: Create a Custom NEAP" style="primary" icon="running" %}}

**1.** Navigate to **Alerts and Episodes**. Review any recently created episodes. Notice that they are using the **Default Aggregation Policy** to group the alerts. As the break scenario in this environment is on a 30 minute cycle (15 minutes healthy, 15 minutes unhealthy), it may take up to 15 minutes before you see episodes.

{{% notice style="Info" %}}
The Alerts and Episodes view shows all current notable events and the episodes they have been grouped into

![Alerts and Episodes](../../images/alerts-and-episodes.png?width=40vw)
{{% / notice %}}

**2.** Navigate to **Configuration** > **Event Management** > **Notable Event Aggregation Policies**.

**3.** Click **Create Notable Event Aggregation Policy** in the upper right corner.

{{% notice style="Info" %}}
ITSI includes several built-in policies. You will create a new one specifically for grouping network site alerts from multiple vendors

![Create NEAP](../../images/create-neap.png?width=40vw)
{{% / notice %}}

**4.** In the **Filtering Criteria and Instructions** add `orig_sourcetype` matches `cisco:dnac:issue`.

**5.** Click **Add Rule (OR)** and enter `orig_sourcetype` matches `solarwinds:alert:hec`.

**6.** In the **Group alerts episodes based on...** replace `host` with `subcomponent`.

**7.** Replace the default **Break Episode** stanza with **If the flow of events into the episode is paused for** and use **600 seconds**.

{{% notice style="info" %}}
When the breaking criteria are met, the current episode can no longer have any events added to it and a new episode starts with the next notable event. For example: Break episode if the following event occurs: message matches **status** `Normal`. This rule breaks an episode once it receives a normal notable event, indicating the problem is resolved.
{{% /notice %}}

{{% notice style="Info" %}}
Filtering criteria define which alert sources this policy applies to, and the grouping field determines how episodes are formed

![Filtering Criteria](../../images/filtering-criteria.png?width=40vw)
{{% / notice %}}

{{% notice style="info" %}}
Event iQ in IT Service Intelligence (ITSI) uses machine learning algorithms to compare field values and correlate notable events into episodes. Instead of defining manual attributes to correlate events, you can automatically identify the correct attributes to use in your grouping policies. After you onboard alerts to ITSI, you can set criteria to filter alerts, and use Event iQ to create your event correlation policies based on an analysis of historical event data.

Using Event iQ in your workflow helps you quickly set up automated alert monitoring, reduce alert noise, and execute event actions. Additionally, algorithms can be continuously tuned to fit your environment's alerting needs.
{{% /notice %}}

**8.** Expand **Episode Information**.

* Set **Episode Title** to **Static Value** and enter `Network Issue Impacting: %subcomponent%`
* Set **Episode Severity** to **Same as the highest Severity**
* Click **Next** in the upper right

{{% notice style="Info" %}}
Using %subcomponent% in the episode title automatically populates the affected site name in every episode created by this policy

![Episode Information](../../images/episode-information.png?width=40vw)
{{% / notice %}}

**9.** Configure the **Action Rules**.

{{% notice style="info" %}}
Set up action rules within an aggregation policy to take automated actions when an episode's activation criteria are met. Action rules are optional and you can define more than one per aggregation policy.
{{% /notice %}}

* Add rule: If **all event severities are** choose **Normal** from the dropdown and enter **60 seconds**
* Then **Change severity to** choose **Normal** from the dropdown and select **Change status to** > **Resolved**
* Click **Next**

{{% notice style="Info" %}}
Action rules enable automatic episode resolution when all contributing alerts return to normal, reducing manual triage

![Action Rules](../../images/action-rules.png?width=40vw)
{{% / notice %}}

**10.** Enter `Network Events by Location` for the **Policy Title**. Click **Enabled** for the Status. Click **Next**.

{{% notice style="Info" %}}
Enable the policy immediately so it begins grouping incoming alerts as soon as it is saved

![Policy Title](../../images/policy-title.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="Nice Job!" %}}
Your custom NEAP is now active. Catalyst Center and SolarWinds alerts that share the same site will be grouped into a single episode titled with the affected location.

Continue to the next section to validate the full end-to-end configuration.
{{% / notice %}}

{{% /notice %}}
