---
title: Getting-Started
linkTitle: 01-Getting-Started
weight: 1
---

During this technical Application Security for Observability workshop, you will explore runtime vulnerability detection, threat-informed prioritization, and SecOps integration using the pre-provisioned **Astronomy Shop** demo application in Splunk Observability Cloud.

To simplify the workshop modules, a shared demo tenant (**Splunk Show US** or **Splunk Show EU**) is provided. The tenant is pre-configured with APM-instrumented microservices that emit Application Security telemetry — runtime vulnerabilities, library inventory, and  attack events — without requiring you to deploy additional agents beyond existing Observability instrumentation.

This workshop introduces you to the benefits of embedding application security inside Observability workflows. By the end of these modules, you will understand how engineering and security teams can share one runtime view of risk, prioritize beyond CVSS alone, and feed findings into existing SOC tools.

---

## 1.1 Access Splunk Observability Cloud

1. Open your browser and sign in to **Splunk Workshop Realm** (credentials provided by your workshop facilitator).
2. Confirm you land on the **Splunk Observability Cloud** home experience.
3. From the left navigation, expand **APM**.

---

## 1.2 Setting the workshop context

1. Note the workshop **environment** you will use: `astronomy-shop-*`.
2. Note the primary **service** for deep-dive exercises: `ad`.

---

## What you learned

- How to access the workshop tenant and confirm Application Security entitlements.
- Which core capabilities you will exercise across the remaining modules.
- Which environment and service anchor the workshop walkthrough.

**Next:** [Runtime Vulnerability Inventory →](02-runtime-vulnerability-inventory.md)
