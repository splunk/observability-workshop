---
title: 1.1 テストの記録
weight: 1
---

このステップでは、Chrome DevTools Recorderを使用して、デモ用Online Boutiqueストアフロントでの完全なユーザージャーニーをキャプチャします。Recorderは操作を監視し、各クリック、キー入力、ナビゲーションを構造化されたステップとして記録します。操作した各要素に対して **複数のセレクター戦略**（CSS、XPathなど）をキャプチャするため、生成されたテストはほとんどのフロントエンド変更に対して堅牢です。1つのセレクターが機能しなくなっても、次のセレクターが順番に試行されます。記録をJSONファイルに保存し、次のステップでSplunk Synthetic Monitoringにインポートします。

## 開始URLを開く

Chromeでワークショップの開始URLを開きます。以下の適切なリンクをクリックして、新しいタブでサイトを開きます。

{{% notice note %}}
ワークショップの開始URLは **EMEA** と **AMER/APAC** で異なります。お住まいの地域に合ったURLを使用してください。

{{% tabs %}}
{{% tab title="EMEA ワークショップURL" %}}

[https://online-boutique-eu.splunko11y.com/](https://online-boutique-eu.splunko11y.com/)

{{% /tab %}}
{{% tab title="AMER/APAC ワークショップURL" %}}

[https://online-boutique-us.splunko11y.com/](https://online-boutique-us.splunko11y.com/)

{{% /tab %}}
{{% /tabs %}}
{{% /notice %}}

## Chrome DevTools Recorderを開く

次に、（上記で開いた新しいタブで）Developer Toolsを開きます。Windowsでは `Ctrl + Shift + I`、Macでは `Cmd + Option + I` を押し、トップレベルメニューまたは **More tools** フライアウトメニューから **Recorder** を選択します。

![Open Recorder](../../img/open-recorder.png)

{{% notice title="注意" style="info" %}}
サイトの要素はビューポートの幅によって変わる場合があります。記録する前に、作成したいテストに適した幅（デスクトップ、タブレット、またはモバイル）にブラウザウィンドウを設定してください。レスポンシブサイトでは、ブレークポイント以下でメニュー項目がハンバーガーアイコンの後ろに隠れることがよくあります。広いウィンドウで「カートリンクをクリック」と記録しても、テストがモバイルビューポートで実行されると正しく再生されません。DevToolsの「dock side」を変更して別ウィンドウとしてポップアウトすると便利です。
{{% /notice %}}

## 新しい記録を作成する

DevToolsウィンドウでRecorderパネルを開いた状態で、{{% button style="blue" %}}Create a new recording{{% /button %}} ボタンをクリックして開始します。

![Recorder](../../img/recorder.png)

**Recording Name** には、イニシャルを記録名のプレフィックスとして使用します（例: **`<your initials>` - Online Boutique**）。**Start Recording** をクリックして操作の記録を開始します。

![Recording Name](../../img/recording-name.png)

記録が開始されたら、サイトで以下の操作を行います。

- **Vintage Camera Lens** をクリックします
- **Add to Cart** をクリックします
- **Place Order** をクリックします
- Recorderパネルで **End recording** をクリックします

![End Recording](../../img/end-recording.png)

## 記録のエクスポート

**Export** ボタンをクリックします。

![Export button](../../img/export-button.png)

フォーマットとして **JSON** を選択し、**Save** をクリックします。

![Export JSON](../../img/export-json.png)

![Save JSON](../../img/save-json.png)

**おめでとうございます!** Chrome DevTools Recorderを使用して記録を正常に作成できました。次に、この記録を使用してSplunk Synthetic MonitoringでReal Browser Testを作成します。

### JSONの中身

記録を確認したい場合は、以下の展開可能なセクションを開いてください。注目すべきポイントがいくつかあります。

- 各操作は `type`（`navigate`、`click` など）と `selectors` のリストを持つオブジェクトです。これが冒頭で説明したマルチ戦略フォールバックです。Recorderは優先順位順にリストし、テストランナーは一致するものが見つかるまで順番に試行します。
- 最初のステップは `setViewport` で、ウィンドウのサイズを固定するため、テストはどのロケーションから実行されても常に同じサイズで再生されます。
- ほとんどのクリックステップには、ナビゲーションURLとページ `title` を含む `assertedEvents` が含まれています。これはRecorderが期待される結果をロックする方法です。クリックが `/cart` へのナビゲーションを *結果として生じるべき* なのに生じない場合、ステップは失敗します。実行結果では、曖昧なタイムアウトではなく明確なアサーション失敗として表示されます。

---

{{% expand "JSONファイルを表示するにはここをクリック" %}}

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
