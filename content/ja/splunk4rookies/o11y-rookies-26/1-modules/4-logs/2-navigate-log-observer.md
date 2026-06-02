---
title: 2. Log Observerへの移動
weight: 2
---

{{% notice title="演習" style="green" icon="running" %}}

* Splunk Observability Cloudのメインナビゲーションメニューから、**Log Observer**をクリックします。
* 右上のタイムピッカーで時間範囲を**Last 15 minutes**に設定します。
* フィルターバーで、ワークショップ環境のフィルターを追加します。
  * {{% button style="blue" %}}Add Filter{{% /button %}}をクリックします
  * `deployment.environment`を選択します
  * 値にインストラクターから提供された環境名を設定します

<!-- TODO screenshot: Log Observer landing page with time range and environment filter set -->

{{% /notice %}}

これで、Log Observerのランディングページに2つのメインエリアが表示されます。

* **Timelineチャート**（上部）— ログの量を時系列で示す棒グラフで、ログのアクティビティを一目で確認できます
* **Logテーブル**（下部）— タイムスタンプ、重大度、サービス名、メッセージを含む個別のログエントリ

{{% notice title="情報" style="info" %}}
Log Observerは**ノーコード**フィルタリングで動作します。SPLやクエリ構文を記述する必要はまったくありません。すべての操作がポイント＆クリックで完結するため、Splunkの経験に関係なく、あらゆるチームメンバーが利用できます。
{{% /notice %}}
