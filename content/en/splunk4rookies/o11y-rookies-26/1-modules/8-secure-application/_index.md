---
title: Application Security
linkTitle: 8. Application Security
weight: 8
archetype: chapter
time: 60 minutes
authors: ["Diana Omuoyo"]
description: Detect and investigate runtime vulnerabilities before attackers find them first.
draft: true
hidden: true
aliases:
  - /o11y-rookies-26/6-secure-application/
params:
  images:
    - images/secureapp.avif
---

This workshop introduces you to the benefits of embedding application security inside Observability workflows. By the end of these modules, you will understand how engineering and security teams can share one runtime view of risk, prioritize beyond CVSS alone, and feed findings into existing SOC tools.

It is suitable for application owners, SREs and SecOps teams. 

---

## Overview 

Application security data is often scattered across standalone scanners, spreadsheets, and ticket queues that never reflect what is actually running in production. As a result, remediation queues widen gaps between engineering and security, and MTTR for exploitable issues slows. This typically happens for three reasons:

- **Fragmented visibility**: Security and reliability are assessed in separate tools with no shared service context.
- **Theoretical prioritization**: Teams assess risk by CVSS alone without observed malicious activity, or runtime attack signals tied to deployed libraries and services.
- **Operational and workflow debt**: Manual triage, duplicate SecOps workflows, and ungoverned library sprawl consume remediation capacity.

To address these challenges you need a way to:

- **Maintain visibility**: Unify reliability and security in existing & shared workspaces without bolting on a second agent or product.
- **Update and upgrade with context**: Tie remediation guidance to vulnerability risk profile, library names, versions, and affected-service blast radius before engaging engineering.
- **Eliminate technical debt**: Govern vulnerability queues with status lifecycle management and hygiene across shared context.
- **Prioritize known threats**: Compare CVSS scores with exploitation risk and pivot from cataloged CVEs to runtime attack forensics with code-level stack traces.
- **Modernize defenses**: Move from periodic scanning and reactive fire drills to continuous runtime detection integrated with Splunk Security.

---
