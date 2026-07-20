---
title: 7. エラーと例外のトラブルシューティング
weight: 7
description: このセクションでは、アプリケーション内のエラーをトラブルシューティングする方法を学びます
---

この演習では、アプリケーション内のエラーを効果的に検出・診断し、根本原因を特定する方法を学びます。さらに、パフォーマンスが低下しているノードやエラーが発生しているノードを特定し、トラブルシューティング手法を適用してパフォーマンスの問題を解決する方法を学びます。このハンズオン体験により、アプリケーションの健全性を維持し、最適なパフォーマンスを確保する能力が向上します。

## アプリケーション内の特定のエラーを見つける

AppDynamicsを使用すると、アプリケーション内のエラーや例外を簡単に見つけることができます。 **Errors** ダッシュボードを使用して、エラーのあるトランザクションスナップショットを確認し、最も頻繁に発生している例外を特定できます。エラーを素早く特定することで、アプリケーションの安定性とユーザー体験を向上させる修正の優先順位付けに役立ちます。例外の種類と頻度を理解することで、最も影響の大きい問題に集中できます。

1. 左メニューの **Troubleshoot** オプションをクリックします。
2. 左メニューの **Errors** オプションをクリックします。エラーのあるビジネストランザクションを素早く特定できるErrorsダッシュボードに移動します。
3. いくつかのエラートランザクションスナップショットを確認します。スナップショットを確認することで、エラーが発生した際の正確なコンテキストとフローを確認できます。
4. **Exceptions** タブをクリックして、タイプ別にグループ化された例外を表示します。例外タイプ別のグループ化により、繰り返し発生する問題やパターンを特定できます。

    ![Errors Dashboard](images/errors-dashboard.png)

    **Exceptions** タブには、アプリケーション内で最も多く発生している例外のタイプが表示されるため、最も影響の大きいものから優先的に修正できます。

5. **Exceptions per minute** と **Exception count**（6）を確認して、エラーの頻度を把握します。高頻度の例外は、即座に対応が必要な重大な問題を示していることが多いです。
6. 例外が発生している **Tier** を確認して、アプリケーションアーキテクチャ内での問題の場所を特定します。影響を受けているTierを把握することで、根本原因の絞り込みに役立ちます。
7. MySQLIntegrityConstraintViolationExceptionタイプをダブルクリックして、詳細を確認します。

    ![Exception Dashboard](images/exception-dashboard.png)
  
8. この例外タイプが発生したスナップショットを示す概要ダッシュボードを確認します。
9. **Stack Traces for this Exception** というラベルのタブには、この例外タイプによって生成された一意のスタックトレースの集約リストが表示されます。スタックトレースはエラーを引き起こしている正確なコードパスを示し、デバッグに不可欠です。
10. スナップショットをダブルクリックして開き、コンテキスト内でエラーを確認します。
これにより、トランザクションフローが表示され、エラーが発生した場所が特定されます。

    ![MySQL Exception](images/MySQL-exception.png)  

    例外画面からエラースナップショットを開くと、エラーが発生したスナップショット内の特定のセグメントが表示されます。

11. 赤いテキストで表示されたexit callに注目します。これはエラーまたは例外を示しています。
12. exit callをドリルダウンして、詳細なエラー情報を表示します。
13. **Error Details** をクリックして、完全なスタックトレースを表示します。完全なスタックトレースは、開発者がバグを追跡して修正するために重要です。

{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}
エラー処理と例外について詳しく知りたい場合は、AppDynamicsの公式ドキュメントを参照してください: [こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/troubleshooting-applications/errors-and-exceptions)
{{% /notice %}}

![Call Graph Error](images/callgraph-error.png)  

## ノードの問題のトラブルシューティング

ノードの健全性はアプリケーションのパフォーマンスと可用性に直接影響します。ノードの問題を早期に検出することで、障害を防ぎ、スムーズな運用を確保できます。AppDynamicsはUI全体にビジュアルインジケーターを提供し、問題を素早く特定できるようにしています。

Application Dashboardの3つの領域でノードの問題のインジケーターを確認できます。

1. **Application Dashboard** でノードの問題を示すビジュアルインジケーターを確認します。色の変化やアイコンにより、問題を即座に把握できます。
2. **Events** パネルには、Node Healthに関連するものを含む正常性ルール違反が表示されます。
3. **Node Health** パネルには、ノードで発生しているクリティカルまたは警告の問題数が表示されます。 **Node Health** パネルのNode Healthリンクをクリックして、 **Tiers & Nodes dashboard** にドリルダウンします。

    ![Application Dashboard](images/application-dashboard.png)  

4. または、左メニューの **Tiers & Nodes** をクリックして **Tiers & Nodes dashboard** に移動することもできます。
5. Grid Viewに切り替えて、ノードの整理されたリストを表示します。Grid Viewを使用すると、警告のあるノードをスキャンして見つけやすくなります。
6. Insurance-Services_Node-01ノードの警告アイコンをクリックします。

    ![Tiers and Nodes List](images/tiers-nodes-list.png)  

7. 正常性ルール違反の概要を確認し、違反の説明をクリックします。
8. **Details** ボタンをクリックして詳細を表示します。

    ![Health Rule Violation](images/health-rule-violations.png)  

    **Health Rule Violation** 詳細ビューアーには以下が表示されます。

9. 違反の現在の状態。
10. 違反が発生していた時間のタイムライン。
11. 違反の詳細とトリガーとなった条件。
12. **View Dashboard During Health Rule Violation** をクリックして、問題発生時のノードメトリクスを確認します。違反とパフォーマンスメトリクスの相関により、診断が容易になります。

    ![Health Rule Violation Details](images/health-rule-violation-details.png)

    **View Dashboard During Health Rule Violation** ボタンをクリックすると、デフォルトでNodeダッシュボードの **Server** タブが開きます。

    AppDynamics Server Visibility Monitoringエージェントをまだインストールしていない場合、ノードのホストのリソースメトリクスは表示されません。これらのメトリクスは次のラボで確認できます。AppDynamics JavaエージェントはJMXを介してJVMからメモリメトリクスを収集します。

    以下の手順でJVMヒープデータを調査します。

13. **Memory** タブをクリックします。
14. 現在のヒープ使用率を確認します。
15. 発生しているMajor Garbage Collectionに注目します。

注意: Memory画面の表示に問題がある場合は、別のブラウザを使用してみてください（FirefoxはWindows、Linux、Macで正しくレンダリングされます）。

    ![Memory Dashboard](images/memory-dashboard.png)  

16. 外側のスクロールバーを使用して、画面の一番下までスクロールします。
17. **PS Old Gen** のメモリ使用量が高いことに注目します。これはメモリリークや非効率なガベージコレクションの潜在的な兆候です。メモリ圧迫を早期に特定することで、障害を防ぐことができます。

ノードとJVMのモニタリングについて詳しくは[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/tiers-and-nodes/troubleshoot-node-problems)と[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/tiers-and-nodes/monitor-jvms)を参照してください。

![PS Old Gen](images/ps-old-gen.png)

## まとめ

このラボでは、AppDynamicsを使用してアプリケーションのエラーとノードの健全性の問題を特定し、トラブルシューティングする方法を学びました。まず、Errorsダッシュボードを使用して特定のエラーと例外を見つけ、その頻度、タイプ、アプリケーションへの影響を理解しました。エラースナップショットとスタックトレースにドリルダウンして、障害の根本原因を特定しました。

次に、Application Dashboardのビジュアルインジケーターを解釈し、正常性ルール違反を調査することで、ノードの健全性モニタリングについて学びました。JVMメモリメトリクスを分析して、ガベージコレクションとヒープ使用量に関連する潜在的なパフォーマンスボトルネックを検出する方法を学びました。

これらのスキルを組み合わせることで、アプリケーションのパフォーマンスと信頼性を維持するためのプロアクティブなモニタリングと迅速なトラブルシューティングが可能になります。
