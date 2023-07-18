---
title: Optimization
linkTitle: Web Optimization
description: How do we improve performance?
weight: 7
---

Now that we've seen both real user and synthetic performance information -- how do we actually make improvements?

Go to [Splunk Web Optimization](https://optimization.rigor.com/s/3609729?tid=ov&sh=8E2A6957B4A505DE466C1EE8130A3D2D). This is an optimization scan on our own splunk.com website.

Here we see performance data as well as some web best practices to improve. Follow along as we take a tour.

Click the "i" icon on the top right to see how the test was configured. Similar to our Synthetic Browser Tests, right?

Take a look at these items in particular:
1. What Core Web Vital is scoring the worst? (Largest Contentful Paint, Total Blocking Time, or Cumulative Layout Shift)
1. What type of content is being used the most, and how does that compare to the internet average?
1. What are the top two Performance Defects, and how easy or difficult are they to address?
1. Under "Top Performance Defects" click "View All" to go to the best practices. Do you see any themes?
1. In the list of defects, sort by highest number of related Links. Why could this view be useful?
1. What is the largest piece of content being served, and how could it be improved? (hint: go to the third party content tab)

There's a lot here, but what's important is that we now have a starting point to improving performance.