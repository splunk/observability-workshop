---
title: Synthetics
linkTitle: Create a Synthetic test
description: How can Synthetics help?
weight: 3
---

We can see how RUM helpfully captures what end users are experiencing. What's a drawback to only using RUM?

Now let's create some Synthetic tests. You can use any public website, including the [workshop demo site](https://frothly.notsplunktshirtco.com/), or your own business site - just remember that everyone in this workshop org will see the results!

1. Go to Synthetics in Observability
1. Click "Add new > Browser Test"
![Add new test](../images/add-test.png)
1. Name the test with three initials that identify you and high level info about the test
   1. For example, "[sitename] SEW Home Desktop US" 
1. Enter the URL, locations, device type, frequency, and **Save**. We'll wait a few minutes while data is being gathered.
![Synthetic browser test configuration](../images/syn-test-config.png)

## Optional: compare to other websites
Create one or more Synthetic Browser Tests on your competitors' websites, **with your initials in the title of the tests** -- this will be important to compare results later. If you want to make multiple tests with the same configuration, use the "copy" feature.

{{% notice title="Tip on comparing metrics" style="info" %}}
Make sure you're comparing apples to apples whenever possible. For example, if you want to see how your homepage compares to your competitors, make sure to not only have all tests on homepages, but also make sure the connection speed, device type, and locations are the same - because these are variables that change performance.

One way to do this is to **copy** an existing test with the configuration you want, rename the test, and update the URL.
{{% /notice %}}

## Optional bonus: multi-step browser tests
1. We'll do a quick walk-through of creating a multi-step browser test.
   1. Using the Chrome recorder to import JSON
   1. Manually building steps 
1. Reference this [Chrome recorder video](https://splunkvideo.hubs.vidyard.com/watch/xNahnFPGDEoHfzucEVtVeE) for more guidance on using the Import feature, which is a quick way to start capturing elements.
1. See this [Lantern article with more tips about multi-step browser tests](https://lantern.splunk.com/Observability/Use_Cases/Digital_Experience_Monitoring/Running_Synthetics_browser_tests/Selectors_for_multi-step_browser_tests). 

{{% notice title="Gather data and hydrate!" style="info" %}}
Take a stretch + water break, and refresh your test page to see what Synthetics has captured.
{{% /notice %}}
