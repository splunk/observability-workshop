---
title: Install the Solarwinds Content Pack
linkTitle: 4.1 Install the Solarwinds Content Pack
weight: 1
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px; margin-top: 25px;">
<center>
In this section you will install and configure the SolarWinds Content Pack to ingest SolarWinds alerts into ITSI, completing the two-source alert pipeline needed for cross-vendor correlation.
</center>

{{% notice title="Exercise: Install the Solarwinds Content Pack" style="primary" icon="running" %}}

**1.** In ITSI, navigate to **Configuration** > **Data Integrations**.

**2.** Under the **Alerts** section of the **Integrations library**, select **Solarwinds**.

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
The SolarWinds Content Pack includes pre-built field mappings and alert templates for ITSI
</div>

![Content Pack for Solarwinds](../../images/solarwinds-content-pack.png?width=40vw)
{{% / notice %}}
</div>

**3.** Enter `Solarwinds Alerts` for the connection title.

**4.** Use the following SPL for the search:

```text
index=netops sourcetype="solarwinds:alert:hec"
```

**5.** Click **Validate**.

**6.** Set the **Lookback period** to **5 minutes**.

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Validation confirms the search is returning SolarWinds events before saving the connection
</div>

![Validate Connection](../../images/solarwinds-validate.png?width=40vw)
{{% / notice %}}
</div>

**7.** Set **Signature** to `title`.

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
The Signature field uniquely identifies each alert type and is used for deduplication within ITSI
</div>

![Signature](../../images/solarwinds-signature.png?width=40vw)
{{% / notice %}}
</div>

**8.** Update the **Severity ID** mapping to a **Mapping rule** using **Value case mapping** as the type

**9.** Set `severity_id` **is equal to (not case sensitive)** to `1` and **then use** to `Normal`

**10.** Map the following values for the remainder of the if statement:

`severity_id` **is equal to (not case sensitive)** to `2` and **then use** to `Low`

`severity_id` **is equal to (not case sensitive)** to `3` and **then use** to `Medium`

`severity_id` **is equal to (not case sensitive)** to `4` and **then use** to `High`

`severity_id` **is equal to (not case sensitive)** to `5` and **then use** to `Critical`

And finally, set **else use this default value** to `Info`

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Map SolarWinds severity values to the ITSI severity scale so episodes display the correct priority
</div>

![Severity ID Mapping](../../images/solarwinds-severity.png?width=40vw)
{{% / notice %}}
</div>

**11.** Update the **subcomponent** to `vendor_region`.

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
The subcomponent field links each SolarWinds alert to its corresponding site, enabling cross-vendor correlation
</div>

![Subcomponent](../../images/solarwinds-subcomponent.png?width=40vw)
{{% / notice %}}
</div>

**12.** Expand **additional fields** and set the **description** to `signature`.

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Additional fields provide extra context visible when reviewing episodes in ITSI
</div>

![Additional Fields](../../images/solarwinds-additional-fields.png?width=40vw)
{{% / notice %}}
</div>

**13.** Set the Schedule to **Run Every Minute**.

**14.** Add `NY HQ`, `Store-SJC10`, and `Store-SJC12` to the **Service Association** section

**15.** Turn on the **Enable throttling** toggle

**16.** Set the **Suppress period** to every **5 minutes**

**17.** Click **Preview Results** in the upper right (**Note:** You may not get results in the preview. We will review the events during the **Create a custom NEAP** section)

**18.** Click **Save and Activate**

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Review the transformed fields in Preview Results before saving to confirm the mapping is correct
</div>

![Save and Activate](../../images/solarwinds-save-activate.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="Primary" title="Nice Job!" %}}
<div style="text-align: center;">
SolarWinds alerts are now flowing into ITSI alongside Catalyst Center events. Both sources are normalized and ready to be correlated.

In the next section you will build a custom NEAP to group alerts from both vendors into a single episode per site.
</div>
{{% / notice %}}

{{% /notice %}}
</div>
