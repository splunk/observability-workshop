---
title: View test results
linkTitle: 7. View test results
weight: 7
---


1\. Click into a spike or failure in your test run results.

![Spike in the browser test performance KPIs chart](../_img/browser-spike.png)

2\. What can you learn about this test run? If it failed, use the error message, filmstrip, video replay, and waterfall to understand what happened.

![Single test run result, with an error message and screenshots](../_img/browser-fail-result.png)

3\. What do you see in the resources? Make sure to click through all of the page (or transaction) tabs.

![resources in the browser test waterfall, with a long request highlighted](../_img/browser-resources.png)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Do you see anything interesting? Common issues to find and fix include: unexpected response codes, duplicate requests, forgotten third parties, large or slow files, and long gaps between requests.
{{% /notice %}}

Want to learn more about specific performance improvements? [Google](https://web.dev/learn/performance/welcome) and [Mozilla](https://developer.mozilla.org/en-US/docs/Web/Performance/How_browsers_work) have great resources to help understand what goes into frontend performance as well as in-depth details of how to optimize it.