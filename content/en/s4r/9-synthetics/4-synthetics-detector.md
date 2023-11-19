---
title: 4. Synthetics Detector
weight: 4
---
Given you can run these tests 24/7, it is an ideal tool to get warned early if your test are failing or starting to run longer then your agreed SLA
instead of getting informed by social media, or Uptime web site's.

![Social media](../images/social-media-post.png)

 To stop that from happening lets detect if our test are taking more then 1.1 minute.

 {{% notice title="Exercise" style="green" icon="running" %}}

* Go back to Synthetics home page via the Menu on the left
* Select the  workshop test again and click the {{% button style="white" %}}Create Detector{{% /button %}} button at the top of the page.  

![synth detector](../images/synth-detector.png)

* First click on the pencil to rename the detector to something meaning full like [YOUR INITIALS - WORKSHOP Detector].
* Ensure that Run Duration and static threshold are selected.
* Set trigger threshold to be around 68000.  Make sure te threshold line is cutting though the long spikes as shown above. (You may have to adjust the threshold value a bit to match your actual latency.)
* Leave the rest as default.
* Note that there are now a row of red and white triangles appeared  below hte spikes. The Red Triangle lets you know the your detector found that your test was above the given threshold & the white triangle indicates the that the result returned to below the threshold. Each red Triangle will trigger an alert.  
* You can change the Alerts criticality by changing the drop down to a different settings, as well of the method of alerting.  Make sure you do **NOT** Add a Recipient. (This wil help your instructor with cleaning up the workshop afterwards.)
* If your interested in the analytics used for this detector you can click the ellipses **⋮**  at the top right of the dialog. This will show you the generated analytics.
* Click Activate to deploy your detector
* This return you to the Synthetic home page, to see if your test is active click on {{% button style="white" %}}Edit Test{{% /button %}} button
* At the bottom of the page there is a list of active detectors,  including the one you just created.

![list of detectors](../images/detector-list.png)

* If you can find your, but see one called *New Synthetic Detector*, you may not saved it correctly with with your name.  click on the *New Synthetic Detector* link, and redo the rename.

{{% /notice %}}
