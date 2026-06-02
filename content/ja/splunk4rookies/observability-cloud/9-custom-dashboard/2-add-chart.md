---
title: コピーしたチャートの追加
linkTitle: 2. コピーしたチャートの追加
weight: 2
hidden: true
---

このセクションでは、**Copy and Paste** 機能を使ってダッシュボードを拡張します。APM Service Dashboard のセクションでいくつかのチャートをコピーしたことを思い出してください。今回はそれらのチャートをダッシュボードに追加します。

{{% exercise title="Request Rate チャートの追加とフィルタリング" %}}

* ページ上部の **2+** を選択し、**Paste charts** を選択します。これでカスタムダッシュボードにチャートが作成されます。
* 現在、チャートはすべての **Environments** と **Services** のデータを表示しているため、自分の environment と **paymentservice** のフィルターを追加しましょう。
* **Request Rate** single value チャートの右上にある 3 点ドット **...** をクリックします。これにより、チャートが編集モードで開きます。
* 新しい画面で、画面中央にある {{% button style="blue" %}}sf_environment:* x{{% /button %}} ボタン **(1)** の **x** をクリックして閉じます。
* {{% button style="blue" %}}**+**{{% /button %}} をクリックして新しいフィルターを追加し、**sf_environment** を選択してドロップダウンから [WORKSHOPNAME] を選び、**Apply** をクリックします。ボタンは **sf_environment:[WORKSHOPNAME]** に変わります。
* {{% button style="blue" %}}sf_service.{{% /button %}} ボタン **(2)** でも同様に、閉じてから **sf_service** の新しいフィルターを作成します。今回は `paymentservice` に変更します。
  ![edit chart](../images/edit-chart.png)
* {{% button style="blue" %}}Save and close {{% /button %}} ボタン **(3)** をクリックします。
* **Request Rate** text チャートでも、前述の 4 ステップを繰り返します。
* 2 つのチャートを更新したら、{{% button style="blue" %}}Save{{% /button %}} をクリックします。
* 新しく貼り付けられたチャートはダッシュボードの一番下に表示されるため、ダッシュボードを再度整理する必要があります。
* 先ほど学んだドラッグ＆ドロップとリサイズの操作を使って、ダッシュボードを下の画像のように整えます。
  ![New dashboard look](../images/copyandpastedcharts.png)
{{% /exercise %}}

次は、実行中の Synthetic テストに基づくカスタムチャートを作成します。
