---
title: Catalyst Center サービスを ITSI にインポートする
linkTitle: 2. Catalyst Center サービスを ITSI にインポートする
weight: 2
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

## デバイスヘルスからロケーションベースのネットワーク可視化へ

従来のネットワーク監視ツールは、個々のデバイスについて報告します（ルーターが稼働しているか停止しているか、スイッチに到達可能かどうか）。このレベルの可視性では、*何が*障害を起こしたかはわかりますが、*どこで影響が出ているか*や*ビジネスにどの程度の影響があるか*はわかりません。ブランチオフィスのディストリビューションスイッチが劣化し始めた場合、運用チームがサイト全体に影響が出ていることを把握するために、複数のツールにまたがるアラートを手動で相関させる必要があってはなりません。

このセクションでは、そのギャップに対処します。**Content Pack for Cisco Enterprise Networks** を使用して Cisco Catalyst Center のトポロジデータを ITSI にインポートすることで、デバイスのヘルスをサイトレベルに集約する**ロケーション対応サービスモデル**を作成します。50 個の個別デバイスアラートを監視する代わりに、サイトごとに単一のサービスヘルススコアが表示され、チームは「*今どのサイトに問題が発生しているか？*」という質問に即座に回答を得ることができます。

## Content Pack が重要な理由

**Content Pack for Cisco Enterprise Networks**（**Splunk App for Content Packs** から入手可能）がここでの主要なイネーブラーです。サービスや KPI をゼロから手動で構築するのではなく、Content Pack は **Cisco Catalyst Add-on for Splunk** によって既に収集されているトポロジデータを使用して、Catalyst Center のサイトを ITSI サービスとして自動的に検出しインポートします。各サイトがサービスになり、各サービスにはそのサイト内のすべてのネットワークレイヤーのヘルスを反映する事前構築済みの KPI セットが付与されます。

インポートワークフローは Cisco Catalyst Center のサイト階層を読み取り、サイトごとに 1 つの ITSI サービスを作成します。その後、ITSI がエンティティディスカバリーサーチを実行し、適切なデバイス（エンティティ）を各サービスに自動的に関連付けます。手動マッピングは不要です！

![Import Catalyst Center Services](../images/review-services.png?width=40vw)

## Catalyst Center Site サービステンプレート

この統合の中核にあるのが **Catalyst Center Site** サービステンプレートです。サービスがインポートされると、このテンプレートが各サイトに適用され、そのロケーションのネットワークスタックの異なるレイヤーをそれぞれ追跡する 6 つのすぐに使える KPI が提供されます

| KPI | 測定内容 |
|---|---|
| **Access Layer** | Access Layer デバイスの平均 HealthScore |
| **Access Points** | Access Point デバイスの平均 HealthScore |
| **Core Layer** | Core Layer デバイスの平均 HealthScore |
| **Distribution Layer** | Distribution Layer デバイスの平均 HealthScore |
| **Router Health** | Router の平均 HealthScore |
| **Wireless Controller Health** | Wireless Controller の平均 HealthScore |

これらの KPI は Cisco Catalyst Center HealthScore から直接取得されます。HealthScore は、オンボーディング、接続性、および無線周波数のヘルスに基づいて Catalyst Center が各デバイスに割り当てる 1〜10 のスコアです。これらのスコアをネットワークレイヤーごとに平均化することで、ITSI はサイトの全体的なヘルスを低下させている*スタックのどの部分*かを正確に特定できます。その結果、「サイト X が劣化している」から「サイト X の Access Layer に問題がある」への判断が数秒で行えるようになります。

## このセクションで行うこと

このセクションを完了すると、以下のことが達成されます

- **Content Pack for Cisco Enterprise Networks** をインストールし、Catalyst Center のサイトを ITSI サービスとしてインポートする
- Catalyst Center Site の KPI が実際のネットワークヘルスデータで正しく表示されていることを検証する
