---
title: SolarWinds 通知の設定
linkTitle: 4. SolarWinds 通知の設定
weight: 4
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px;">

## 2つ目のアラートソースの追加

このワークショップの主要な目標は、クロスベンダーのアラート相関を実演することです。Cisco Catalyst Center は Cisco インフラストラクチャをカバーしますが、多くのエンタープライズネットワークでは、Cisco 以外のデバイス、WAN リンク、およびより広範なネットワークヘルスメトリクスを監視するために、SolarWinds のようなサードパーティ監視ツールにも依存しています。両方のソースが同じサイトまたは同じ時間帯についてアラートを発生させた場合、ITSI はそれぞれに個別のノイズを生成するのではなく、単一のエピソードにグループ化できるべきです。

**SolarWinds Add-on for Splunk** は詳細なアセットコンテキストを提供できますが、このユースケースでは SolarWinds アラートは Splunk HTTP Event Collector に直接配信されます。Content Pack for Cisco Enterprise Networks には、これらのアラートを正規化して Catalyst Center アラートと同じ方法で ITSI に認識させるための事前構築済みの統合テンプレートが含まれています。

このセクションでは、SolarWinds Content Pack をインストールし、インバウンド通知接続を設定します。これにより、次のセクションで NEAP が相関させる2ソースアラートパイプラインが完成します。

## このセクションで行うこと

このセクションを完了すると、以下が達成されます:

- **SolarWinds Content Pack** のインストールとインバウンド通知接続の設定
- SolarWinds アラートが正規化されたノータブルイベントとして ITSI に流入していることの確認

</div>
