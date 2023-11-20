---
title: Dashboard Introduction
linkTitle: 1. Dashboard Introduction
weight: 9
---

As we already saved some useful log charts in a dashboard in the Log observer exercise, we are going to extend that dashboard.

{{% notice title="Exercise" style="green" icon="running" %}}

* Go back to your dashboard with the two log charts, by clicking on **Dashboards*, and select your dashboard group from the list of linked dashboards at the bottom of the page. This should bring you back to your previously saved dashboard.

![log list](../images/log-charts.png)

* Even if the log information is useful, it will need more information to have it make sense for our team so lets add a bit more information
* The first step is adding a description chart to the dashboard. Click on the {{% button style="gray" %}}New text note{{% /button %}} and replace the text in the note with below with the text then click  the {{% button style="blue" %}}Save and close{{% /button %}}  button and name the chart **Instructions**
{{% notice title=" information to use with text note" style="info" %}}

```text

This is a Custom Health Dashboard for the **Payment service**,  
Please pay attention to any error in the logs.
For more detail visit [link](https://https://www.splunk.com/en_us/products/observability.html)

```

{{% /notice %}}


add request rate charts and Error rate charts.




{{% /notice %}}


3. Revisit APM, Select explore, and select the payment service.
4. Select the Dashboard option on the top right of the screen.
5. You should now be on the APM services map with the workshop and payment service selected.
6. Click on the three dots **...** and select *Copy*
7. Note that you now have a **1**  before the **+**  at the top right of the page, indicating you have a copied chart in your clipboard available.
8. Find your War room dashboard again.
9. Select the  **1+** at the top of the page and select Past Chart. this will create the chart in your dashboard.
10. Let's add some more, go back to the APM services dashboard either via the APM  or selecting the *APM services* dashboard group followed by the *service* dashboard from **Dashboards**
11. This time select Error rate, click on the **...**  and select copy, do the same for the error rate chart, but this time choose Add to dashboard. This will allow you to select and add multiple charts in one go. Note That the **+** now shows the number of charts copied into the clipboard.
12. Return to your war room dashboard and select past charts from the **+* menu.
13. At this point these charts are not filtered, so let's add the correct filter
14. Add `sf_environment=[WORKSHOPNAME]` and `sf_service=payment_service` to the override filter box.
15. Now with the info for our service let's rearrange the chart so that they are useful
16. Drag the Request rate to the top left, resize its width 50 percent by dragging the left edge, and add the Error rate chart next to it.
17. Drag the error rate chart next to the two the chart and resize it so it fills the page
18. click on **new text note* and replace the text below with the text in the note  then click save  name the chart instructions
{{% notice title=" TExt for Text note" style="info" %}}

```text

This is a  war room dashboard for the **Payment service**,  
Please pay attention  to any error in the logs.
For more detail visit [link](https://https://www.splunk.com/en_us/products/observability.html)

```

{{% /notice %}}
19. Place the instruction below the request rate chart, add the timeline log chart next to it and size it to fit the page.
20. Make sure the Log view chart is the bottom chart, is full size and extended to the bottom of your page.

The result should be like this:
![war room](../images/warroom.png)



{{% notice title="Exercise" style="green" icon="running" %}}

{{% /notice %}}