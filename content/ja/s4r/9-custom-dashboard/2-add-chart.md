---
title: チャートの追加
linkTitle: 2. チャートの追加
weight: 2
---

このセクションでは、**コピー＆ペースト**の機能を使用してダッシュボードを拡張します。以前、APMサービスダッシュボードのセクションでチャートをコピーしました。これらのチャートをカスタムダッシュボードに追加します。

{{% notice title="エクササイズ" style="green" icon="running" %}}

* ページの上部にある**2+**を選択し、**Paste charts**を選択して、カスタムダッシュボードにチャートを作成します。
* チャートは現在、すべての**Environments**および**Services**のデータを表示しています。したがって、環境と**paymentservice**のためのフィルタを追加しましょう。
* ページの右上にある**...**（3つのドット）をクリックして、**Request Rate**の単一の値のチャートを編集モードで開きます。
* 新しい画面で、画面の中央にある{{% button style="blue" %}}sf_environment:* x{{% /button %}}ボタン（**1**）の**x**をクリックして閉じます。
* {{% button style="blue" %}}**+**{{% /button %}}をクリックして新しいフィルタを追加し、**sf_environment**を選択して、ドロップダウンから[WORKSHOPNAME]を選択して**Apply**をクリックします。ボタンは**sf_environment:[WORKSHOPNAME]**に変わります。
* 同様に、{{% button style="blue" %}}sf_service.{{% /button %}}ボタン（**2**）に対しても同じ手順を行い、**sf_service**のための新しいフィルタを作成します。ただし、この時は`paymentservice`に変更します。
  ![edit chart](../images/edit-chart.png)
* {{% button style="blue" %}}Save and close{{% /button %}}ボタン（**3**）をクリックします。
* **Request Rate**テキストチャートについても、前述の4つの手順を繰り返します。
* 2つのチャートを更新したら、{{% button style="blue" %}}Save{{% /button %}}をクリックします。
* 新しく貼り付けられたチャートはダッシュボードの一番下に表示されたため、再びダッシュボードを整理する必要があります。
* 以前に学んだドラッグアンドドロップおよびサイズ変更のスキルを使用して、ダッシュボードを以下の画像のように整えます。
  ![New dashboard look](../images/copyandpastedcharts.png)
{{% /notice %}}

次に、実行中のSyntheticテストに基づいたカスタムチャートを作成します。
