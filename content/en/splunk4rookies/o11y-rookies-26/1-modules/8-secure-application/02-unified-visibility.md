---
title: Unified Visibility
linkTitle: 02-Unified-Visibility
weight: 2
---

## Why Unified Visibility Matters

When reliability and security live in separate tools, prioritization conversations stall. SREs ask *what broke?* while AppSec asks *what is exploitable?* and neither view shows services that are simultaneously unhealthy and high-risk.

Splunk Secure Application surfaces vulnerability and attack summaries alongside golden signals on **APM Overview**, **Service Map**, and the **per-service Application Security** workspace. Engineering, application security, and SecOps can share one runtime view without a duplicate agent or workflow.

### Security posture on APM Overview

We are bringing security together with reliability, allowing teams to review Application Security risks in the same place they understand application performance and behavior

{{% notice title="Exercise" style="green" icon="running" %}}

1. Navigate to **APM → Overview**.
2. Set the **environment** filter to 'astronomy-shop-*'.
3. Scroll to the **Services** tab.

Observe each service row: alongside standard health metrics, you should see runtime vulnerability and threat profile summaries for instrumented services- counts of critical and high CVEs and attacks.

![apm](../images/02-overview.png)
{{% /notice %}}

### Service Map runtime security widgets

Visibility into a summarized view of the top vulnerabilities (CVE title, ID, CVSS score, libraries) and any attack activity (type and outcome)in a centralized and correlated view of a service.

{{% notice title="Exercise" style="green" icon="running" %}}

1. Navigate to **APM → Service Map**.
2. Open the **Services** filter and select **'ad'**.
3. Click the **`ad`** node in the service map.
4. Scroll to the **Runtime Vulnerabilities** and **Attacks** widgets (right-hand side of screen).

![apm](../images/02-servicemap.png)
{{% /notice %}}

(Optional) - Drill into a vulnerability or attack detail (from the relevant widget) to review the navigation path.

{{% notice title="Note" style="info" %}}
This view highlights Blast-radius thinking where issues are framed next to all related dependencies, application traffic and performance patterns.
{{% /notice %}}

### What you learned

- How to correlate service health with vulnerability and threat profiles on APM Overview.
- How Service Map widgets frame security issues in topology context.
- How per-service Application Security keeps triage inside the APM workspace.
