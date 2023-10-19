---
title: Splunk RUM
weight: 40
---

Splunk Real User Monitoring (RUM) allows your teams to quickly identify and eliminate customer-facing issues across your entire architecture.

Splunk RUM collects performance metrics, web vitals, errors, and other forms of data for every user session to enable you to detect and troubleshoot problems in your application.

In Splunk Observability Cloud click on the **RUM** tab in the left navigation bar.

![RUM App dashboard](../images/rum_dashboard.png)

As we know, modern web experiences can appear simple, but are complex, asynchronous systems. Single page applications must accommodate myriad browser and machine types, and apps must interact with many backend services. Only Splunk RUM captures, in full-fidelity, all of the data generated in every user session and presents it to you in a rich and actionable way.

From this page we can see a variety of metrics, such as: highest page load times, number of frontend and backend errors, top pages by views, top endpoints, and Google’s web vitals metrics. We also get out of the box views for front end health, back end health, and custom events so it's quick to see trends, anomalies, and even create detectors from these views.

{{% notice style="note" %}}
You can learn more about Web Vitals metrics here: [https://web.dev/vitals](https://web.dev/vitals)
{{% /notice %}}

Click the filter bar across the top, show different filtering options
![Filter options for the dashboard](../images/filters.png)

I can also filter down my RUM view to isolate issues for specific operations, browser types, browser versions, or users from specific geographic regions, among others.

In the top-left corner I can see that my highest page load times are higher than  they have been in the previous hour, and way too too high if I want to keep happy customers. Let’s dig into this a little more to see what’s happening here.

![Page load preview with URLs and load times](../images/load.png)

Show and hide filters as you mention them

![Tag Spotlight filters](../images/spotlight.png)

By clicking into the checkout process in the Highest P75 Page Load times you can see I am taken to the tag spotlight view, filtered down to the /cart/checkout process showing me all the tags associated with every user session such as browser, version, city, state and much more. I can also change this tag spotlight view to break this data down by any of the metrics available.

In this graph at the top of the page I can see that there are some alarming page load times.

Click and drag to filter the view down to one of the spikes on the graph, then click the sessions tab

![Highlighting a spike on the line graph](../images/spike.jpg)

Now, if I look at these spikes I can see the P99 is even more alarming, so let’s filter this down and dig into the actual user session that took this alarming amount of time.

Click on the session that appears after filtering with the long duration, if more than one click the one with the highest duration. Click on the /cart/checkout process in the waterfall view to collapse the expanded view so you no longer see the tags."

![List of user sessions associated with this app and time period](../images/sessions.png)
![Waterfall of requests for a specific user session](../images/waterfall.png)

Here I can see one of the clicks this user made during this session. And I can see that there is 1 process that is taking up almost 99% of the duration of the whole transaction.

Click on the long green checkout span that has a blue APM link

![Long checkout span includes link to APM](../images/span.png)

By expanding this I can see all the metadata associated with this span and all of the tags associated with it.
