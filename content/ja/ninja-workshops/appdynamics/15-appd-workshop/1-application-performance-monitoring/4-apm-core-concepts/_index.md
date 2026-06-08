---
title: 4. AppDynamics コアコンセプト
weight: 4
description: このセクションでは、Splunk AppDynamics APM 機能のコアコンセプトについて学びます
---

このセクションでは、Splunk AppDynamics APM 機能のコアコンセプトについて学びます。セクションの終わりまでに、以下のコンセプトを理解できるようになります

- Application Flow Maps
- Business Transactions (BTs)
- Snapshots
- Call Graphs

## Flow Maps

AppDynamics アプリエージェントは、最も一般的なアプリケーションフレームワークとサービスを自動的に検出します。組み込みのアプリケーション検出機能と構成設定を使用して、エージェントはアプリケーションデータとメトリクスを収集し、Flow Maps を構築します。

AppDynamics はすべてのトランザクションを自動的にキャプチャしてスコアリングします。Flow Maps は、選択した時間枠のコンテキストに沿って、監視対象アプリケーション環境のコンポーネントとアクティビティを動的に視覚的に表現します。

Flow Map のさまざまな機能を確認してみましょう。

1. さまざまなレイアウトオプションを試してみてください（Flow Map 上の各アイコンをクリックしてドラッグし、位置を変更することもできます）。
2. スライダーとマウスのスクロールホイールを使用して、ズームレベルを調整してみてください。
3. Transaction Scorecard を確認してください。
4. Flow Map の編集オプションを探索してください。

Flow Maps の詳細については、[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-applications/flow-maps/flow-map-overview)をご覧ください。

![Flow Map Components](images/FlowMapComponents.png)  

## Business Transactions  

AppDynamics モデルでは、Business Transaction はリクエスト（多くの場合ユーザーリクエスト）のデータ処理フローを表します。実際の環境では、以下のようなリクエストを処理するために、アプリケーション内の多くの異なるコンポーネントが連携してサービスを提供する場合があります

- EC アプリケーションでは、ユーザーのログイン、商品の検索、カートへの商品の追加。
- コンテンツポータルでは、スポーツ、ビジネス、エンタメニュースなどのコンテンツをユーザーがリクエスト。
- 株式取引アプリケーションでは、株価の取得、株式の売買などのオペレーション。

AppDynamics は Business Transactions を中心にパフォーマンス監視を行うため、ユーザーの視点からアプリケーションコンポーネントのパフォーマンスに焦点を当てることができます。コンポーネントがすぐに利用可能かどうか、またはパフォーマンスの問題が発生しているかどうかを素早く特定できます。たとえば、ユーザーがログイン、チェックアウト、またはデータの表示が可能かどうかを確認できます。ユーザーのレスポンスタイムや、問題が発生した際の原因を確認できます。

Business Transactions の詳細については、[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/overview-of-application-monitoring/business-transactions)および[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions)をご覧ください。

## Business Transactions の確認

以下の手順に従って、Business Transactions が自動的に検出されていることを確認します。

1. 左メニューの **Business Transactions** オプションをクリックします。
2. Business Transactions のリストとそのパフォーマンスを確認します。

![Business Transactions](images/business-transactions.png)  
  
## Snapshots

AppDynamics は、計装された環境内の Business Transaction のすべての実行を監視し、メトリクスはすべての実行を反映します。ただし、トラブルシューティングの目的で、AppDynamics は問題が発生しているトランザクションの特定のインスタンスのスナップショット（詳細な診断情報を含む）を取得します。

以下の手順に従って、トランザクションスナップショットが自動的に収集されていることを確認します。

1. 左メニューの **Application Dashboard** オプションをクリックします。
2. **Transaction Snapshots** タブをクリックします。
3. **Exe Time (ms)** カラムをクリックして、実行時間が最も長いスナップショットでソートします。
4. Business Transaction スナップショットをダブルクリックして、スナップショットビューアーを表示します。
  
![Snapshots](images/snapshots.png)  

トランザクションスナップショットは、トランザクションの単一の呼び出しに対するクロスティアの処理フローを表示します。

**Potential Issues** パネルは、低速なメソッドやリモートサービス呼び出しを強調表示し、パフォーマンス問題の根本原因を調査するのに役立ちます。

## Drill Downs & Call Graphs

Call Graphs と Drill Downs は、ティア上でのトランザクション実行における最も遅いメソッド、エラー、リモートサービス呼び出しなどの重要な情報を提供します。Drill Down には、部分的または完全な Call Graph が含まれる場合があります。Call Graphs は、特定のティア上での Business Transaction の処理のコードレベルのビューを反映します。
  
Business Transaction スナップショットの Flow Map で、Drill Down リンクのあるティアは、AppDynamics がそのティアの Call Graph を取得したことを示します。
  
以下の手順に従って、トランザクションスナップショットの Call Graph にドリルダウンします。
  
1. 左側の Potential Issues リストで低速な呼び出しをクリックします。
2. Drill Down into Call Graph をクリックします。

![Snapshot Drill Down](images/SnapShotDrillDown.png)  
  
Call Graph ビューには以下の詳細が表示されます。

1. メソッド実行シーケンスは、このノード上で Business Transaction の処理に参加したクラスとメソッドの名前を、制御フローが進行した順序で表示します。
2. 各メソッドについて、処理に費やされた時間とパーセンテージ、およびソースコードの行番号を確認できるため、トランザクションのパフォーマンスに影響を与えている可能性のあるコード内の場所を特定できます。
3. Call Graph は、データベースクエリや Web サービス呼び出しなど、他のコンポーネントへのアウトバウンド呼び出しを行うメソッドの Exit Call リンクを表示します。

Transaction Snapshots の詳細については、[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/troubleshoot-business-transaction-performance-with-transaction-snapshots)をご覧ください。

Call Graphs の詳細については、[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/troubleshoot-business-transaction-performance-with-transaction-snapshots/call-graphs)をご覧ください。
  
![Call Graph](images/call-graph.png)  
