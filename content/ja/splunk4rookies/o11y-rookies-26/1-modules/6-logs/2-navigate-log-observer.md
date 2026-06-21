---
title: 2. Log Observer への移動
weight: 2
---

{{% notice title="演習" style="green" icon="running" %}}

* Splunk Observability Cloud のメインナビゲーションメニューから、**Log Observer** をクリックします。
* 右上のタイムピッカーを使用して、時間範囲を **Last 15 minutes** に設定します。
* フィルターバーで、ワークショップ環境のフィルターを追加します
  * {{% button style="blue" %}}Add Filter{{% /button %}} をクリックします
  * `deployment.environment` を選択します
  * インストラクターから提供された環境名を値に設定します

<!-- TODO screenshot: Log Observer landing page with time range and environment filter set -->

{{% /notice %}}

Log Observer のランディングページに、2つの主要なエリアが表示されます

* **タイムラインチャート**（上部）— 時間経過に伴うログ量を示す棒グラフで、ログアクティビティを一目で把握できます
* **ログテーブル**（下部）— タイムスタンプ、重大度、サービス名、メッセージを含む個々のログエントリです

{{% notice title="情報" style="info" %}}
Log Observer は**ノーコード**フィルタリングで動作します — SPL やクエリ構文を記述する必要はありません。すべてがポイント＆クリックで操作でき、Splunk の経験に関係なく、どのチームメンバーでもアクセスできます。
{{% /notice %}}
