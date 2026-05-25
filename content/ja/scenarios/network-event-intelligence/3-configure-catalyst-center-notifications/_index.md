---
title: Catalyst Center 通知の設定
linkTitle: 3. Catalyst Center 通知の設定
weight: 3
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

## Catalyst Center アラートを ITSI に取り込む

Catalyst Center のサービスと KPI が ITSI で稼働している状態で、次のステップはインバウンド通知を設定し、Catalyst Center が生成した Issue と Event を ITSI エピソードに直接取り込むことです。これにより、ロケーションベースの監視を実用的なものにするフィードバックループが構築されます。サイトの KPI ヘルススコアが低下すると、Catalyst Center が Issue を発行し、その Issue は影響を受けたサイトサービスに紐づくノータブルイベントとして ITSI に表示されます。

**Cisco Catalyst Add-on for Splunk** がデータの取り込みを処理しますが、アラートの正規化には ITSI 内でインバウンド通知接続を設定する必要があります。Content Pack for Cisco Enterprise Networks には、Catalyst Center 用の構築済みアラートデータ統合テンプレートが含まれており、関連フィールドが自動的にマッピングされるため、セットアップは簡単です。

**注:** このセクションでは、ITSI で Catalyst Center インバウンド通知接続のカスタムバージョンを設定し、Catalyst Center からの Issue が Episode Review ページに正規化されたノータブルイベントとして表示されるようにします。

![Catalyst Center Notification Configuration](../images/cat-center-notification-config-1.png?width=60vw)

## このセクションで行うこと

このセクションを完了すると、以下が達成されます

- ITSI で **Cisco Catalyst Center** アラート用のカスタムインバウンド通知接続を設定
- イベントを正しいサイトサービスに関連付けるために必要なアラートフィールドをマッピング
