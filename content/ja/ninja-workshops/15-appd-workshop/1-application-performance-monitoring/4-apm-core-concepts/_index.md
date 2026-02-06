---
title: 4. AppDynamics の基本概念
weight: 4
description: このセクションでは、Splunk AppDynamics APM 機能の基本概念について学びます
---

このセクションでは、Splunk AppDynamics APM 機能の基本概念について学びます。このセクションを終了すると、以下の概念を理解できるようになります：

- Application Flow Maps
- Business Transactions (BTs)
- Snapshots
- Call Graphs

## Flow Maps

AppDynamics アプリエージェントは、最も一般的なアプリケーションフレームワークとサービスを自動的に検出します。組み込みのアプリケーション検出および設定を使用して、エージェントはアプリケーションデータとメトリクスを収集し、Flow Maps を構築します。

AppDynamics はすべてのトランザクションを自動的にキャプチャしてスコアリングします。Flow Maps は、選択した時間枠のコンテキストで、監視対象のアプリケーション環境のコンポーネントとアクティビティを動的に視覚化して表示します。

Flow Map のさまざまな機能に慣れてください。

1. さまざまなレイアウトオプションを試してみてください（Flow Map 上の各アイコンをクリックしてドラッグして位置を変更することもできます）。
2. スライダーとマウスのスクロールホイールを使用してズームレベルを調整してみてください。
3. Transaction Scorecard を確認してください。
4. Flow Map を編集するオプションを探索してください。

Flow Maps の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-applications/flow-maps/flow-map-overview)をご覧ください。

![Flow Map Components](images/FlowMapComponents.png)  

## Business Transactions

AppDynamics モデルでは、Business Transaction はリクエスト（通常はユーザーリクエスト）のデータ処理フローを表します。現実世界では、アプリケーション内の多くの異なるコンポーネントが相互作用して、以下のようなタイプのリクエストを処理するサービスを提供します：

- e コマースアプリケーションでは、ユーザーのログイン、商品の検索、カートへの商品追加
- コンテンツポータルでは、スポーツ、ビジネス、エンターテインメントニュースなどのコンテンツのリクエスト
- 株式取引アプリケーションでは、株価の取得、株式の売買などの操作

AppDynamics は Business Transactions を中心にパフォーマンス監視を行うため、ユーザーの視点からアプリケーションコンポーネントのパフォーマンスに集中できます。コンポーネントがすぐに利用可能かどうか、またはパフォーマンスの問題が発生しているかどうかをすばやく特定できます。たとえば、ユーザーがログインできるか、チェックアウトできるか、データを表示できるかを確認できます。ユーザーの応答時間と、問題が発生した場合の原因を確認できます。

Business Transactions の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/overview-of-application-monitoring/business-transactions)と[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions)をご覧ください。

## Business Transactions の確認

以下の手順に従って、Business Transactions が自動的に検出されていることを確認します。

1. 左側のメニューで **Business Transactions** オプションをクリックします。
2. Business Transactions のリストとそのパフォーマンスを確認します。

![Business Transactions](images/business-transactions.png)  
  
## Snapshots

AppDynamics は、計装された環境内のすべての Business Transaction の実行を監視し、メトリクスはそれらすべての実行を反映します。ただし、トラブルシューティングの目的で、AppDynamics は問題が発生しているトランザクションの特定のインスタンスのスナップショット（詳細な診断情報を含む）を取得します。

以下の手順に従って、トランザクションスナップショットが自動的に収集されていることを確認します。

1. 左側のメニューで **Application Dashboard** オプションをクリックします。
2. **Transaction Snapshots** タブをクリックします。
3. **Exe Time (ms)** 列をクリックして、実行時間が最も長いスナップショットでソートします。
4. Business Transaction スナップショットをダブルクリックしてスナップショットビューアを表示します

![Snapshots](images/snapshots.png)

トランザクションスナップショットは、単一のトランザクション呼び出しの処理フローをクロスティアビューで表示します。

**Potential Issues** パネルは、遅いメソッドと遅いリモートサービスコールを強調表示し、パフォーマンス問題の根本原因を調査するのに役立ちます。  

## Drill Downs と Call Graphs

Call graphs と drill downs は、Tier でのトランザクション実行に関する重要な情報を提供します。これには、最も遅いメソッド、エラー、リモートサービスコールが含まれます。drill down には、部分的または完全な call graph が含まれる場合があります。Call graphs は、特定の Tier での Business Transaction の処理をコードレベルで表示します。

Business Transaction スナップショットの Flow Map で、Drill Down リンクがある Tier は、AppDynamics がその Tier の call graph を取得したことを示しています。

以下の手順に従って、トランザクションスナップショットの call graph にドリルダウンします。

1. 左側の Potential Issues リストで遅いコールをクリックします。
2. **Drill Down into Call Graph** をクリックします。

![Snapshot Drill Down](images/SnapShotDrillDown.png)

call graph ビューには、以下の詳細が表示されます。

1. メソッド実行シーケンスは、このノードで Business Transaction の処理に参加したクラスとメソッドの名前を、制御フローの進行順序で表示します。
2. 各メソッドについて、処理に費やされた時間と割合、およびソースコード内の行番号を確認でき、トランザクションのパフォーマンスに影響を与えている可能性のあるコード内の場所を特定できます。
3. call graph は、データベースクエリや Web サービスコールなど、他のコンポーネントへの発信コールを行うメソッドの exit call リンクを表示します。

Transaction Snapshots の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/troubleshoot-business-transaction-performance-with-transaction-snapshots)をご覧ください。

Call Graphs の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/troubleshoot-business-transaction-performance-with-transaction-snapshots/call-graphs)をご覧ください。

![Call Graph](images/call-graph.png)  
