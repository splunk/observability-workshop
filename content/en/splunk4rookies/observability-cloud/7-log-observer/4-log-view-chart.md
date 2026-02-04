---
title: 4. Log View Chart
weight: 4
---

The next chart type that can be used with logs is the **Log View** chart type. This chart will allow us to see log messages based on predefined filters.

As with the previous Log Timeline chart, we will add a version of this chart to our Customer Health Service Dashboard:

{{% notice title="Info" style="green" title="Exercise" icon="running" %}}

* After the previous exercise make sure you are still in **Log Observer**.
* The filters should be the same as the previous exercise, with the time picker set to the **Last 15 minutes** and filtering on severity=error, `sf_service=paymentservice` and `sf_environment=[WORKSHOPNAME]`.
* Make sure we have the header with just the fields we wanted.
* Click again on **Save** and then **Save to Dashboard**.
* This will again provide you with the Chart creation dialog.
* For the **Chart name** use **Log View**.
* This time Click {{% button style="blue" %}}Select Dashboard{{% /button %}} and search for the Dashboard you created in the previous exercise. You can start by typing your initials in the search box **(1)**.
  ![search dashboard](../images/search-dashboard.png)
* Click on your dashboard name to highlight it **(2)** and click {{% button style="blue" %}}OK{{% /button %}} **(3)**.
* This will return you to the create chart dialog.
* Ensure **Log View** is selected as the **Chart Type**.
  ![log view](../images/log-view.png?classes=left&width=30vw)
* To see your dashboard click {{% button style="blue" %}}Save and go to dashboard{{% /button %}}.
* The result should be similar to the dashboard below: 
  ![Custom Dashboard](../images/log-observer-custom-dashboard.png)
* As the last step in this exercise, let us add your dashboard to your workshop team page, this will make it easy to find later in the workshop.
* At the top of the page, click on the vertical 3 dots menu **⋮** on the top right, select **Dashboard Group Actions** > **Link to teams**.
  ![linking](../images/linking.png) 
* In the following **Link to teams** dialog box, find the Workshop team that your instructor will have provided for you and click {{% button style="blue" %}}Done{{% /button %}}.

{{% /notice %}}

In the next session, we will look at Splunk Synthetics and see how we can automate the testing of web-based applications.
