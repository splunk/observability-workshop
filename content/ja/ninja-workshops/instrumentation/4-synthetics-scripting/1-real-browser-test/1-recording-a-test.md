---
title: 1.1 テストの記録
weight: 1
---

このステップでは、Chrome DevTools Recorder を使用して、デモ用 Online Boutique ストアフロントでの一連のユーザージャーニーをキャプチャします。Recorder はあなたの操作を監視し、各クリック、キー入力、ナビゲーションを構造化されたステップとして記録します。操作対象の各要素について、**複数のセレクター戦略**（CSS、XPath など）をキャプチャするため、結果として得られるテストはほとんどのフロントエンド変更に対して堅牢です。あるセレクターが機能しなくなった場合は、次のセレクターが順番に試行されます。記録は JSON ファイルに保存し、次のステップで Splunk Synthetic Monitoring にインポートします。

## 開始 URL を開く

ワークショップの開始 URL を Chrome で開きます。下記の該当するリンクをクリックして、新しいタブでサイトを開いてください。

{{% notice note %}}
ワークショップの開始 URL は **EMEA** と **AMER/APAC** で異なります。お住まいのリージョンに応じた正しい URL を使用してください。

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

次に、上記で開いた新しいタブで、Windows では `Ctrl + Shift + I`、Mac では `Cmd + Option + I` を押して Developer Tools を開き、トップレベルメニューまたは **More tools** フライアウトメニューから **Recorder** を選択します。

![Open Recorder](../../img/open-recorder.png)

{{% notice title="Note" style="info" %}}
サイトの要素はビューポート幅によって変化することがあります。記録を開始する前に、作成したいテスト（Desktop、Tablet、または Mobile）に合わせてブラウザウィンドウの幅を設定してください。レスポンシブサイトでは、ブレークポイント以下になるとメニュー項目がハンバーガーアイコンの背後に隠れることがよくあります。広いウィンドウで「カートリンクをクリック」と記録しても、テストがモバイルビューポートで実行される場合は正しく再生されません。役立つ場合は、DevTools の「dock side」を変更して別ウィンドウとしてポップアウトさせてください。
{{% /notice %}}

## 新しい記録を作成する

DevTools ウィンドウで Recorder パネルを開いた状態で、{{% button style="blue" %}}Create a new recording{{% /button %}} ボタンをクリックして開始します。

![Recorder](../../img/recorder.png)

**Recording Name** には、自分のイニシャルを記録名のプレフィックスとして使用します（例: **`<your initials>` - Online Boutique**）。**Start Recording** をクリックして、操作の記録を開始します。

![Recording Name](../../img/recording-name.png)

記録が開始されたら、サイトで以下の操作を実行してください。

- **Vintage Camera Lens** をクリック
- **Add to Cart** をクリック
- **Place Order** をクリック
- Recorder パネルの **End recording** をクリック

![End Recording](../../img/end-recording.png)

## 記録のエクスポート

**Export** ボタンをクリックします。

![Export button](../../img/export-button.png)

形式として **JSON** を選択し、**Save** をクリックします。

![Export JSON](../../img/export-json.png)

![Save JSON](../../img/save-json.png)

**おめでとうございます！** Chrome DevTools Recorder を使用して記録を作成できました。次は、この記録を使用して Splunk Synthetic Monitoring で Real Browser Test を作成します。

### JSON の中身は実際にどうなっているか

記録の内容を確認したい場合は、下の展開可能なセクションを開いてください。注目すべき点をいくつか挙げます。

- 各操作は `type`（`navigate`、`click` など）と `selectors` のリストを持つオブジェクトです。これは冒頭で説明した複数戦略のフォールバックです。Recorder は優先順位順にセレクターをリスト化し、テストランナーは一致するものが見つかるまで各セレクターを試行します。
- 最初のステップは `setViewport` で、ウィンドウの寸法を固定します。これにより、どのロケーションから実行しても、テストは常に同じサイズで再生されます。
- ほとんどのクリックステップには、`navigation` の URL とページ `title` を含む `assertedEvents` が含まれます。これは Recorder が期待される結果を固定する方法です。クリックが `/cart` へのナビゲーションを発生させる*べき*なのに発生しない場合、ステップは失敗します。実行結果には、曖昧なタイムアウトではなく、明確なアサーション失敗として表示されます。

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
