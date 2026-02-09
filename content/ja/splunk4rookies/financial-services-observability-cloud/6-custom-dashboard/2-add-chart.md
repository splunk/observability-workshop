---
title: コピーしたチャートの追加
linkTitle: 2. コピーしたチャートの追加
weight: 2
hidden: true
---

このセクションでは、**コピー＆ペースト**機能を使用してダッシュボードを拡張します。APM Service Dashboard のセクションでいくつかのチャートをコピーしたことを覚えていますか。ここでそれらのチャートをダッシュボードに追加します。

{{% notice title="Exercise" style="green" icon="running" %}}

* ページ上部の **2+** を選択し、**Paste charts** を選択します。これにより、カスタムダッシュボードにチャートが作成されます。
* チャートは現在、すべての **Environments** と **Services** のデータを表示しているため、自分の環境と **paymentservice** のフィルタを追加しましょう。
* **Request Rate** 単一値チャートの右上にある3つのドット **...** をクリックします。これにより、チャートが編集モードで開きます。
* 新しい画面で、画面中央の {{% button style="blue" %}}sf_environment:* x{{% /button %}} ボタン **(1)** の **x** をクリックして閉じます。
* {{% button style="blue" %}}**+**{{% /button %}} をクリックして新しいフィルタを追加し、**sf_environment** を選択してから、ドロップダウンから [WORKSHOPNAME] を選択し、**Apply** をクリックします。ボタンが **sf_environment:[WORKSHOPNAME]** に変わります。
* {{% button style="blue" %}}sf_service.{{% /button %}} ボタン **(2)** についても同様に行います。閉じてから **sf_service** の新しいフィルタを作成します。ただし、今回は `paymentservice` に変更します。
  ![edit chart](../images/edit-chart.png)
* {{% button style="blue" %}}Save and close {{% /button %}} ボタン **(3)** をクリックします。
* **Request Rate** テキストチャートについても、前の4つの手順を繰り返します。
* 2つのチャートを更新したら、{{% button style="blue" %}}Save{{% /button %}} をクリックします。
* 新しく貼り付けたチャートはダッシュボードの下部に表示されるため、ダッシュボードを再度整理する必要があります。
* 先ほど学んだドラッグ＆ドロップとリサイズのスキルを使用して、ダッシュボードを下の画像のようにしてください。
  ![New dashboard look](../images/copyandpastedcharts.png)
{{% /notice %}}

次に、実行中の Synthetic テストに基づいてカスタムチャートを作成します。
