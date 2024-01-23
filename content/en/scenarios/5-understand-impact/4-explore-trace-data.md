---
title: Explore Trace Data
linkTitle: 5.4 Explore Trace Data
weight: 4
---

Now that we've captured several tags from our application, lets explore some of the trace data we've captured that include this additional context, and see if we can identify what's causing poor user experience in some cases. 

## Use Trace Analyzer

Navigate to **APM**, then select **Traces**.  This takes us to the **Trace Analyzer**, where we can add filters to search for traces of interest. For example, we can filter on traces where the credit score starts with "7": 

![Credit Check Starts with Seven](../images/credit_score_starts_with_seven.png)

If you load one of these traces, you'll see that the credit score indeed starts with seven. 

We can apply similar filters for the customer number, credit score category, and credit score result. 

## Explore Traces With Errors

Let's remove the credit score filter and toggle "Errors only" to on, which results in a list of only those traces where an error occurred: 

![Traces with Errors Only](../images/traces_errors_only.png)

Click on a few of these traces, and look at the tags we captured. Do you notice any patterns? 

If you found a pattern - great job!  But keep in mind that this is a difficult way to troubleshoot, as it requires you to look through many traces and remember what you saw in each one to see if you can identify a pattern. 

Thankfully, Splunk Observability cloud provides a more efficient way to do this, which we'll explore next.  