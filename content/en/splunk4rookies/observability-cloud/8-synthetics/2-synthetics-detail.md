---
title: 2. Synthetics Test Detail
weight: 2
---

Right now we are looking at the result of a single Synthetic Browser Test. This test is split up into **Business Transactions**, think of this as a group of one or more logically related interactions that represent a business-critical user flow.

{{% notice title="Info" style="info" %}}

The screenshot below doesn't contain a red banner with an error in it however you might be seeing one in your run results. This is expected as in some cases the test run fails and does not impact the workshop.

{{% /notice %}}

![waterfall](../images/synth-waterfall.png)

1. **Filmstrip:** Offers a set of screenshots of site performance so that you can see how the page responds in real-time.
2. **Video:** This lets you see exactly what a user trying to load your site from the location and device of a particular test run would experience.
3. **Waterfall chart**  The waterfall chart is a visual representation of the interaction between the test runner and the site being tested.
4. **Browser test metrics:**  A View that offers you a picture of website performance.

By default, Splunk Synthetics provides screenshots and video capture of the test. This is useful for debugging issues. You can see, for example, the slow loading of large images, the slow rendering of a page etc.

{{% notice title="Exercise" style="green" icon="running" %}}

* Use your mouse to scroll left and right through the filmstrip to see how the site was being rendered during the test run.
* In the Video pane, press on the play button **▶** to see the test playback. If you click the ellipses **⋮** you can change the *playback speed*, view it *Picture in Picture* and even *Download* the video.
* In the waterfall find the line **GET** *splunk-otel-web.js*.
* Click on the **>** button to open the metadata section to see the Request/Response Header information.

{{% /notice %}}
