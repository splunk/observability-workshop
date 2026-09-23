---
title: 3. Synthetic Run Details
weight: 3
---

The run details page shows what the synthetic user experienced during this specific test run. The failure summary identifies the affected transaction and step, while the filmstrip and video let you review how the application behaved leading up to the failure.

{{% exercise title="Inspect the failed test run" %}}

* Review the **failure summary (1)**. Note the *synthetic transaction*, *failed step*, and r*eported error*.
* Open **Filter** by a synthetic transaction, page, or step (2) and select **Place Order** under Synthetic transactions. This limits the view to the checkout portion of the journey.
* Review the **filmstrip (3)** from left to right to see how the *Astronomy Shop* appeared as the test progressed.
* In the **Video** pane, select **Play (4)** to watch the recorded test journey.

Compare the final screenshots and video with the failure summary. Identify what the synthetic user was waiting for when the test timed out.

<!-- * Use your mouse to scroll left and right through the filmstrip to see how the site was being rendered during the test run.
* In the Video pane, press on the play button **▶** **(1)** to see the test playback.
* Using the filter above the filmstrip, under the heading **Filter by a synthetic transaction, page, or step** **(2)**, click on **Place Order** under **Synthetic transactions**. -->

![waterfall](../images/synth-waterfall.png)

{{< tabs >}}
{{% tab title="Question" %}}
* **Which step failed, and what condition caused the test to time out?** 
{{% /tab %}}
{{% tab title="Answers" %}}
**Step 6 – confirm checkout failed. The test timed out because the expected confirmation text, “We’ve sent you a confirmation email,” did not appear within the allowed time.**
{{% /tab %}}
{{< /tabs >}}

{{% /exercise %}}
