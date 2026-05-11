---
title: Catalyst Center サービスを ITSI にインポートする
linkTitle: 2. Catalyst Center サービスを ITSI にインポートする
weight: 2
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---
<div style="max-width: 80%; margin: 0 auto; font-size: 18px;">

## デバイスヘルスからロケーションベースのネットワーク可視化へ

従来のネットワーク監視ツールは、個々のデバイスについてレポートします（ルーターが稼働しているか停止しているか、スイッチに到達可能かどうかなど）。このレベルの可視性では、*何が*障害を起こしたかはわかりますが、*どこで影響が発生しているか*や*ビジネスにとってどの程度深刻か*はわかりません。ブランチオフィスのディストリビューションスイッチがパフォーマンス低下し始めた場合、運用チームがサイト全体に影響が及んでいることを把握するために、複数のツールのアラートを手動で関連付ける必要があってはなりません。

このセクションでは、そのギャップに対処します。**Content Pack for Cisco Enterprise Networks** を使用して Cisco Catalyst Center のトポロジーデータを ITSI にインポートすることで、デバイスのヘルスをサイトレベルに集約する**ロケーション対応のサービスモデル**を作成します。50個の個別のデバイスアラートを監視する代わりに、サイトごとに1つのサービスヘルススコアが表示されるため、チームは「*現在どのサイトで問題が発生しているか？*」という質問に即座に回答を得ることができます。

## Content Pack が重要な理由

**Content Pack for Cisco Enterprise Networks**（**Splunk App for Content Packs** を通じて利用可能）が、ここでの重要なイネーブラーです。サービスや KPI を一から手動で構築する代わりに、このコンテンツパックは **Cisco Catalyst Add-on for Splunk** によって既に収集されているトポロジーデータを使用して、Catalyst Center のサイトを ITSI サービスとして自動的に検出・インポートします。各サイトがサービスとなり、各サービスにはそのサイト内のすべてのネットワークレイヤーのヘルスを反映する事前構築済みの KPI セットが付与されます。

インポートワークフローは、Cisco Catalyst Center のサイト階層を読み取り、サイトごとに1つの ITSI サービスを作成します。その後、ITSI がエンティティディスカバリーサーチを実行し、適切なデバイス（エンティティ）を各サービスに自動的に関連付けます。手動でのマッピングは不要です！

![Import Catalyst Center Services](../images/review-services.png?width=40vw)

## Catalyst Center Site サービステンプレート

この統合の中核となるのが、**Catalyst Center Site** サービステンプレートです。サービスがインポートされると、このテンプレートが各サイトに適用され、そのロケーションにおけるネットワークスタックの各レイヤーを追跡する6つのすぐに使える KPI が提供されます

<div style="max-width: 60%; margin: 0 auto;">

| KPI | 測定対象 |
|---|---|
| **Access Layer** | Access Layer デバイスの平均 HealthScore |
| **Access Points** | Access Point デバイスの平均 HealthScore |
| **Core Layer** | Core Layer デバイスの平均 HealthScore |
| **Distribution Layer** | Distribution Layer デバイスの平均 HealthScore |
| **Router Health** | ルーターの平均 HealthScore |
| **Wireless Controller Health** | Wireless Controller の平均 HealthScore |

</div>

これらの KPI は、Cisco Catalyst Center HealthScore から直接取得されます。HealthScore は、Catalyst Center がオンボーディング、接続性、無線周波数のヘルスに基づいて各デバイスに割り当てる1〜10のスコアです。これらのスコアをネットワークレイヤーごとに平均化することで、ITSI はサイト全体のヘルスを低下させている*スタックの正確な部分*を特定できます。その結果、「Site X のパフォーマンスが低下している」から「Site X の Access Layer が問題である」への特定が数秒で行えるようになります。

## このセクションで行うこと

このセクションを完了すると、以下が達成されます

- **Content Pack for Cisco Enterprise Networks** をインストールし、Catalyst Center のサイトを ITSI サービスとしてインポート
- Catalyst Center Site の KPI が実際のネットワークヘルスデータで正しく値が入力されていることを検証

</div>
