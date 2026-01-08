---
title: 1.1 テストの記録
weight: 1
---

## 開始 URL を開く

ワークショップの開始 URL を Chrome で開きます。以下の適切なリンクをクリックして、新しいタブでサイトを開きます。

{{% notice note %}}
ワークショップの開始 URL は **EMEA** と **AMER/APAC** で異なります。お住まいの地域に応じて正しい URL を使用してください。

{{% tabs %}}
{{% tab title="EMEA Workshop URL" %}}

[https://online-boutique-eu.splunko11y.com/](https://online-boutique-eu.splunko11y.com/)

{{% /tab %}}
{{% tab title="AMER/APAC Workshop URL" %}}

[https://online-boutique-us.splunko11y.com/](https://online-boutique-us.splunko11y.com/)

{{% /tab %}}
{{% /tabs %}}
{{% /notice %}}

## Chrome DevTools Recorder を開く

次に、（上記で開いた新しいタブで）Developer Tools を開きます。Windows では `Ctrl + Shift + I`、Mac では `Cmd + Option + I` を押し、トップレベルメニューまたは **More tools** フライアウトメニューから **Recorder** を選択します。

![Open Recorder](../../img/open-recorder.png)

{{% notice title="注意" style="info" %}}
サイトの要素はビューポートの幅によって変わる場合があります。記録する前に、作成するテストの種類（デスクトップ、タブレット、モバイル）に応じてブラウザウィンドウを適切な幅に設定してください。必要に応じて、DevTools の「dock side」を別ウィンドウとしてポップアウトさせると便利です。
{{% /notice %}}

## 新しい記録を作成

DevTools ウィンドウで Recorder パネルを開いた状態で、{{% button style="blue" %}}Create a new recording{{% /button %}} ボタンをクリックして開始します。

![Recorder](../../img/recorder.png)

**Recording Name** には、イニシャルを接頭辞として使用します（例: **`<your initials>` - Online Boutique**）。**Start Recording** をクリックして、アクションの記録を開始します。

![Recording Name](../../img/recording-name.png)

記録が開始されたら、サイトで以下のアクションを実行します:

- **Vintage Camera Lens** をクリック
- **Add to Cart** をクリック
- **Place Order** をクリック
- Recorder パネルの **End recording** をクリック

![End Recording](../../img/end-recording.png)

## 記録のエクスポート

**Export** ボタンをクリックします:

![Export button](../../img/export-button.png)

フォーマットとして **JSON** を選択し、**Save** をクリックします。

![Export JSON](../../img/export-json.png)

![Save JSON](../../img/save-json.png)

**おめでとうございます！** Chrome DevTools Recorder を使用した記録の作成に成功しました。次に、この記録を使用して Splunk Synthetic Monitoring で Real Browser Test を作成します。

---

{{% expand "JSON ファイルを表示するにはここをクリック" %}}

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
