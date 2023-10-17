---
title: Splunk Log Observer
weight: 30
---

Hover over the boxes at the bottom of the trace

![Related content to the trace incldues Logs](../images/rel-logs.png?width=50vw)

We are federating logs across multiple Splunk instances and indexes, which can be extremely useful when I have logs in multiple places – on-prem or in the cloud.

Let’s navigate to the linked logs.

Click on the logs that are in Splunk Cloud integration

![Link to Logs for this trace](../images/logo.png?width=50vw)

I can now see the log entries coming from this specific trace.

Search for “severity” on the right under the “Fields” section, hover over “error”, and click the = next to “error”

![Logs narrowed down by severity](../images/log-errors.png?width=50vw)

Log Observer gives me an easy way to aggregate and filter on the logs I need to. Here we are just filtering on the log entries that are errors.

Click on one of the errors"

![Error detail](../images/error-detail.png?width=50vw)

I can see there is a bad token in the deployment of the new version. If we filter by this error message, we see the same issue is causing all of the errors.

We’ve now been successful in narrowing down the offending service, version of code, and specific errors that were causing the problem.

If I were still in the middle of my investigation I can see some additional content that can take me back to the map or trace or into the infrastructure where these errors are found. Splunk Observability helps to direct me to the right places to find context.
