---
title: 5. Detector の作成
weight: 5
---

{{% exercise title="アラートを受け取る" %}}

* メインメニューから **Digital Experience → Synthetics tests** に移動します。
* ワークショップのテスト **[NAME OF WORKSHOP]** を選択します。
* テストをクリックします。
* ページ上部の {{% button %}}**Create Detector**{{% /button %}} ボタンをクリックします。
* アラート基準を変更し、メトリクスが **Run Duration** **(1)** （Uptime ではなく）、条件が **Static Threshold** になるようにします。
* **Trigger threshold** **(2)** を `50000` ms 程度に設定します。
* **Split by location** **(3)** を **No** に設定します。
* チャートのスパイクの下に、赤と白の三角形の行が表示されていることを確認してください。
* 赤い三角形は、Detector がテストが指定したしきい値を超えたことを検出したことを示し、白い三角形は結果がしきい値以下に戻ったことを示します。それぞれの赤い三角形はアラートをトリガーします。

> [!WARNING] アラートでメールを大量に受け取らないようにするため、受信者の追加や Detector の有効化は行いません。

![Detector](../images/synth-detector.png)

* このアプリケーションは常に失敗するように設計されているため、多数のアラートが生成されます。実際のシナリオでは、誤検知を避けるためにしきい値を微調整することになります。

{{% /exercise %}}
