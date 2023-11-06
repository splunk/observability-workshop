---
title: Step 1
weight: 1
---

1. We have come from a trace to the logs for paymentservice
2. Note that the time window is set to a specific time range that is relevant to the trace which is included in the filter
3. Group By Severity
4. Notice that the chart changes and you have a legend of debug, error and info
5. Click on error, and add to filter
6. Now only have all error fields
7. Click on an error entry, what is the error?
8. Click on configure table and ensure the following is selected:
  - `k8s.pod_name`
  - `message`
  - `version`
9. Change to last 15m
10. Remove trace id from filter and add service.name=paymentservice
11. Click Save to Dashboard
12. Enter name, description, select dashboard, new dashboard, name = initial+ War Room
13. Ensure new dashboard is highlighted
14. Click OK
15. Select Log Timeline
16. Save
17. Repeat above for log view
18. Click save and goto dashboard

Hover over the boxes at the bottom of the trace

![Related content to the trace includes Logs](../images/rel-logs.png?width=50vw)

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
