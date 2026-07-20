---
title: 4. AppDynamicsのコアコンセプト
weight: 4
description: このセクションでは、Splunk AppDynamics APM機能のコアコンセプトについて学びます
---

このセクションでは、Splunk AppDynamics APM機能のコアコンセプトについて学びます。セクションの終わりまでに、以下のコンセプトを理解できるようになります。

- Application Flow Maps
- Business Transactions（BTs）
- Snapshots
- Call Graphs

## Flow Maps

AppDynamicsのアプリケーションエージェントは、最も一般的なアプリケーションフレームワークとサービスを自動的に検出します。組み込みのアプリケーション検出機能と設定を使用して、エージェントはアプリケーションデータとメトリクスを収集し、Flow Mapsを構築します。

AppDynamicsはすべてのトランザクションを自動的にキャプチャしてスコアリングします。Flow Mapsは、選択した時間枠のコンテキストに基づいて、監視対象アプリケーション環境のコンポーネントとアクティビティを動的に視覚化します。

Flow Mapのさまざまな機能を確認します。

1. 異なるレイアウトオプションを試します（Flow Map上の各アイコンをクリックしてドラッグし、位置を変更することもできます）。
2. スライダーとマウスのスクロールホイールを使用してズームレベルを調整します。
3. Transaction Scorecardを確認します。
4. Flow Mapの編集オプションを確認します。

Flow Mapsの詳細は[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-applications/flow-maps/flow-map-overview)を参照してください。

![Flow Map Components](images/FlowMapComponents.png)  

## Business Transactions  

AppDynamicsモデルにおいて、Business Transactionはリクエスト（多くの場合ユーザーリクエスト）のデータ処理フローを表します。実際のシナリオでは、アプリケーション内の多くの異なるコンポーネントが連携して、以下のようなリクエストを処理するサービスを提供します。

- ECアプリケーションでは、ユーザーのログイン、アイテムの検索、カートへのアイテムの追加。
- コンテンツポータルでは、スポーツ、ビジネス、エンターテイメントニュースなどのコンテンツのリクエスト。
- 株式取引アプリケーションでは、株価の取得、株式の売買などの操作。

AppDynamicsはBusiness Transactionsを中心にパフォーマンスモニタリングを行うため、ユーザーの視点からアプリケーションコンポーネントのパフォーマンスに注目できます。コンポーネントが正常に利用可能か、パフォーマンスの問題が発生しているかを迅速に特定できます。たとえば、ユーザーがログイン、チェックアウト、データの閲覧を正常に行えているかを確認できます。ユーザーのレスポンスタイムや、問題が発生した際の原因を確認できます。

Business Transactionsの詳細は[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/overview-of-application-monitoring/business-transactions)と[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions)を参照してください。

## Business Transactionsの確認

以下の手順に従って、Business Transactionsが自動的に検出されていることを確認します。

1. 左メニューの **Business Transactions** オプションをクリックします。
2. Business Transactionsのリストとそのパフォーマンスを確認します。

![Business Transactions](images/business-transactions.png)  
  
## Snapshots

AppDynamicsは計装された環境内のBusiness Transactionのすべての実行を監視し、メトリクスはそれらすべての実行を反映します。ただし、トラブルシューティングの目的で、AppDynamicsは問題が発生しているトランザクションの特定のインスタンスのスナップショット（詳細な診断情報を含む）を取得します。

以下の手順に従って、トランザクションスナップショットが自動的に収集されていることを確認します。

1. 左メニューの **Application Dashboard** オプションをクリックします。
2. **Transaction Snapshots** タブをクリックします。
3. **Exe Time (ms)** 列をクリックして、実行時間が最も長いスナップショット順にソートします。
4. Business Transactionスナップショットをダブルクリックしてスナップショットビューアを表示します。
  
![Snapshots](images/snapshots.png)  

トランザクションスナップショットは、トランザクションの単一の呼び出しに対する処理フローのクロスティアビューを提供します。

**Potential Issues** パネルは、遅いメソッドや遅いリモートサービスコールを強調表示し、パフォーマンス問題の根本原因の調査を支援します。

## Drill DownsとCall Graphs

Call GraphsとDrill Downsは、ティア上のトランザクション実行における最も遅いメソッド、エラー、リモートサービスコールなどの重要な情報を提供します。Drill Downには部分的または完全なCall Graphが含まれる場合があります。Call Graphsは、特定のティア上でのBusiness Transactionの処理をコードレベルで表示します。
  
Business TransactionスナップショットのFlow Mapにおいて、Drill Downリンクのあるティアは、AppDynamicsがそのティアのCall Graphを取得したことを示します。
  
以下の手順に従って、トランザクションスナップショットのCall Graphにドリルダウンします。
  
1. 左側のPotential Issuesリストで遅いコールをクリックします。
2. Drill Down into Call Graphをクリックします。

![Snapshot Drill Down](images/SnapShotDrillDown.png)  
  
Call Graphビューには以下の詳細が表示されます。

1. メソッド実行シーケンスは、このノード上でBusiness Transactionの処理に参加したクラスとメソッドの名前を、制御フローが進行した順序で表示します。
2. 各メソッドについて、処理に費やされた時間と割合、およびソースコード内の行番号を確認でき、トランザクションのパフォーマンスに影響を与えている可能性のあるコード内の場所を特定できます。
3. Call Graphは、データベースクエリやWebサービスコールなどの他のコンポーネントへのアウトバウンドコールを行うメソッドのexit callリンクを表示します。

Transaction Snapshotsの詳細は[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/troubleshoot-business-transaction-performance-with-transaction-snapshots)を参照してください。

Call Graphsの詳細は[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/troubleshoot-business-transaction-performance-with-transaction-snapshots/call-graphs)を参照してください。
  
![Call Graph](images/call-graph.png)  
