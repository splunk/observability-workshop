---
title: Key Takeaways
linkTitle: 1. Key Takeaways
weight: 1
---

During the workshop, we have seen how the Splunk Observability Cloud in combination with the OpenTelemetry signals (**metrics**, **traces** and **logs**) can help you to reduce mean time to detect (**MTTD**) and also reduce mean time to resolution (**MTTR**).

* We have a better understanding of the Main User interface and its components, the *Landing, Infrastructure, APM, Log Observer, Dashboard* pages, and a quick peek at the *Settings* page.
* Depending on time, we did an *Infrastructure* exercise and looked at *Metrics* used in the  Kubernetes Navigators and saw related services found on our Kubernetes cluster:

![Kubernetes](../images/infra-k8s.png)

* Understood what users were experiencing and used APM to Troubleshoot a particularly long load time and error, by following its trace across the front and back end and right to the log entries.
We used tools like the APM *Dependency map* with Breakdown to discover what is causing our issue:

![apm](../images/apm.png)

* Used *Tag Spotlight*, in APM, to understand blast radius, detect trends and context for our performance issues and errors. We drilled down in *Span's* in the APM *Trace waterfall* to  see how services interacted and find errors:

![tag and waterfall](../images/tag-spotlight-waterfall.png)

* We used the *Related content* feature to follow the link between our *Trace* directly to the *Logs* related to our *Trace* and used filters to drill down to the exact cause of our issue.

![logs](../images/log.png)

* In the final exercise, we created a health dashboard to keep that running for our Developers and SREs on a TV screen:

![synth and TV](../images/synth-tv.png)
