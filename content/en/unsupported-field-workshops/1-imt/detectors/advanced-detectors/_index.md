---
title: Multi-Condition Detector
linkTitle: 4.2 Advanced Detectors
weight: 3
authors: ["Charity Anderson"]
---

## Overall Objective

Build a **multi-condition detector** that alerts only when:

- A metric is **historically anomalous**  
- AND above a **static operational threshold**  
- For a **sustained duration**  
- With a **customized, actionable alert message**  

The intent of this lab is to use a real-world example to gain hands-on experience with the **SignalFlow behind detectors and alerts**. You will move beyond the wizard interface to understand how **metric streams** are evaluated, how **threshold functions** generate anomaly conditions, and how **detection logic** is composed programmatically.

You will examine the out-of-the-box functions used by the wizard, understand how they translate to **SignalFlow**, and introduce additional SignalFlow methods and functions to construct a detector with greater precision and control.

---

## Scenario

Alert when:

- CPU utilization is **anomalous based on history**  
- AND above **90%**  
- For **15 minutes sustained**  

This pattern reduces noise by combining statistical deviation with an operational guardrail and reinforces how **threshold generation** and **alert logic** work together within SignalFlow.