---
title: 1. Introduction to Logs
weight: 1
---

You’ve now navigated directly from an **APM** trace into **Logs** using the **Related Content** link. **Logs** is Splunk Observability Cloud’s no-code interface for exploring and analyzing log data.

The key advantage, just as with the **RUM** and **APM** integration, is that you’re viewing your logs in the context of your previous actions. In this case, that context includes the matching time range **(1)** from the trace and a filter **(2)** automatically applied to the `trace_id`.

![Trace Logs](../images/log-observer-trace-logs.png)

The results contain the available log records correlated with that trace. These records may come from several services that participated in the checkout request. The exact number of records depends on which services emit logs, whether those logs are ingested, and whether they contain the required trace metadata.

Even for a small application such as the **Astronomy Shop**, a single transaction can generate many log records. On the next page, you’ll filter these results to find the entries that explain the payment failure.

Before continuing, let’s recap how the three pillars of observability have guided the investigation:

|  Metrics                   | Traces                      |  Logs                      |
| :-------:                  | :------:                    | :----:                     |
| _**Do I have a problem?**_ | _**Where is the problem?**_ | _**What is the problem?**_ |

* **Metrics** revealed the symptom. In **RUM**, the *PlaceOrder* duration showed that customers were experiencing slow checkout interactions.

* **Traces** narrowed the investigation. Following a failing request into **APM** led us to the **payment** service. Comparing its versions showed that the errors were associated with *v350.10*, while *v350.9* completed requests successfully.

* The **waterfall** exposed the failure. The affected request encountered **HTTP 401** errors and repeated *payment* attempts, contributing to the checkout delay. The span reported *“Invalid request,”* but that message alone did not explain why the request was rejected.

* **Logs** provide the next piece of evidence. Using **Related Content**, we opened the log records associated with the same trace. Now we’ll filter those records to uncover the details behind the payment failure.
