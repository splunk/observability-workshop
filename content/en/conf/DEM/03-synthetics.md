---
title: Synthetics
linkTitle: Create a Synthetic test
description: How can Synthetics help?
weight: 3
---

We can see how RUM helpfully captures what end users are experiencing. What's a drawback to only using RUM?

Let's look at a Synthetic test. What is it capturing? 

Now let's create some Synthetic tests on the same site.

1. Go to Synthetics in Observability
1. Click "Add new > Browser Test"
![Add new test](../images/add-test.png)
1. Name the test with three initials that identify you and high level info about the test
   1. For example, "SEW Home Desktop US" 
1. Enter the URL, locations, device type, frequency, and **Save**. We'll wait a few minutes while data is being gathered.
![Synthetic browser test configuration](../images/syn-test-config.png)
1. Take a stretch + water break, and refresh your test page to see what Synthetics has captured.
1. What do the results look like so far? How might this testing be beneficial? Does this spark ideas for more testing?
1. Click on a run result and see the relevant RUM data in the right sidebar.
   1. How does the Synthetics data compare to RUM?
   1. When could comparing Synthetics results to RUM data be helpful?
   1. Why is there a difference between what you see in RUM and Synthetics?
1. We have tests that have been running on our sister retail site. Let's look at the dashboard. What stands out about the data? Now let's see what happens when we change the site.