---
title: Enable Digital Experience Analytics with Splunk RUM
linkTitle: DXA with RUM
weight: 20
archetype: chapter
time: 60 minutes
authors: ["Splunk"]
description: Configure Splunk RUM for Digital Experience Analytics, create DXA event definitions, and connect user behavior analysis back to RUM troubleshooting workflows.
draft: false
hidden: false
---

Digital Experience Analytics (DXA) uses Splunk Real User Monitoring (RUM) data to analyze user journeys, conversion friction, adoption, and frustration signals. In this workshop you will configure a browser application for RUM, make the RUM data usable by DXA, create DXA event definitions, and connect behavior analysis back to RUM sessions for troubleshooting.

The runnable lab uses nginx to inject the RUM snippet because it is easy to run locally and mirrors a common rollout pattern for legacy or static sites. If you own the frontend build pipeline, the same RUM configuration belongs in the application bundle so versioning, review, and release ownership stay with the app team.

## Workshop goals

- Configure Splunk RUM browser agent version 2.0 or later for DXA.
- Explicitly enable anonymous user tracking so DXA can correlate events by user and session.
- Generate page load, click, route, error, and checkout activity in a local browser app.
- Create a DXA project, event definitions, user segments, funnel analysis, and time series analysis.
- Use RUM sessions, Session Replay, and APM links to investigate the behavior surfaced by DXA.

## Lab files

The runnable sample for this workshop is in:

```text
workshop/rum-nginx-session-replay/
```

The workshop content uses the sample files as reference implementations. You can run them locally with Docker, then adapt the same RUM configuration to a reverse proxy, ingress controller, static-site nginx deployment, or app-native JavaScript bundle.

## References

- [Set up Digital Experience Analytics in Splunk RUM](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/set-up-digital-experience-analytics)
- [Projects in Digital Experience Analytics](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/set-up-digital-experience-analytics/projects-in-digital-experience-analytics)
- [Create and manage event definitions](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/digital-experience-analytics/create-and-manage-event-definitions)
- [Install the Splunk RUM browser agent](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-browser-applications-for-splunk-rum/install-the-splunk-rum-browser-agent)
- [Configure the Splunk RUM browser agent](https://help.splunk.com/en/splunk-observability-cloud/manage-data/instrument-front-end-applications/instrument-mobile-and-web-applications-for-splunk-real-user-monitoring-rum/instrument-browser-applications-for-splunk-rum/configure-the-splunk-rum-browser-agent)
- [Introduction to Splunk RUM](https://help.splunk.com/en/splunk-observability-cloud/digital-experience-monitoring/real-user-monitoring/introduction-to-splunk-rum)
