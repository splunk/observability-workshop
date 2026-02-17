---
title: Advanced Detectors
linkTitle: 4.2 Multi-Condition Detectors
weight: 3
---

## Lab Objective

Build a multi-condition detector that alerts only when:

- A metric is historically anomalous  
- AND above a static operational threshold  
- For a sustained duration  
- With a customized, actionable alert message  

---

## Scenario

Alert when:

- CPU utilization is anomalous  
- AND above 90%  
- For 15 minutes sustained  

This pattern reduces noise by combining statistical deviation with an operational guardrail.

---