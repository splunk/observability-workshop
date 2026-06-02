---
title: 4. AppDynamics のコアコンセプト
weight: 4
description: このセクションでは、Splunk AppDynamics APM 機能のコアコンセプトについて学びます
---

このセクションでは、Splunk AppDynamics APM 機能のコアコンセプトについて学びます。このセクションを終える頃には、以下の概念を理解できるようになります。

- Application Flow Maps
- Business Transactions (BTs)
- Snapshots
- Call Graphs

## Flow Maps

AppDynamics アプリエージェントは、最も一般的なアプリケーションフレームワークやサービスを自動的に検出します。組み込みのアプリケーション検出機能と設定を使用して、エージェントはアプリケーションのデータとメトリクスを収集し、Flow Maps を構築します。

AppDynamics はすべてのトランザクションを自動的にキャプチャしてスコアリングします。Flow Maps は、選択した時間枠のコンテキストに沿って、監視対象のアプリケーション環境のコンポーネントとアクティビティを動的にビジュアル表現します。

Flow Map のさまざまな機能について慣れていきましょう。

1. さまざまなレイアウトオプションを試してみてください（Flow Map 上の各アイコンをクリックしてドラッグし、位置を変更することもできます）。
2. スライダーやマウスのスクロールホイールを使ってズームレベルを調整してみましょう。
3. Transaction Scorecard を確認します。
4. Flow Map を編集するためのオプションを確認します。

Flow Maps の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-applications/flow-maps/flow-map-overview)をご覧ください。

![Flow Map Components](images/FlowMapComponents.png)  

## Business Transactions  

AppDynamics のモデルにおいて、Business Transaction はリクエスト（多くの場合ユーザーリクエスト）に対するデータ処理フローを表します。実際のシステムでは、アプリケーションの多くの異なるコンポーネントが連携して、以下のようなリクエストを処理するためのサービスを提供します。

- e コマースアプリケーションでは、ユーザーがログインしたり、商品を検索したり、商品をカートに追加したりする操作。
- コンテンツポータルでは、ユーザーがスポーツ、ビジネス、エンターテインメントなどのニュースコンテンツをリクエストする操作。
- 株式取引アプリケーションでは、株価情報の取得、株式の売買などの操作。  
AppDynamics はパフォーマンス監視を Business Transactions を中心に構成しているため、ユーザー視点でアプリケーションコンポーネントのパフォーマンスにフォーカスできます。コンポーネントが利用可能な状態にあるか、パフォーマンスの問題が発生しているかを素早く特定できます。例えば、ユーザーがログイン、チェックアウト、データ閲覧などの操作を実行できているかを確認できます。ユーザーへのレスポンスタイムや、問題発生時の原因を確認できます。

Business Transactions の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/overview-of-application-monitoring/business-transactions)および[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions)をご覧ください。

## Business Transactions の確認

以下の手順で、Business Transactions が自動的に検出されていることを確認します。

1. 左メニューの **Business Transactions** オプションをクリックします。
2. Business Transactions の一覧とそのパフォーマンスを確認します。

![Business Transactions](images/business-transactions.png)  
  
## Snapshots

AppDynamics は、計装された環境において Business Transaction の実行をすべて監視し、メトリクスはこれらすべての実行を反映します。ただし、トラブルシューティングを目的として、AppDynamics は問題が発生している特定のトランザクションインスタンスについて、深い診断情報を含むスナップショットを取得します。

以下の手順で、トランザクションスナップショットが自動的に収集されていることを確認します。

1. 左メニューの **Application Dashboard** オプションをクリックします。
2. **Transaction Snapshots** タブをクリックします。
3. **Exe Time (ms)** カラムをクリックして、実行時間が最も長いスナップショット順にソートします。
4. Business Transaction のスナップショットをダブルクリックすると、スナップショットビューアーが表示されます。  
  
![Snapshots](images/snapshots.png)  

トランザクションスナップショットは、トランザクションの 1 回の呼び出しについて、ティアをまたいだ処理フローを確認できます。

**Potential Issues** パネルでは、遅いメソッドや遅いリモートサービス呼び出しが強調表示され、パフォーマンス問題の根本原因の調査に役立ちます。  

## Drill Downs と Call Graphs

Call graphs と drill downs は、ティア上でのトランザクション実行に関する重要な情報、例えば最も遅いメソッド、エラー、リモートサービス呼び出しなどを提供します。drill down には、部分的または完全な call graph が含まれる場合があります。Call graphs は、特定のティアにおける Business Transaction の処理をコードレベルで可視化します。
  
Business Transaction スナップショットの Flow Map 上で、Drill Down リンクが付いているティアは、AppDynamics がそのティアで call graph を取得していることを示します。
  
以下の手順で、トランザクションスナップショットの call graph にドリルダウンします。
  
1. 左側の Potential Issues リストで遅い呼び出しをクリックします。
2. Drill Down into Call Graph をクリックします。

![Snapshot Drill Down](images/SnapShotDrillDown.png)  
  
call graph ビューには以下の詳細情報が表示されます。

1. メソッド実行シーケンスは、このノード上で Business Transaction の処理に関わったクラスとメソッドの名前を、制御フローの順序で表示します。
2. 各メソッドについて、処理に費やされた時間と割合、ソースコード内の行番号を確認できるため、トランザクションのパフォーマンスに影響を与えている可能性のあるコード位置を特定できます。
3. call graph には、データベースクエリやウェブサービス呼び出しなど、他のコンポーネントへの外部呼び出しを行うメソッドの exit call リンクが表示されます。

Transaction Snapshots の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/troubleshoot-business-transaction-performance-with-transaction-snapshots)をご覧ください。

Call Graphs の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/troubleshoot-business-transaction-performance-with-transaction-snapshots/call-graphs)をご覧ください。

![Call Graph](images/call-graph.png)  
