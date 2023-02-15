---
title: ダッシュボードにチャートを追加する
linkTitle: 3.5 さらにチャートを追加
weight: 5
isCJKLanguage: true
---

## 1. 既存のダッシュボードに保存する

右上に **YOUR_NAME-Dashboard** と表示されていることを確認しましょう

これは、あなたのチャートがこのダッシュボードに保存されることを意味します。

チャートの名前を **Latency History** とし、必要に応じてチャートの説明を追加します。

![Save Chart 1](../../images/M-MoreCharts-1.png)

{{< labelbutton  >}}Save And Close{{< /labelbutton >}} をクリックします。これで、ダッシュボードに戻ると2つのチャートが表示されているはずです！

![Save Chart 2](../../images/M-MoreCharts-2.png)
では、先ほどのチャートを元に、もう一つのチャートをさくっと追加してみましょう。

## 2. チャートのコピー＆ペースト

ダッシュボードの **Latency History** チャート上の3つのドット **`...`** をクリックし、 **Copy** をクリックします。

![Copy chart](../../images/M-MoreCharts-3.png)

ページ左上の **+** の横に赤い円と白い1が表示されていれば、チャートがコピーされているということになります。

ページ上部の ![red one](../../images/M-MoreCharts-4.png) をクリックし、メニューの *Paste Charts* をクリックしてください (また、右側に 1 が見える赤い点があるはずです)。

![Past charts](../../images/M-MoreCharts-5.png)

これにより、先程のチャートのコピーがダッシュボードに配置されます。

![Three Dashboard](../../images/M-MoreCharts-6.png)


## 3. 貼り付けたチャートを編集する

ダッシュボードの **Latency History** チャートの3つの点 **`...`** をクリックし、**Open** をクリックします（または、チャートの名前（ここでは **Latency History**）をクリックすることもできます）。

すると、再び編集できる環境になります。

まず、チャートの右上にあるタイムボックスで、チャートの時間を -1h（1時間前から現在まで） に設定します。そして、シグナル「*A*」の前にある目のアイコンをクリックして再び表示させ、「*C*」 を非表示にし、*Latency history* の名前を **Latency vs Load** に変更します。

![Set Visibility](../../images/M-MoreCharts-7.png)

{{% labelbutton color="ui-button-blue" %}}Add Metric Or Event{{% /labelbutton %}} ボタンをクリックします。これにより、新しいシグナルのボックスが表示されます。シグナル **D** に `demo.trans.count` と入力・選択します。

![Dashboard Info](../../images/M-MoreCharts-8.png)

これにより、チャートに新しいシグナル **D** が追加され、アクティブなリクエストの数が表示されます。*demo_datacenter:Paris* のフィルタを追加してから、 **Configure Plot** ボタンをクリックしロールアップを **Auto (Delta)** から **Rate/sec** に変更します。名前を **demo.trans.count** から **Latency vs Load** に変更します。

![rollup change](../../images/M-MoreCharts-9.png)

最後に {{< labelbutton  >}}Save And Close{{< /labelbutton >}} ボタンを押します。これでダッシュボードに戻り、3つの異なるチャートが表示されます。

![three charts](../../images/M-MoreCharts-10.png)

次のモジュールでは、「説明」のメモを追加して、チャートを並べてみましょう！
