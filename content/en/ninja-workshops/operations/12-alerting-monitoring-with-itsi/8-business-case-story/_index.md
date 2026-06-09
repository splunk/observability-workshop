---
title: Business Case Story
linkTitle: 8. Business Case Story
weight: 1
---

# Business case story: the missed delivery window

This workshop story uses a specialty pharmacy instead of the usual online checkout scenario. The business is not trying to sell one more item. It is trying to keep a patient delivery promise.

## The company

**Meridian Specialty Pharmacy** delivers refrigerated medication to patients at home. Many deliveries are tied to a treatment schedule, so the business promise is simple:

> "Every confirmed delivery must arrive inside the patient delivery window."

If the delivery window is missed, the impact is larger than a late package:

* The patient may miss a treatment appointment.
* The pharmacy may need to replace expensive refrigerated medication.
* The support team receives urgent calls from patients and clinics.
* Operations leaders lose confidence in the route planning system.

The technology team supports a few critical systems:

| System | What it does | Observable signal |
|---|---|---|
| Patient Portal | Patients confirm delivery windows | RUM page load time, browser errors |
| Route Planner API | Builds route assignments for couriers | APM latency, error rate, trace waterfalls |
| Courier Mobile API | Couriers accept routes and update status | APM request rate, failed check-ins |
| Notification Gateway | Sends SMS and email updates | Synthetic availability, provider errors |
| Dispatch Queue | Holds route assignments waiting for confirmation | Queue depth, oldest pending route age |

## The incident

At 8:10 AM, dispatchers notice that the morning route board is behind. Drivers are waiting for confirmed routes, but the patient portal still looks mostly available. No single alert explains the issue.

By 8:25 AM:

* Patient confirmation pages are loading slower than normal.
* The route planner API is retrying calls to a geocoding dependency.
* The dispatch queue is growing.
* The notification gateway is healthy, so patients are not seeing obvious failures yet.
* Support calls have not spiked yet, but the business is already at risk.

The root problem is not "the site is down." The root problem is that the delivery promise is quietly becoming unsafe.

## Workshop objective

Participants should leave with one core idea:

> Splunk Observability Cloud helps teams find the technical evidence, while ITSI turns that evidence into business service health, grouped incidents, and a shared operating view.

## 75-minute workshop path

| Time | Story beat | Product view | ITSI concept | Small wow factor |
|---|---|---|---|---|
| 10 min | Define the delivery promise | ITSI Service Analyzer | Service | A business service can be monitored like a technical service. |
| 10 min | Show early service degradation | ITSI KPI list | KPI | A service can be yellow before customers start calling. |
| 10 min | Connect user and backend symptoms | Observability Cloud RUM and APM | Supporting signals | Frontend pain and backend latency tell one story. |
| 10 min | Show why the service is degraded | ITSI dependency view | Dependency | A child service can explain parent service health. |
| 10 min | Reduce alert noise | ITSI Episode Review | Episode | Five symptoms become one incident to work. |
| 15 min | Investigate the cause | ITSI deep dive and Observability Cloud drilldown | Deep dive | Operators move from business health to evidence without changing the story. |
| 10 min | Present to operations | ITSI glass table | Glass table | A non-technical stakeholder sees delivery risk, not raw telemetry. |

## Scene 1: Start with the business service

Open ITSI and show a parent service named `Medication Delivery Promise`.

Under it, show four child services:

* `Patient Confirmation`
* `Route Planning`
* `Courier Updates`
* `Patient Notifications`

**Concept introduced:** ITSI service.

**What participants should notice:** The service name is business language. It is not a host, pod, or endpoint.

**Simple product highlight:** In Service Analyzer, the health score lets the instructor say, "This is how the business is doing right now," before discussing any technical details.

## Scene 2: Show a yellow service before the outage

Select `Medication Delivery Promise` and show these KPIs:

| KPI | Normal meaning | Incident behavior |
|---|---|---|
| Delivery confirmation success rate | Patients can confirm delivery windows | Slightly lower than normal |
| Route planner p95 latency | Routes can be generated quickly | Above warning threshold |
| Oldest pending route age | Dispatch queue is moving | Growing steadily |
| Patient portal page load p95 | Patients can use the portal | Slower than normal |

**Concept introduced:** KPI.

**What participants should notice:** The service is not red. It is degraded early enough for operations to act.

**Simple product highlight:** KPI severity changes roll up into service health. This is the first "wow" because the business service changes status from several small signals, not from one big outage.

## Scene 3: Pivot to Observability Cloud for evidence

Open Splunk Observability Cloud and show two views:

* RUM shows the patient confirmation page is slower for mobile users.
* APM shows the route planner API has high latency in the geocoding span.

**Concept introduced:** supporting evidence outside ITSI.

**What participants should notice:** ITSI is the operating model, and Observability Cloud is where the technical investigation gets rich.

**Simple product highlight:** The story moves from business health to trace-level evidence without changing the incident narrative.

## Scene 4: Explain the dependency

Return to ITSI and select `Route Planning`.

Show that `Route Planning` depends on:

* `Geocoding Provider`
* `Dispatch Queue`
* `Notification Gateway`

In the story, `Notification Gateway` is green, but `Geocoding Provider` and `Dispatch Queue` are yellow or red.

**Concept introduced:** service dependency.

**What participants should notice:** A healthy notification provider does not mean the delivery promise is healthy.

**Simple product highlight:** Dependencies make it possible to explain why the parent service is degraded without forcing everyone to inspect every dashboard.

## Scene 5: Turn noisy signals into one episode

Open Episode Review and show one episode named:

`Medication Delivery Promise degraded - route planning latency`

The episode can contain related notables such as:

* Route planner latency warning
* Dispatch queue age critical
* Patient portal page load warning
* Geocoding provider latency warning

**Concept introduced:** notable event aggregation and episode.

**What participants should notice:** The team works one incident instead of chasing several disconnected alerts.

**Simple product highlight:** Episode grouping makes ITSI feel different from a normal alert list. It turns symptoms into a manageable operational object.

## Scene 6: Use a deep dive to compare signals

From the service or KPI, open a deep dive with lanes for:

* Route planner p95 latency
* Oldest pending route age
* Patient portal page load p95
* Delivery confirmation success rate

**Concept introduced:** deep dive.

**What participants should notice:** The queue age rises after route planner latency rises. That makes the incident explainable.

**Simple product highlight:** A deep dive lets the instructor show time alignment without building a custom dashboard during the workshop.

## Scene 7: Close with a glass table for operations

Open a simple glass table named `Morning Delivery Risk`.

Keep it minimal:

| Tile | Value |
|---|---|
| Medication Delivery Promise | Health score |
| At-risk routes | Current count |
| Oldest pending route | Age in minutes |
| Patient Confirmation | Health score |
| Route Planning | Health score |
| Courier Updates | Health score |

**Concept introduced:** glass table.

**What participants should notice:** This view is for dispatch leaders, not observability engineers.

**Simple product highlight:** ITSI can show service health in the language of an operating team. The same data that helps engineers troubleshoot can help managers decide whether to add staff, warn clinics, or delay dispatch.

## Instructor script

Use this short narrative as the through-line:

1. "Meridian's promise is not uptime. Their promise is that confirmed medication deliveries arrive inside the patient window."
2. "At 8:10 AM, nothing is fully down, but the promise is becoming risky."
3. "ITSI shows the business service turning yellow because several KPIs are weakening together."
4. "Observability Cloud shows the technical evidence: route planner latency and slow patient confirmation pages."
5. "The dependency view explains why the delivery promise is affected even though notifications are still healthy."
6. "Episode Review groups related alerts so the team works one incident."
7. "The glass table gives operations a view they can act on without reading traces."

## Simple build plan

For a hands-on lab, do not build every system. Simulate or pre-load enough data to teach the concepts.

| Workshop object | Suggested simple implementation |
|---|---|
| Parent service | `Medication Delivery Promise` |
| Child services | `Patient Confirmation`, `Route Planning`, `Courier Updates`, `Patient Notifications` |
| Core KPIs | Route planner p95 latency, oldest pending route age, patient portal page load p95, delivery confirmation success rate |
| Detector examples | High route planner latency, high pending route age |
| Episode rule | Group by service name and environment |
| Glass table | Six tiles: parent health, child health, at-risk routes, oldest pending route |

## Optional advanced moments

Use these only if the audience is ready:

* **Adaptive thresholds:** Explain that route volume is different at 8 AM than at 8 PM, so static thresholds can be noisy.
* **Maintenance windows:** Show how planned route-planner maintenance should not create false operational incidents.
* **Entity-level KPIs:** Show one region or courier hub degrading while the national service is still mostly healthy.
* **Drift detection:** Explain how a queue age KPI that slowly worsens over weeks can become normal-looking unless ITSI watches for behavior changes.

## Why this story works

This story is simple, but it is not generic:

* It has a believable business promise.
* The incident starts before a full outage.
* The signals come from different places: frontend, backend, queue, dependency, and business KPI.
* ITSI concepts are introduced in the order an operator would use them.
* The final view is useful to a non-technical stakeholder.

## Author references

* [Splunk Observability Cloud service description](https://help.splunk.com/en?resourceId=get-started_service-description)
* [Introduction to Splunk RUM](https://help.splunk.com/en?resourceId=rum_intro-to-rum)
* [Introduction to Splunk APM](https://help.splunk.com/splunk-observability-cloud/monitor-application-performance/introduction-to-splunk-apm)
* [Monitor your services with the ITSI Service Analyzer](https://help.splunk.com/en/splunk-it-service-intelligence/splunk-it-service-intelligence/visualize-and-assess-service-health/4.19/service-analyzer/monitor-your-services-with-the-itsi-service-analyzer)
* [Configure KPI thresholds in ITSI](https://help.splunk.com/en/splunk-it-service-intelligence/splunk-it-service-intelligence/visualize-and-assess-service-health/4.21/create-kpis/configure-kpi-thresholds-in-itsi)
* [Overview of Service Insights in ITSI](https://help.splunk.com/splunk-it-service-intelligence/splunk-it-service-intelligence/visualize-and-assess-service-health/4.19/overview/overview-of-service-insights-in-itsi)

