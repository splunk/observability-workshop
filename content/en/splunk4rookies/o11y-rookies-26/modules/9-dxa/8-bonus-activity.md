---
title: 8. Bonus Activity!
weight: 8
---

Have some extra time? Nice! Let's do a little configuration.

{{% exercise title="Create a new Event Definition" %}}
1. In the DXA project, go to the Event Definitions tab and click "Pick from page"
![DXA Event Definitions table with pick from page button highlighted](../images/dxa-picker.png)
1. Enter the URL where you want to capture a new Event Definition, like a single product page in the Astronomy Shop for this workshop.
1. Activate the Element Picker
1. Select an element on the page to capture, like one of the "Ask AI" prompts or "Show All Reviews", and see how the Element Picker both updates the target element code and provides a preview of how many interactions have been captured recently.
1. Confirm your choice and further edit the new event definition to be clear and readable. You can also choose to further edit the element qualities to be more or less specific, and see how the Occurences preview changes.
1. Save - now your new Event Definition is available to use in Time Series!
{{% /exercise %}}

{{% exercise title="Create a Time Series analysis" %}}
Now, let's show engagement on your new Event Definition over time.
1. Go to the Analyses tab and click New Analysis > Time Series
1. Add your new Event Definition to the first series. Rename the series and add any other filters you'd like.
1. Does it make sense to trend this event alongside another? If so, add another Series!
1. Name the new Time Series and save.
1. Click into a point on the chart and validate that the session replay captures your custom event!
{{% /exercise %}}

{{< tabs >}}
{{% tab title="Question" %}}

What is the value in creating Custom Event Definitions within DXA?

{{% /tab %}}
{{% tab title="Answer" %}}

We can change the analyses we are able to do as often as we'd like, without having to push code changes to our application.

{{% /tab %}}
{{< /tabs >}}