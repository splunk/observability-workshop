---
title: 1. Troubleshooting with Splunk Observability Cloud
weight: 1
---

One of the core tenets in building the Splunk Observability Cloud is unifying telemetry data to build a complete picture of a user’s experience and your application stack.

In this demo we’ll be showing how Splunk Observability Cloud provides instant visibility of the user experience -- from the perspective of the front end application to its backing services -- using Real User Monitoring (or RUM), Application Performance Monitoring (or APM), and Log Observer.

This is my application. It’s an online boutique that has been instrumented for Splunk RUM. I will do what I would typically do in this application -- browse through a few items, add them to my cart, and then checkout.
This checkout process seems to be taking a while to complete, but it did ultimately complete. Let’s go take a look at what this looks like in RUM.

Modern web experiences can appear simple, but are complex, asynchronous systems. Single page applications must accommodate myriad browser and machine types, and interact with many backend services. Splunk RUM captures, in full-fidelity, all of the data generated in every user session and presents it to you in a rich and actionable way.

From this page I can see a variety of metrics, such as: highest page load times, number of frontend and backend errors, top pages by views, top endpoints, and Google’s web vitals metrics. It’s all here on the dashboard.
(Note: You can learn more about Web Vitals metrics here: [https://web.dev/vitals/](https://web.dev/vitals)

I can also filter down my RUM view to isolate issues for specific operations, browser types, browser versions, or users from specific geographic regions, among others.

In the top-left corner I can see that my highest page load times are higher than  they have been in the previous hour, and way too high if I want to keep happy customers. Let’s dig into this a little more to see what’s happening here.

By clicking into the checkout process in the Highest P75 Page Load times you can see I am taken to the tag spotlight view, filtered down to the /cart/checkout process showing me all the tags associated with every user session such as browser, version, city, state and much more. I can also change this tag spotlight view to break this data down by any of the metrics available.

In this graph at the top of the page I can see that there are some alarming page load times.

Now, if I look at these spikes I can see the P99 is even more alarming, so let’s filter this down and dig into the actual user session that took this alarming amount of time.

Here I can see one of the clicks this user made during this session. And I can see that there is 1 process that is taking up almost 99% of the duration of the whole transaction.

By expanding this I can see all the metadata associated with this span and all of the tags associated with it.

This is where the end to end value of the Splunk Observability Cloud starts to show. We can hover over this APM link to reveal some quick, at a glance, info about what’s happening on the backend.

This performance summary is clearly showing two actionable things:
Time is being spent in the app (not db, network, or external); and
There are errors occurring in these back-end services, and I can see precisely which service is producing the “root cause” for this particular trace (in this case the payment service in dark red).

To dig further, I can explore two different paths, depending on the questions I want to ask.

Let’s explore both to understand why I might want to do one or the other.

First let’s look at the workflow. Here I am getting a summarized view of all of the back-end traces, but specifically for the checkout process. I can see my whole application’s service map, with interservice latency and errors displayed, starting at the frontend and going through all of my microservices on the backend. The workflow is filtering out the noise, by having me only focus on service interactions involved in this process.

[Click on the payment service.]

Because Splunk is designed with AI-directed triage at its center, I can plainly see an alarming error rate within my payment service, the same service that caused an issue for my specific user session in RUM. The solid red status indicates the errors originate here. Let me say that again: this is not just indicating errors, but that this is the root cause of the errors in the workflow. This is powerful for distributed microservices applications, where different teams own different services. The team engaged here needs to be the payment service team who develop and support that service.

I can navigate to a similar tag spotlight view like we saw with the front-end to get a better picture of what’s in common with these error traces.

[Click on Tag Spotlight]

In this view I can see tags associated with errors for the checkout process for the payment service. I can also toggle this view to look at latency instead. I see out of the box tags like http status codes and infrastructure metadata, and custom tags I can add to my application, like tenant level and version number.

Now, looking at these tags I can see all of the errors were 401’s, and all of my tenants are being impacted by these errors. I also notice that 100% of the requests that hit this new version v350.10 failed, but all requests that hit the previous version succeeded. Being able to see the blast radius and context is immensely powerful. Being able to isolate issues on specific parts of my infrastructure is powerful as well. I can also jump to infrastructure views in kubernetes, or logs for my payment service, if this was relevant to this analysis.

[Click on the second tab that opened (trace id).]

The other method I can troubleshoot is by following the very trace I was looking at from the front-end. I can only do this with Splunk’s powerful collection of every single trace (no sampling), which guarantees I don’t hit any dead ends. Here I can see the specific errors occurring on the payment service, with several attempts failing.

Many problems are solved with features like tag spotlight, which help identify what is in common with issues. Other times I need to track down a very unique situation. In these cases it helps having every single trace.
[Click on one of the error spans.]

By looking at one of the spans I can see that this error is due to an invalid request error on version 350.10. I can also see the different tags that came from the instrumentation, as well as the custom tags I added to my code.

[Click on the … next to k8s.pod.name]

I can also follow links to investigate my infrastructure, such as my pod here.

On the bottom of the screen you can see related content for this trace. I can follow that breadcrumb to get more information about these errors.

[Click on “ERROR” in the legend and “Add to Filter”.]

I’m now looking at the log messages correlated to that trace. I can filter down to the errors to get additional details I might only find in the logs.
[Click on one of the errors.]

I can see I am getting an invalid API token error, and it reaffirms the error associated with version v350.10.

[Close the popup. Click on “k8s.namespace.name” and click on the “=” next to your “username-shop”.]

[In the filter bar, click an x next to your trace id.]

[In the aggregation bar, click “Clear all”, select “Version”, and click “Apply”]

By adjusting my filters, I can now see how many errors I am getting for this application, and which versions are impacted. I can clearly see the problem is unique to this new version.

I could even widen my time window to look beyond this troubleshooting time window.
[Drop down the “three dots” menu”]

If I want I can save this query, to easily use it next time.
[Drop down the time window and select “Live Tail”]

Let’s say I want to ensure this error has been resolved and I want to make sure it isn’t coming back. I can use Live Tail to monitor the incoming logs, as they happen.
I’m still seeing errors coming in, so it looks like the developer’s haven’t resolved the issue just yet.
Now our troubleshooting exercise has been completed. But while we’re here in Log Observer I wanted to show you one more thing you can accomplish that is more proactive.

[Change the time period to “Last 15 minutes”]

[In the filter bar, click the x next to “ERROR”.]
 If the customer is an existing Splunk Customer, they may ask if these are the logs from Splunk Enterprise (platform/core) or Cloud. Or if you want to show them that option, jump to Log Observer Connect.

[Drop down the group by, click “Clear All”, select “ad_context_words_all”, and click “Apply”]

Frequently we will find interesting events within the logs that would be useful to measure as metrics, for charting and analysis. Here, we can do just that - metricize logs, which can help with tracking events, alerting on situations, or identifying anomalies.

In this case we will pick the example of metricizing product keywords.
[Click the “three dots’ menu and click “Save as Metric”]

Being an e-commerce app, we can begin the process of metricizing these ad words.
In the first step, your recent logs, in this case last 15 minutes, are evaluated. We have 6 different keywords, which means 6 metric time series will be created. We can change the time window to see if additional time series would be created.
[Click Next.]

Next we select the token used for creating this data. Here we can see that we only have 6 MTS’s for the entire week.
[Click Next.]

Finally we can review and approve.

[IMPORTANT NOTE: Don’t actually save this, it will just clutter things. We will go to one already saved.]
[Click the bookmarks button, and select the “Adwords” dashboard under “Favorites.]

NOTE: If you don’t find the dashboard there you can find it under “Dashboards”; the demo prework shows how to set this up.

We’ve already set up this metric, so let’s take a look at the results.
In this chart we can see a summary of orders for each of the different adwords. We could use this to see which are more successful than others, or to alert if we see any anomalous results.
Demo Conclusion
That wraps up the demo of Splunk Observability Cloud. We were able to:
Understand what real users were experiencing
Troubleshoot a particularly long page load, by following it’s trace across the front and back end and right to the log entries
Use tag spotlight, in both RUM and APM, to understand blast radius and context for our performance issues and errors
Use live tail, to ensure our identified problem is truly resolved, real-time
Convert log entries into metrics, giving us flexible ways to present the data and alert on anomalies.
Today we didn’t even talk about the power of the rest of Splunk Observability Cloud, such as:
Infrastructure monitoring, which shows how our infrastructure is behaving -- hosts, kubernetes, and applications
Synthetics, which can simulate web and mobile traffic and report on application behavior and potential areas for improvement
And much more…
[End of Demo]
