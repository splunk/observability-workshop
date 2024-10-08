---
title: View test results
linkTitle: 7. View test results
weight: 7
---


1\. Click into a spike or failure in your test run results.

![image](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-01/7da71cab-5d3f-4557-af22-413e51706016/ascreenshot.jpeg?tl_px=0,372&br_px=1719,1333&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=251,277)

2\. What can you learn about this test run? If it failed, use the error message, filmstrip, video replay, and waterfall to understand what happened.

![Single test run result](../../images/browser-run-result.png)

3\. What do you see in the resources? Make sure to click through all of the page (or transaction) tabs.

![image](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-02-01/f971fc4b-49bd-4134-ae27-fe9444e41ef0/ascreenshot.jpeg?tl_px=738,453&br_px=2458,1414&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,276)

{{% notice title="Workshop Question" style="tip" icon="question" %}}
Do you see anything interesting? Common issues to find and fix include: unexpected response codes, duplicate requests, forgotten third parties, large or slow files, and long gaps between requests.
{{% /notice %}}

Want to learn more about specific performance improvements? [Google](https://web.dev/learn/performance/welcome) and [Mozilla](https://developer.mozilla.org/en-US/docs/Web/Performance/How_browsers_work) have great resources to help understand what goes into frontend performance as well as in-depth details of how to optimize it.