---
title: Configure Solarwinds Notifications
linkTitle: 4. Configure Solarwinds Notifications
weight: 4
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---


## Adding a Second Alert Source

A key goal of this workshop is demonstrating cross-vendor alert correlation. Cisco Catalyst Center covers your Cisco infrastructure, but many enterprise networks also rely on third-party monitoring tools like Solarwinds to track non-Cisco devices, WAN links, and broader network health metrics. When both sources raise alerts about the same site or time window, ITSI should be able to group them into a single episode rather than generating separate noise for each.

The **Solarwinds Add-on for Splunk** can provide deep asset context, but for this use case Solarwinds alerts are delivered directly to the Splunk HTTP Event Collector. ITSI includes a pre-built integration template for Solarwinds that normalizes these alerts so they are recognized by ITSI in the same way as other event sources, such as Catalyst Center alerts.

In this section you will configure the **Solarwinds Inbound Notification** connection, completing the two-source alert pipeline that the **Notable Event Aggregation Policy** in the next section will correlate.

## What You'll Do in This Section

By the end of this section you will have:

- Configured the **Solarwinds Inbound Notification** connection which will create Notable Events in ITSI for these alerts
- Verified that Solarwinds alerts are flowing into ITSI as normalized notable events

