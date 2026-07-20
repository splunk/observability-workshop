---
title: 1.1 Recording a test
weight: 1
---

In this step you'll capture a complete user journey through the demo Online Boutique storefront using the Chrome DevTools Recorder. The recorder watches your interactions and records each click, keystroke, and navigation as a structured step. For every element you interact with it captures **multiple selector strategies** (CSS, XPath, etc.), so the resulting test is robust against most front-end changes — if one selector breaks the next is tried in turn. You'll save the recording to a JSON file that you'll import into Splunk Synthetic Monitoring in the next step.

## Open the starting URL

Open the starting URL for the workshop in Chrome. Click on the appropriate link below to open the site in a new tab.

{{% notice note %}}
The starting URL for the workshop is different for **EMEA** and **AMER/APAC**. Please use the correct URL for your region.

{{% tabs %}}
{{% tab title="EMEA Workshop URL" %}}

[https://online-boutique-eu.splunko11y.com/](https://online-boutique-eu.splunko11y.com/)

{{% /tab %}}
{{% tab title="AMER/APAC Workshop URL" %}}

[https://online-boutique-us.splunko11y.com/](https://online-boutique-us.splunko11y.com/)

{{% /tab %}}
{{% /tabs %}}
{{% /notice %}}

## Open the Chrome DevTools Recorder

Next, open the Developer Tools (in the new tab that was opened above) by pressing `Ctrl + Shift + I` on Windows or `Cmd + Option + I` on a Mac, then select **Recorder** from the top-level menu or the **More tools** flyout menu.

![Open Recorder](../../img/open-recorder.png)

{{% notice title="Note" style="info" %}}
Site elements might change depending on viewport width. Before recording, set your browser window to the correct width for the test you want to create (Desktop, Tablet, or Mobile). Responsive sites often hide menu items behind a hamburger icon below a breakpoint — recording a "click the cart link" on a wide window won't replay correctly if the test runs at a mobile viewport. Change the DevTools "dock side" to pop out as a separate window if it helps.
{{% /notice %}}

## Create a new recording

With the Recorder panel open in the DevTools window. Click on the {{% button style="blue" %}}Create a new recording{{% /button %}} button to start.

![Recorder](../../img/recorder.png)

For the **Recording Name** use your initials to prefix the name of the recording e.g. **`<your initials>` - Online Boutique**. Click on **Start Recording** to start recording your actions.

![Recording Name](../../img/recording-name.png)

Now that we are recording, complete the following actions on the site:

- Click on **Vintage Camera Lens**
- Click on **Add to Cart**
- Click on **Place Order**
- Click on **End recording** in the Recorder panel.

![End Recording](../../img/end-recording.png)

## Exporting the recording

Click on the **Export** button:

![Export button](../../img/export-button.png)

Select **JSON** as the format, then click on **Save**

![Export JSON](../../img/export-json.png)

![Save JSON](../../img/save-json.png)

**Congratulations!** You have successfully created a recording using the Chrome DevTools Recorder. Next, we will use this recording to create a Real Browser Test in Splunk Synthetic Monitoring.

### What's actually in the JSON?

Open the expandable below if you'd like to inspect the recording. A few things worth noticing:

- Each interaction is an object with a `type` (`navigate`, `click`, etc.) and a list of `selectors` — that's the multi-strategy fallback we mentioned at the start. The recorder lists them in priority order; the test runner tries each until one matches.
- The first step is a `setViewport`, which pins the window dimensions so the test always replays at the same size regardless of which location it runs from.
- Most click steps include `assertedEvents` with a `navigation` URL and page `title`. These are the recorder's way of locking in expected outcomes — if a click *should* result in a navigation to `/cart` and it doesn't, the step fails. You'll see this surface in run results as a clear assertion failure rather than a vague timeout.

---

{{% expand "Click here to view the JSON file" %}}

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
            "url": "https://online-boutique-eu.splunko11y.com/",
            "assertedEvents": [
                {
                    "type": "navigation",
                    "url": "https://online-boutique-eu.splunko11y.com/",
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
                    "url": "https://online-boutique-eu.splunko11y.com/product/66VCHSJNUP",
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
                    "url": "https://online-boutique-eu.splunko11y.com/cart",
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
                    "url": "https://online-boutique-eu.splunko11y.com/cart/checkout",
                    "title": ""
                }
            ]
        }
    ]
}
```

{{% /expand %}}
