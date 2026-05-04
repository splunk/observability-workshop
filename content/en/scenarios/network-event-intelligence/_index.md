---
title: Network Event Intelligence with Splunk IT Service Intelligence
linkTitle: Network Event Intelligence
weight: 10
archetype: chapter
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
description: Integrate Cisco Catalyst Center, Solarwinds, and Splunk ITSI to correlate network events across vendors, reduce alert noise, and understand the business impact of network incidents.
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px;">

## Welcome!

This hands-on workshop is designed specifically for anyone looking to effectively demonstrate and position the power of IT Service Intelligence (ITSI) for Network Event Intelligence use cases. Participants will gain practical experience integrating these platforms, focusing on real-world scenarios and use cases that resonate with potential clients. The workshop emphasizes the correlation of multiple sources across the Cisco Networking portfolio and 3rd party monitoring solutions, enabling Solution Architects to confidently showcase how Splunk can address the critical customer challenge of effective network event correlation.

## Introduction and Overview

In today's complex IT landscape, ensuring the performance and availability of applications and services is paramount. This workshop will introduce you to a powerful combination of tools including Cisco Catalyst Center, Solarwinds, Splunk Enterprise, and Splunk IT Service Intelligence (ITSI) that work together to provide comprehensive monitoring and alerting capabilities.

### The Challenge of Modern Network Observability

Modern enterprise networks span an ever-growing mix of vendors and platforms ranging from Cisco solutions like Cisco Catalyst Center, Meraki, ThousandEyes to 3rd-party tools like SolarWinds, HPE Aruba Networking, and Palo Alto Networks. Each generates its own alerts, in its own format, delivered through its own console. When a network event occurs, operations teams are left manually hunting across disconnected tools to piece together what happened, where it started, and which services or users are affected. Without a common correlation layer, alert noise is high, investigation is slow, and the business impact of network incidents remains invisible until customers start calling.

### The Solution: Network Event Intelligence

A comprehensive Network Intelligence strategy requires integrating data from various sources and correlating it to gain actionable insights. This workshop will demonstrate how the Splunk Platform and ITSI work together to achieve this.

* **Cisco Enterprise Networks:** Provides top datasources from the Cisco Data Fabric such as Catalyst Center, Meraki, and ThousandEyes.

* **Splunk:** Acts as the central platform for log analytics and the collection and correlation of data from any source, enabling powerful search, visualization, and correlation capabilities. Splunk provides a holistic view of your IT environment.

* **Splunk IT Service Intelligence (ITSI):** Provides service intelligence by correlating data from all the other platforms. ITSI allows you to define services, map dependencies, and monitor Key Performance Indicators (KPIs) that reflect the overall health and performance of those services. ITSI is essential for understanding the *business impact* of IT issues.

## Workshop Objectives

By the end of this workshop, you will have configured 
- ITSI to monitor network health from multiple locations using data from Cisco Catalyst Center
- Inbound notifications from both Catalyst Center and Solarwinds for correlating alerts
- Correlated episodes using notifications from both Catalyst Center and Solarwinds
- Episodes that automatically resolve when the health of degraded services return to normal

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
The easiest way to navigate through this workshop is by using:

* the left/right arrows (**<** | **>**) on the top right of this page
* the left (◀️) and right (▶️) cursor keys on your keyboard
  {{% /notice %}}
  
</div>