---
title: Record a test
linkTitle: 1. Record a test
weight: 1
---

Write down a short user journey you want to test. Remember: smaller bites are easier to chew! In other words, get started with just a few steps. This is easier not only to create and maintain the test, but also to understand and act on the results. Test the essential features to your users, like a support contact form, login widget, or date picker.

{{% notice note %}}
Record the test in the same type of viewport that you want to run it. For example, if you want to run a test on a mobile viewport, narrow your browser width to mobile and refresh before starting the recording. This way you are capturing the correct elements that could change depending on responsive style rules.
{{% /notice %}}

Open your starting URL in Chrome Incognito. This is important so you're not carrying cookies into the recording, which we won't set up in the Synthetic test by default. If you workshop instructor does not have a custom URL, feel free to use [https://online-boutique-eu.splunko11y.com](https://online-boutique-eu.splunko11y.com) or [https://online-boutique-us.splunko11y.com](https://online-boutique-us.splunko11y.com), which are in the examples below.

## Open the Chrome DevTools Recorder

Next, open the Developer Tools (in the new tab that was opened above) by pressing `Ctrl + Shift + I` on Windows or `Cmd + Option + I` on a Mac, then select **Recorder** from the top-level menu or the **More tools** flyout menu.

![Open Recorder](../../_img/open-recorder.png)

{{% notice title="Note" style="info" %}}
Site elements might change depending on viewport width. Before recording, set your browser window to the correct width for the test you want to create (Desktop, Tablet, or Mobile). Change the DevTools "dock side" to pop out as a separate window if it helps.
{{% /notice %}}

## Create a new recording

With the Recorder panel open in the DevTools window. Click on the {{% button style="blue" %}}Create a new recording{{% /button %}} button to start.

![Recorder](../../_img/recorder.png)

For the **Recording Name** use your initials to prefix the name of the recording e.g. **`<your initials>` - `<website name>`**. Click on **Start Recording** to start recording your actions.

![Recording Name](../../_img/recording-name.png)

Now that we are recording, complete a few actions on the site. An example for our demo site is:

- Click on **Vintage Camera Lens**
- Click on **Add to Cart**
- Click on **Place Order**
- Click on **End recording** in the Recorder panel.

![End Recording](../../_img/end-recording.png)

## Export the recording

Click on the **Export** button:

![Export button](../../_img/export-button.png)

Select **JSON** as the format, then click on **Save**

![Export JSON](../../_img/export-json.png)

![Save JSON](../../_img/save-json.png)

**Congratulations!** You have successfully created a recording using the Chrome DevTools Recorder. Next, we will use this recording to create a Real Browser Test in Splunk Synthetic Monitoring.

---

{{% expand "View the example JSON file for this browser test recording" %}}

```json
{
    "title": "RWC - Online Boutique",
    "steps": [
        {
            "type": "setViewport",
            "width": 1430,
            "height": 1016,
            "deviceScaleFactor": 1,
            "isMobile": false,
            "hasTouch": false,
            "isLandscape": false
        },
        {
            "type": "navigate",
            "url": "https://online-boutique-eu.o11ystore.com/",
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://online-boutique-eu.o11ystore.com/",
                    "title": "Online Boutique"
                }
            ]
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "div:nth-of-type(2) > div:nth-of-type(2) a > div"
                ],
                [
                    "xpath//html/body/main/div/div/div[2]/div[2]/div/a/div"
                ],
                [
                    "pierce/div:nth-of-type(2) > div:nth-of-type(2) a > div"
                ]
            ],
            "offsetY": 170,
            "offsetX": 180,
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://online-boutique-eu.o11ystore.com/product/66VCHSJNUP",
                    "title": ""
                }
            ]
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/ADD TO CART"
                ],
                [
                    "button"
                ],
                [
                    "xpath//html/body/main/div[1]/div/div[2]/div/form/div/button"
                ],
                [
                    "pierce/button"
                ],
                [
                    "text/Add to Cart"
                ]
            ],
            "offsetY": 35.0078125,
            "offsetX": 46.4140625,
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://online-boutique-eu.o11ystore.com/cart",
                    "title": ""
                }
            ]
        },
        {
            "type": "click",
            "target": "main",
            "selectors": [
                [
                    "aria/PLACE ORDER"
                ],
                [
                    "div > div > div.py-3 button"
                ],
                [
                    "xpath//html/body/main/div/div/div[4]/div/form/div[4]/button"
                ],
                [
                    "pierce/div > div > div.py-3 button"
                ],
                [
                    "text/Place order"
                ]
            ],
            "offsetY": 29.8125,
            "offsetX": 66.8203125,
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://online-boutique-eu.o11ystore.com/cart/checkout",
                    "title": ""
                }
            ]
        }
    ]
}
```

{{% /expand %}}
