---
title: Configure SolarWinds Notifications
linkTitle: 4. Configure SolarWinds Notifications
weight: 4
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px;">

## Adding a Second Alert Source

A key goal of this workshop is demonstrating cross-vendor alert correlation. Cisco Catalyst Center covers your Cisco infrastructure, but many enterprise networks also rely on third-party monitoring tools like SolarWinds to track non-Cisco devices, WAN links, and broader network health metrics. When both sources raise alerts about the same site or time window, ITSI should be able to group them into a single episode rather than generating separate noise for each.

The **SolarWinds Add-on for Splunk** can provide deep asset context, but for this use case SolarWinds alerts are delivered directly to the Splunk HTTP Event Collector. The Content Pack for Cisco Enterprise Networks includes a pre-built integration template that normalizes these alerts so they are recognized by ITSI in the same way as Catalyst Center alerts.

In this section you will install the SolarWinds Content Pack and configure the inbound notification connection, completing the two-source alert pipeline that the NEAP in the next section will correlate.

## What You'll Do in This Section

By the end of this section you will have:

- Installed the **SolarWinds Content Pack** and configured the inbound notification connection
- Verified that SolarWinds alerts are flowing into ITSI as normalized notable events

</div>
