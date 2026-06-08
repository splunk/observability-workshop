---
title: 2. Log Observer への移動
weight: 2
---

{{% notice title="Exercise" style="green" icon="running" %}}

* Splunk Observability Cloud のメインナビゲーションメニューから、**Log Observer** をクリックします。
* 右上のタイムピッカーを使用して、時間範囲を **Last 15 minutes** に設定します。
* フィルターバーで、ワークショップ環境のフィルターを追加します:
  * {{% button style="blue" %}}Add Filter{{% /button %}} をクリックします
  * `deployment.environment` を選択します
  * インストラクターから提供された環境名を値に設定します

<!-- TODO screenshot: Log Observer landing page with time range and environment filter set -->

{{% /notice %}}

Log Observer のランディングページに、2つの主要なエリアが表示されます:

* **Timeline chart**（上部）— 時間経過に伴うログ量を示す棒グラフで、ログアクティビティの概要を一目で確認できます
* **Log table**（下部）— タイムスタンプ、重大度、サービス名、メッセージを含む個別のログエントリです

{{% notice title="Info" style="info" %}}
Log Observer は**ノーコード**フィルタリングで動作します。SPL やクエリ構文を記述する必要はありません。すべてポイント＆クリックで操作できるため、Splunk の経験に関係なく、どのチームメンバーでも利用できます。
{{% /notice %}}
