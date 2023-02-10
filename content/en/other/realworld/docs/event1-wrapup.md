---
title: Event 1 - Wrapup
weight: 11
---

## Review Questions

### Questions to consider
* Do we have all of the information we need to troubleshoot the issue?
  * Yes, we were able to find in Kubernetes Navigator that we ran low on disk.
* Is this information be alertable? Is alerting on this data the best way to deal with the problem?
  * Yes, we can create a "Resources Running Out" alert on disk, for example.
* The users contacted us. How else could we find out about application slowness before a user calls us?
  * One way is to use Synthetics, which can test the application and identify latency.
  * Another way is to use Real User Monitoring, to identify slowness that our users experience.
* How much time did it take before we found out about this issue? What could be the cost of those delays?
  * Not every user that is impacted will report the issue. So often there is a long delay between when an issue is reported and that information gets to a person that can solve the issue.
  * In short: TOO long.

[Go to Event 2](../event2)