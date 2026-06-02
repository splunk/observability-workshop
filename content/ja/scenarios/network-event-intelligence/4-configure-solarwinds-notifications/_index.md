---
title: Configure Solarwinds Notifications
linkTitle: 4. Configure Solarwinds Notifications
weight: 4
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---


## 2つ目のアラートソースの追加

このワークショップの重要な目標は、クロスベンダーのアラート相関を実演することです。Cisco Catalyst Center は Cisco インフラストラクチャをカバーしますが、多くのエンタープライズネットワークでは、非 Cisco デバイス、WAN リンク、およびより広範なネットワークヘルスメトリクスを追跡するために、Solarwinds のようなサードパーティ監視ツールにも依存しています。両方のソースが同じサイトまたは同じ時間帯についてアラートを発生させた場合、ITSI はそれぞれに個別のノイズを生成するのではなく、単一のエピソードにグループ化できる必要があります。

**Solarwinds Add-on for Splunk** は詳細なアセットコンテキストを提供できますが、このユースケースでは Solarwinds アラートは Splunk HTTP Event Collector に直接配信されます。ITSI には Solarwinds 用のビルトイン統合テンプレートが含まれており、これらのアラートを正規化して、Catalyst Center アラートなどの他のイベントソースと同じ方法で ITSI に認識されるようにします。

このセクションでは、**Solarwinds Inbound Notification** 接続を設定し、次のセクションの **Notable Event Aggregation Policy** が相関させる2ソースアラートパイプラインを完成させます。

## このセクションで行うこと

このセクションを完了すると、以下が達成されます

- **Solarwinds Inbound Notification** 接続を設定し、これらのアラートに対して ITSI に Notable Events を作成します
- Solarwinds アラートが正規化された Notable Events として ITSI に流入していることを確認します
