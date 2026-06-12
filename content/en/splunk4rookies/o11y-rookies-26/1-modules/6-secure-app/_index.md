---
title: Application Security for Observability
linkTitle: 8. Application Security for Observability
weight: 8
archetype: chapter
time: 60 minutes
authors: ["Diana Omuoyo"]
description: Detect and investigate runtime vulnerabilities before attackers find them first.
draft: true
hidden: true
aliases:
  - /o11y-rookies-26/6-secure-app/
params:
  images:
    - images/secureapp.avif
---

This workshop is for application owners, SREs, and SecOps teams — detect runtime vulnerabilities and exploits inside Splunk Observability Cloud, prioritize by real-world threat context, and integrate findings with existing SOC workflows.

---

Application security data is often scattered across standalone scanners, spreadsheets, and ticket queues that never reflect what is actually running in production. As a result, remediation queues swell with theoretical severity, visibility gaps widen between engineering and security, and MTTR for exploitable issues slows. This typically happens for three reasons:

- **Fragmented visibility**: Vulnerability findings live outside the APM views teams already use for latency, errors, and dependencies. Security and reliability are assessed in separate tools with no shared service context.
- **Theoretical prioritization**: Teams sort by CVSS alone without exploit availability, observed malicious activity, or runtime attack signals tied to deployed libraries and services.
- **Operational and workflow debt**: Manual triage, duplicate SecOps workflows, and ungoverned library sprawl consume remediation capacity while confirmed, actionable items wait in queue.

To address these challenges you need a way to:

- **Maintain visibility**: Unify reliability and security on APM Overview, Service Map, and per-service Application Security workspaces - plus org-wide library inventory and SIEM notification — without bolting on a second agent or product.
- **Update and upgrade with context**: Tie remediation guidance to library names, versions, and affected-service blast radius before engaging engineering.
- **Eliminate technical debt**: Govern vulnerability queues with status lifecycle management and supply-chain hygiene across shared libraries.
- **Prioritize known threats**: Compare CVSS with exploitation risk scoring and pivot from cataloged CVEs to runtime attack forensics with code-level stack traces.
- **Modernize defenses**: Move from periodic scanning and reactive fire drills to continuous runtime detection integrated with Splunk Enterprise Security, with a credible path toward inline protection.

In this workshop, we'll explore:

- How to navigate Application Security entry points.
- How to inventory runtime vulnerabilities and correlate security posture with service health.
- How to prioritize findings using threat-informed risk scoring.
- How to guide remediation, manage vulnerability status, and review library hygiene.
- How to investigate runtime attacks and integrate notifications with SecOps.
- How to articulate the end-to-end Observability plus security value story.

---
