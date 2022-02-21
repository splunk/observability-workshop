# ダッシュボードにチャートを追加する

それでは、チャートを保存してみましょう。

---

## 1. 既存のダッシュボードに保存する

右上に **YOUR_NAME-Dashboard** と表示されていることを確認しましょう

これは、あなたのチャートがこのダッシュボードに保存されることを意味します。

チャートの名前を **Latency History** とし、必要に応じてチャートの説明を追加します。

![Save Chart 1](../images/dashboards/M-MoreCharts-1.png)

**Save And Close**{: .label-button .sfx-ui-button-blue} をクリックします。これで、ダッシュボードに戻ると2つのチャートが表示されているはずです！

![Save Chart 2](../images/dashboards/M-MoreCharts-2.png)
では、先ほどのチャートを元に、もう一つのチャートをさくっと追加してみましょう。

---

## 2. チャートのコピー＆ペースト

ダッシュボードの **Latency History** チャート上の3つのドット **`...`** をクリックし、 **Copy** をクリックします。

![Copy chart](../images/dashboards/M-MoreCharts-3.png)

ページ左上の **+** の横に赤い円と白い1が表示されていれば、チャートがコピーされているということになります。

ページ上部の ![red one](../images/dashboards/M-MoreCharts-4.png) をクリックし、メニューの *Paste Charts* をクリックしてください (また、行の最後に 1 が見える赤い点があるはずです)。

![Past charts](../images/dashboards/M-MoreCharts-5.png)

これにより、先程のチャートのコピーがダッシュボードに配置されます。

![Three Dashboard](../images/dashboards/M-MoreCharts-6.png)

---

## 3. 貼り付けたチャートを編集する

ダッシュボードの **Latency History** チャートの3つの点 **`...`** をクリックし、**Open** をクリックします（または、チャートの名前（ここでは **Latency History**）をクリックすることもできます）。

すると、再び編集できる環境になります。

まず、チャートの右上にあるタイムボックスで、チャートの時間を -1h（1時間前から現在まで） に設定します。そして、シグナル「*A*」の前にある目のアイコンをクリックして再び表示させ、「*C*」 を非表示にし、*Latency history* の名前を **Latency vs Load** に変更します。

![Set Visibility](../images/dashboards/M-MoreCharts-7.png)

**Add Metric Or Event**{: .label-button .sfx-ui-button-blue} ボタンをクリックします。これにより、新しいシグナルのボックスが表示されます。シグナル **D** に `demo.trans.count` と入力・選択します。

![Dashboard Info](../images/dashboards/M-MoreCharts-8.png)

これにより、チャートに新しいシグナル **D** が追加され、アクティブなリクエストの数が表示されます。*demo_datacenter:Paris* のフィルタを追加してから、**Delta Rollup** をクリック（または歯車のアイコンをクリック）し、ロールアップタイプを変更します。

![rollup change](../images/dashboards/M-MoreCharts-9.png)

ビジュアライゼーションのパネルが開いたら、Rollup ドロップダウンを **Rollup:Rate/sec** に変更し、左上の名前フィールドをクリックして **Latency vs load** に変更し、**Save And Close**{: .label-button .sfx-ui-button-blue} ボタンを押します。これでダッシュボードに戻り、3つの異なるチャートが表示されます。

![three charts](../images/dashboards/M-MoreCharts-10.png)

次のモジュールでは、「説明」のメモを追加して、チャートを並べてみましょう!
