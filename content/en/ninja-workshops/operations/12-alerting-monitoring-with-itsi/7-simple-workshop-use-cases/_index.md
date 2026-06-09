---
title: Simple Workshop Use Cases
linkTitle: 7. Simple Workshop Use Cases
weight: 1
---

# Simple use cases for a Splunk Observability Cloud and ITSI workshop

Use these scenarios as short, instructor-friendly building blocks. Each one should take 10-20 minutes and can be run as a standalone demonstration or combined into a 60-90 minute workshop.

For a cohesive workshop story that avoids the standard ecommerce checkout scenario, use the [business case story](../8-business-case-story/) as the primary narrative and pull individual ideas from this page only as needed.

The goal is to help participants connect three ideas:

* Splunk Observability Cloud shows what is happening across applications, infrastructure, traces, logs, RUM, synthetics, and detectors.
* ITSI turns technical signals into services, KPIs, dependencies, health scores, and episodes.
* The best workshop story starts with a user or business impact, then follows the signal back to the technical cause.

## Suggested 90-minute flow

| Time | Activity | Products |
|---|---|---|
| 10 min | Map the sample service and business goal | ITSI |
| 15 min | Find a slow or failing service in APM | Observability Cloud |
| 15 min | Turn the signal into a detector or alert | Observability Cloud |
| 20 min | Create a service KPI and dependency | ITSI |
| 15 min | Group related events into an episode | ITSI |
| 15 min | Review the incident from operator and business-owner views | Observability Cloud, ITSI |

## Use case 1: Checkout latency becomes a service health problem

**Story:** Customers can browse products, but checkout is slow.

**Observability Cloud activity:** Open APM, find the checkout or payment service, compare latency and error rate, and identify the slow dependency.

**ITSI activity:** Create a `Checkout Experience` service with KPIs for latency, error rate, and request volume. Add the payment service as a dependency and show how one degraded component affects the business service health score.

**Instructor angle:** This is the clearest first use case because it connects traces and service health without requiring a complex topology.

## Use case 2: CPU saturation creates noisy alerts

**Story:** A Kubernetes node or host is running hot and several downstream services start alerting.

**Observability Cloud activity:** Use Infrastructure Monitoring to find the saturated host, container, or Kubernetes node. Create or review a detector for CPU utilization.

**ITSI activity:** Send or model the detector signal as a notable event. Build an aggregation policy that groups related CPU and service alerts into one episode.

**Instructor angle:** Focus on noise reduction. Participants should see that ITSI is not just another alert destination; it groups related symptoms into an incident workflow.

## Use case 3: Synthetic test detects an outage before users report it

**Story:** The homepage or checkout endpoint fails from one region.

**Observability Cloud activity:** Review a synthetic test failure, compare location results, and confirm whether the issue is regional or global.

**ITSI activity:** Add synthetic availability as a KPI on the customer-facing service. Show how a failed synthetic test changes service health even before application teams report errors.

**Instructor angle:** This works well for executive or service-owner audiences because the signal is easy to understand: can customers reach the service or not?

## Use case 4: Real user monitoring exposes browser-side pain

**Story:** Backend services look healthy, but users are experiencing slow page loads.

**Observability Cloud activity:** Use RUM to review page load time, JavaScript errors, or slow resources for a browser application.

**ITSI activity:** Create a user-experience KPI such as page load p95, frontend error rate, or impacted sessions. Add it to the same service that already has backend KPIs.

**Instructor angle:** Use this to teach that service health should include frontend experience, not only server-side telemetry.

## Use case 5: A bad deployment increases error rate

**Story:** A new version was deployed and errors rose shortly after the release.

**Observability Cloud activity:** Use APM to compare error rate before and after deployment. Filter by service version or environment if those tags exist.

**ITSI activity:** Create a KPI for service error rate and demonstrate threshold changes from normal to high or critical. Add a short episode note that captures the suspected deployment.

**Instructor angle:** This scenario is simple, repeatable, and useful for showing how tags and metadata speed up triage.

## Use case 6: Logs add the missing detail to an incident

**Story:** A service is unhealthy, but metrics only show symptoms.

**Observability Cloud activity:** Pivot from APM or infrastructure context into related logs and find repeated errors, timeout messages, or failed downstream calls.

**ITSI activity:** Add a deep-dive lane or supporting search that lets responders see the relevant log trend from the ITSI investigation path.

**Instructor angle:** Keep this lightweight. The point is correlation and investigation flow, not advanced SPL.

## Use case 7: Business transaction health by service tier

**Story:** A business owner wants to know whether ordering, payment, and fulfillment are healthy.

**Observability Cloud activity:** Identify the technical services that support each step of the transaction.

**ITSI activity:** Build three services: `Ordering`, `Payment`, and `Fulfillment`. Connect them as dependencies under a parent service such as `Online Store`.

**Instructor angle:** This is the best use case for explaining why ITSI models services and dependencies instead of only showing dashboards.

## Use case 8: One recurring incident, many duplicate alerts

**Story:** Every time a cache service fails, application, infrastructure, and synthetic alerts all fire.

**Observability Cloud activity:** Show the different alerts or detectors that fire from the same underlying problem.

**ITSI activity:** Use Episode Review to group the alerts by service, environment, and incident type. Show how responders work one episode instead of several separate alerts.

**Instructor angle:** This is a strong operational story for alert fatigue, MTTR reduction, and cleaner handoff to incident management.

## Use case 9: Service owner dashboard with a glass table

**Story:** A service owner wants a single view of application health, user experience, and business impact.

**Observability Cloud activity:** Choose two or three signals that matter: latency, error rate, availability, or user sessions.

**ITSI activity:** Create a simple glass table that shows the parent service, key dependent services, and a few KPI tiles.

**Instructor angle:** Keep the glass table small. The outcome is not a beautiful dashboard; it is a shared service health view.

## Use case 10: Workshop capstone incident

**Story:** Checkout is degraded because payment latency is high, CPU is elevated, and users are abandoning sessions.

**Observability Cloud activity:** Participants inspect APM, infrastructure, and RUM signals to identify the most likely cause.

**ITSI activity:** Participants review the service health score, open the episode, check impacted KPIs, and explain the business impact.

**Instructor angle:** Use this as the final exercise. Ask participants to present the incident in two minutes: customer impact, affected service, suspected cause, and next action.

## Recommended simple lab data

For a short workshop, use one sample application and keep the taxonomy consistent:

| Field | Example values |
|---|---|
| Application | `online-boutique` |
| Environment | `workshop`, `dev`, `prod` |
| Region | `us-east`, `us-west` |
| Services | `frontend`, `checkoutservice`, `paymentservice`, `cartservice` |
| Business service | `Online Store` |
| KPIs | latency, error rate, request rate, synthetic availability, page load time |

## Facilitator checklist

* Start with a business service name before opening product screens.
* Pick one obvious failure signal and one supporting signal.
* Avoid teaching every navigation path in one use case.
* Use thresholds that visibly change service health during the workshop.
* End each use case with the same operational summary: impact, evidence, suspected cause, next action.
