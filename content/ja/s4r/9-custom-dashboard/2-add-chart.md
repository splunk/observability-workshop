---
title: コピーしたチャートの追加
linkTitle: 2. コピーしたチャートの追加
weight: 2
---

このセクションでは、**コピー＆ペースト**の機能を使用してダッシュボードを拡張します。以前、APMサービスダッシュボードのセクションでチャートをコピーしました。これらのチャートをカスタムダッシュボードに追加します。

{{% notice title="Exercise" style="green" icon="running" %}}

* ページの上部にある **2+** を選択し、**Paste charts** を選択します。カスタムダッシュボードにチャートを作成することができます。
* チャートは現在、すべての **Environments** および **Services** のデータを表示しています。したがって、環境名と **paymentservice** にフィルタする設定を追加しましょう。
* **Request Rate** の単一の値が表示されているチャートの右上にある **...**（3つのドット）をクリックします。すると、このチャートが編集モードで開かれます。
* 新しい画面で、画面の中央にある{{% button style="blue" %}}sf_environment:* x{{% /button %}} ボタン（**1**）の **x** をクリックして閉じます。
* 次に、{{% button style="blue" %}}**+**{{% /button %}}をクリックして新しいフィルタを追加します。**sf_environment** を選択して、ドロップダウンから **[WORKSHOPNAME]** を選択して **Apply** をクリックします。ボタンは **sf_environment:[WORKSHOPNAME]** に変わります。
* 同様の操作を {{% button style="blue" %}}sf_service{{% /button %}} ボタン（**2**）に対して行います。 一度今の設定を削除して、**sf_service** に関するフィルタ設定を作成します。フィルタの対象として、`paymentservice` を指定します。
  ![edit chart](../images/edit-chart.png)
* 設定が完了したら、{{% button style="blue" %}}Save and close{{% /button %}} ボタン（**3**）をクリックします。
* **Request Rate** の数値を表示しているチャートについても、前述の4つの手順を繰り返します。
* 2つのチャートを更新したら、{{% button style="blue" %}}Save{{% /button %}} をクリックします。
* 新しく貼り付けられたチャートはダッシュボードの一番下に表示されたため、再びダッシュボードを並べ替える必要があります。
* 既に学んだドラッグアンドドロップおよびサイズ変更を行い、ダッシュボードを以下の画像のように整えます。
  ![New dashboard look](../images/copyandpastedcharts.png)
{{% /notice %}}

次に、実行中の Synthetic テストに基づいたカスタムチャートを作成します。
