---
title: 5. Detectorの作成
weight: 5
---

{{% exercise title="アラートの設定" %}}

* メインメニューから **Digital Experience → Synthetics tests** に移動します。
* ワークショップテスト **[NAME OF WORKSHOP]** を選択します。
* テストをクリックします。
* ページ上部の {{% button %}}**Create Detector**{{% /button %}} ボタンをクリックします。
* アラート条件を変更し、メトリクスを **Run Duration** **(1)**（Uptimeではなく）に、条件を **Static Threshold** に設定します。
* **Trigger threshold** **(2)** を `50000` ms前後に設定します。
* **Split by location** **(3)** を **No** に設定します。
* チャートのスパイクの下に、赤と白の三角形の列が表示されていることを確認します。
* 赤い三角形は、テストが指定されたしきい値を超えたことをDetectorが検出したことを示し、白い三角形は結果がしきい値を下回ったことを示します。赤い三角形ごとにアラートがトリガーされます。

> [!WARNING] メールにアラートが大量に届くことを避けるため、受信者の追加やDetectorの有効化は行いません。

![Detector](../images/synth-detector.png)

このアプリケーションは頻繁に失敗するように設計されているため、多数のアラートが生成されます。実際のシナリオでは、誤検知を避けるためにしきい値を適切に調整する必要があります。

{{% /exercise %}}
