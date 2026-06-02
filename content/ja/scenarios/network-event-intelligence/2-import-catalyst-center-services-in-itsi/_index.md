---
title: Catalyst Center サービスを ITSI にインポートする
linkTitle: 2. Catalyst Center サービスを ITSI にインポートする
weight: 2
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

## デバイスヘルスからロケーションベースのネットワーク可視性へ

従来のネットワーク監視ツールは、個々のデバイスについて報告します（ルーターが稼働しているか停止しているか、スイッチに到達可能かどうかなど）。このレベルの可視性では、*何が*障害を起こしたかはわかりますが、*どこで影響が出ているか*や*ビジネスにとってどの程度深刻か*はわかりません。ブランチオフィスのディストリビューションスイッチが劣化し始めた場合、運用チームはサイト全体が影響を受けていることを把握するために、ツール間でアラートを手動で相関付ける必要があってはなりません。

このセクションでは、そのギャップに対処します。**Content Pack for Cisco Enterprise Networks** を使用して Cisco Catalyst Center のトポロジーデータを ITSI にインポートすることで、デバイスのヘルスをサイトレベルまで集約する**ロケーション対応サービスモデル**を作成します。50 個の個別デバイスアラートを監視する代わりに、サイトごとに単一のサービスヘルススコアが表示され、チームは「*現在どのサイトに問題が発生しているか？*」という質問に即座に答えることができます。

## Content Pack が重要な理由

**Content Pack for Cisco Enterprise Networks**（**Splunk App for Content Packs** から入手可能）は、ここでの重要なイネーブラーです。サービスと KPI を一から手動で構築するのではなく、Content Pack は **Cisco Catalyst Add-on for Splunk** によって既に収集されているトポロジーデータを使用して、Catalyst Center サイトを ITSI サービスとして自動的に検出してインポートします。各サイトがサービスとなり、各サービスにはそのサイト内のすべてのネットワークレイヤーのヘルスを反映する事前構築済み KPI のセットが設定されます。

インポートワークフローは Cisco Catalyst Center のサイト階層を読み取り、サイトごとに 1 つの ITSI サービスを作成します。その後、ITSI はエンティティディスカバリーサーチを実行して、適切なデバイス（エンティティ）を各サービスに自動的に関連付けます。手動マッピングは不要です！

![Import Catalyst Center Services](../images/review-services.png?width=40vw)

## Catalyst Center Site サービステンプレート

この統合の中心にあるのが **Catalyst Center Site** サービステンプレートです。サービスがインポートされると、このテンプレートが各サイトに適用され、そのロケーションにおけるネットワークスタックの異なるレイヤーをそれぞれ追跡する 6 つのすぐに使える KPI が提供されます

| KPI | 測定内容 |
|---|---|
| **Access Layer** | Access Layer デバイスの平均 HealthScore |
| **Access Points** | Access Point デバイスの平均 HealthScore |
| **Core Layer** | Core Layer デバイスの平均 HealthScore |
| **Distribution Layer** | Distribution Layer デバイスの平均 HealthScore |
| **Router Health** | ルーターの平均 HealthScore |
| **Wireless Controller Health** | Wireless Controller の平均 HealthScore |

これらの KPI は Cisco Catalyst Center HealthScore から直接取得されます。これは、Catalyst Center がオンボーディング、接続性、および無線周波数のヘルスに基づいて各デバイスに割り当てる 1〜10 のスコアです。ネットワークレイヤーごとにこれらのスコアを平均化することで、ITSI はサイト全体のヘルスを低下させている*スタックのどの部分が原因か*を正確に特定できます。その結果、「サイト X が劣化している」から「サイト X の Access Layer が問題である」への特定が数秒で行えるようになります。

## このセクションで行うこと

このセクションを完了すると、以下が達成されます

- **Content Pack for Cisco Enterprise Networks** をインストールし、Catalyst Center サイトを ITSI サービスとしてインポートしたこと
- Catalyst Center Site KPI が実際のネットワークヘルスデータで正しく入力されていることを検証したこと
