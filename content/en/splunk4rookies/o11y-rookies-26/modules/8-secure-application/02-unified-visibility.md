---
title: 2. Unified Visibility
weight: 2
---

## Why Unified Visibility Matters

When reliability and security live in separate tools, prioritization conversations stall. SREs ask *what broke?* while AppSec asks *what is exploitable?* and neither view shows services that are simultaneously unhealthy and high-risk.

Splunk Secure Application surfaces vulnerability and attack summaries alongside golden signals on **APM Overview**, **Service Map**, and the **per-service Application Security** workspace. Engineering, application security, and SecOps can share one runtime view without a duplicate agent or workflow.

### Security posture on APM Overview

We are bringing security together with reliability, allowing teams to review Application Security risks in the same place they understand application performance and behavior

{{% notice title="Exercise" style="green" icon="running" %}}

1. Make the navigation pane size smaller if needed by clicking on the Hamburger icon **(1)**
2. Navigate to **APM → Overview (2)**.
![apm](../images/02-overview.webp)

3. Set the workshop **Environment** filter to **[NAME OF WORKSHOP]-workshop (1)**. 
4. Close the **APM Overview** pane **(2)**
5. Scroll to the **Services (3)** tab.

Observe each service row and find the **ad** Service **(4)**: alongside standard health metrics, you should see runtime vulnerability and threat profile summaries for instrumented services- counts of critical and high CVEs and attacks **(5)**.

![apm](../images/services.webp)
{{% /notice %}}

### Service Map runtime security widgets

Visibility into a summarized view of the top vulnerabilities (CVE title, ID, CVSS score, libraries) and any attack activity (type and outcome)in a centralized and correlated view of a service.

{{% notice title="Exercise" style="green" icon="running" %}}

1. Use the Navigation Pane to go to **APM → Service Map**.
2. Find the **`ad` (1)** service in the map.
3. Click the **`ad` (1)** node in the service map.
4. Scroll to the **Runtime Vulnerabilities (2)** and **Attacks (3)** widgets (right-hand side of screen).

![apm](../images/02-servicemap.webp)
{{% /notice %}}

(Optional) - Drill into a vulnerability or attack detail (from the relevant widget) to review the navigation path.

{{% notice title="Note" style="info" %}}
This view highlights Blast-radius thinking where issues are framed next to all related dependencies, application traffic and performance patterns.
{{% /notice %}}

### What you learned

- How to correlate service health with vulnerability and threat profiles on APM Overview.
- How Service Map widgets frame security issues in topology context.
- How per-service Application Security keeps triage inside the APM workspace.
