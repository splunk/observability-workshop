---
title: Review of the workshop
linkTitle: 1. Key Items
weight: 1
---

During our workshop we have seen how the Splunk Infrastructure Suite in combination with the OpenTelemetry signals **Metric's**, **Traces** and **Log's** can help you to discover problems and resolve them faster.

* We have a better understanding of the Main User interface and its components, the *Landing, Infrastructure, APM, RUM, Synthetics, Dashboards* pages, and a quick peek at the *Settings* page.
* Depending on time, we did an *Infrastructure* exercise and looked at *Metrics* used in the  Kubernetes Navigators and saw related services found on our Kubernetes cluster:

![kubernetes](../images/infra.png)

* Understood what users were experiencing and used RUM & APM to Troubleshoot a particularly long page load, by following its trace across the front and back end and right to the log entries.
We used tools like RUM *Session replay* and the APM *Dependency map* with Breakdown to discover what is causing our issue:

![rum and apm](../images/rum-apm.png)

* Used *Tag Spotlight*, in both RUM and APM, to understand blast radius, detect trends and context for our performance issues and errors. We drilled down in *Span's* in the APM *Trace waterfall* to  see how services interacted and find errors:

![tag and waterfall](../images/tag-spotligth-waterfall.png)

* We used the *Related content* feature to follow the link between our *Trace*  directly to the *Log's* related to our *Trace* used filters to drill down to the exact cause of our issue.

![logs](../images/log.png)

* We then looked at Synthetics, which can simulate web and mobile traffic and we used the available  Synthetic Test, first to confirm our finding from RUM/AMm and Log observer, then we created a *Detector*  so we would be  alerted if when the run time of a test exceeded our SLA.

* As the last exercise we create a health dashboard with the intention to keep that running for our Developers  and SRE on a TV screen:

![synth and TV](../images/synth-tv.png)

