---
title: Modernizing Defenses
linkTitle: 08-Modernizing-Defenses
weight: 8
---

## Why integration completes the modernization story

Detecting vulnerabilities and attacks inside Observability is only half the modernization journey. SecOps teams live in SIEM workflows — if findings do not reach those tools, security reverts to duplicate ticketing and stale exports.

Splunk Secure Application closes the loop with **notification rules** that stream runtime findings to Splunk Enterprise Security and other supported destinations, using credentials managed through your organization's secrets practices.

---

## 7.4 Connect to SecOps [Review]

If your tenant has a pre-provisioned notification integration, note that exploit events can stream to **Splunk Enterprise Security** in real time. You will configure this explicitly in the next module.

![apm](./images/06-notification.png)

> *"SecOps gets these events with full context — no duplicate workflow."*

---

## 8.1 Security notifications and SIEM integration

1. Navigate to **APM → Application Security → Notifications**.
2. Review any existing notification rules (the demo tenant may have a pre-provisioned Splunk ES integration).
3. Click **Create Notification Rule** to walk through the configuration flow:

| Step | Action |
|------|--------|
| **Trigger** | Select vulnerability or exploit event types |
| **Destination** | Choose supported integration (e.g., Splunk ES HTTP Event Collector) |
| **Credentials** | Reference vault-managed secrets |

> *"Single pipeline from runtime findings to SOC visibility."*

---

## What you learned

- How notification rules feed Observability-native findings into Splunk ES and other SOC tools.
- How to discuss the block-attacks roadmap without overstating current availability.
- How modernized defenses combine runtime detection with existing SecOps workflows.

**Next:** [Conclusion →](09-conclusion.md)
