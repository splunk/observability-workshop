---
title: "Phase 1: Docker -- Before OBI"
linkTitle: 3. Docker Before OBI
weight: 3
archetype: chapter
time: 15 minutes
description: Deploy three microservices with Docker Compose and confirm that APM is empty -- no traces exist because there is no instrumentation.
---

In this phase you'll deploy a polyglot microservices stack and establish the "before" state: infrastructure metrics flow to Splunk, but APM has zero traces because the applications have absolutely no instrumentation.

```text
Frontend (Node.js :3000)  →  Order-Processor (Go :8080)  →  Payment-Service (Go :8081)
```
