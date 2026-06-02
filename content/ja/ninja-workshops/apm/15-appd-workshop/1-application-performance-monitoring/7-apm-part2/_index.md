---
title: 7. エラーと例外のトラブルシューティング
weight: 7
description: このセクションでは、アプリケーション内のエラーをトラブルシューティングする方法を学びます
---

この演習では、アプリケーション内のエラーを効果的に検出・診断し、根本原因を特定する方法を学びます。さらに、パフォーマンスが低下していたりエラーが発生していたりする特定のノードを特定する方法を学び、これらのパフォーマンス問題を解決するためのトラブルシューティング手法を適用します。このハンズオンの経験により、アプリケーションの健全性を維持し、最適なパフォーマンスを確保する能力が向上します。

## アプリケーション内の特定のエラーを見つける

AppDynamics を使用すると、アプリケーション内のエラーや例外を簡単に見つけることができます。**Errors** ダッシュボードを使用して、エラーを伴うトランザクションのスナップショットを確認したり、最も頻繁に発生している例外を見つけたりすることができます。エラーを迅速に特定することで、アプリケーションの安定性とユーザー体験を向上させる修正の優先順位付けが容易になります。例外の種類と頻度を理解することで、最も影響の大きい問題に集中することができます。

1. 左メニューの **Troubleshoot** オプションをクリックします。
2. 左メニューの **Errors** オプションをクリックします。これにより、エラーを伴うビジネストランザクションを迅速に特定できる Errors ダッシュボードに移動します。
3. いくつかのエラートランザクションスナップショットを確認します。スナップショットを確認することで、エラーが発生したときの正確なコンテキストとフローを把握できます。
4. **Exceptions** タブをクリックして、タイプ別にグループ化された例外を確認します。例外タイプ別にグループ化することで、繰り返し発生する問題やパターンを特定しやすくなります。

    ![Errors Dashboard](images/errors-dashboard.png)

    **Exceptions** タブには、アプリケーション内で最も多く発生している例外のタイプが表示されるため、最も影響の大きいものから優先的に修正することができます。

5. **Exceptions per minute** と **Exception count** (6) を観察し、エラーの頻度を把握します。頻度の高い例外は、即座に対応が必要な重大な問題を示していることがよくあります。
6. 例外が発生している **Tier** に注目して、アプリケーションアーキテクチャ内での問題箇所を特定します。影響を受けている tier を知ることで、根本原因の絞り込みに役立ちます。
7. MySQLIntegrityConstraintViolationException タイプをダブルクリックして、さらに詳しく調べます。

    ![Exception Dashboard](images/exception-dashboard.png)

8. この例外タイプが発生したスナップショットを表示する概要ダッシュボードを確認します。
9. **Stack Traces for this Exception** というラベルのタブには、この例外タイプによって生成された一意のスタックトレースの集計リストが表示されます。スタックトレースは、エラーを引き起こしている正確なコードパスを示しており、デバッグに不可欠です。
10. スナップショットをダブルクリックして開き、コンテキスト内でエラーを確認します。
これにより、トランザクションフローが表示され、エラーが発生した場所が特定されます。

    ![MySQL Exception](images/MySQL-exception.png)

    例外画面からエラースナップショットを開くと、スナップショット内のエラーが発生した特定のセグメントが開きます。

11. エラーや例外を示す赤いテキストの exit call に注目します。
12. exit call をドリルダウンして、詳細なエラー情報を表示します。
13. **Error Details** をクリックして、完全なスタックトレースを表示します。完全なスタックトレースは、開発者がバグを追跡して修正するために重要です。

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
エラー処理と例外について詳しく学びたい場合は、次のリンクから AppDynamics の公式ドキュメントを参照してください: [here](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/troubleshooting-applications/errors-and-exceptions)。
{{% /notice %}}

![Call Graph Error](images/callgraph-error.png)

## ノードの問題のトラブルシューティング

ノードの健全性は、アプリケーションのパフォーマンスと可用性に直接影響します。ノードの問題を早期に検出することで、障害を防ぎ、スムーズな運用を確保できます。AppDynamics は UI 全体に視覚的なインジケーターを提供しており、問題を迅速に特定することが容易になります。

ノードの問題のインジケーターは、Application Dashboard の 3 つの領域で確認できます。

1. **Application Dashboard** を観察して、ノードの問題の視覚的なインジケーターを確認します。色の変化やアイコンによって、問題が即座に通知されます。
2. **Events** パネルには、Node Health に関連するものを含む Health Rule Violations が表示されます。
3. **Node Health** パネルには、ノードで発生している critical または warning の問題の数が表示されます。**Node Health** パネルの Node Health リンクをクリックして、**Tiers & Nodes dashboard** にドリルダウンします。

    ![Application Dashboard](images/application-dashboard.png)

4. または、左メニューの **Tiers & Nodes** をクリックして、**Tiers & Nodes dashboard** にアクセスすることもできます。
5. Grid View に切り替えて、整理されたノードのリストを表示します。Grid view を使用すると、警告のあるノードのスキャンと検索が容易になります。
6. Insurance-Services_Node-01 ノードの警告アイコンをクリックします。

    ![Tiers and Nodes List](images/tiers-nodes-list.png)

7. Health Rule Violations の概要を確認し、違反の説明をクリックします。
8. **Details** ボタンをクリックして、詳細を表示します。

    ![Health Rule Violation](images/health-rule-violations.png)

    **Health Rule Violation** の詳細ビューアには、次の情報が表示されます。

9. 違反の現在の状態。
10. 違反が発生していた時間のタイムライン。
11. 違反の具体的な内容と、それをトリガーした条件。
12. **View Dashboard During Health Rule Violation** をクリックして、問題発生時のノードのメトリクスを確認します。違反とパフォーマンスメトリクスを関連付けることで、診断に役立ちます。

    ![Health Rule Violation Details](images/health-rule-violation-details.png)

    **View Dashboard During Health Rule Violation** ボタンをクリックすると、デフォルトでノードダッシュボードの **Server** タブが開きます。

    AppDynamics Server Visibility Monitoring agent をまだインストールしていない場合は、ノードのホストのリソースメトリクスは表示されません。これらのメトリクスは次のラボで確認できます。AppDynamics Java agent は、JMX を介して JVM からメモリメトリクスを収集します。

    以下の手順で JVM ヒープデータを調査します。

13. **Memory** タブをクリックします。
14. 現在のヒープ使用率を確認します。
15. 発生している Major Garbage Collections に注目します。

注: Memory 画面の表示に問題がある場合は、別のブラウザを使用してみてください (Firefox は Windows、Linux、Mac で正しくレンダリングされます)。

    ![Memory Dashboard](images/memory-dashboard.png)

16. 外側のスクロールバーを使用して、画面の最下部までスクロールします。
17. **PS Old Gen** メモリ使用量が高い場合は、メモリリークまたは非効率なガベージコレクションの兆候である可能性があるため注意します。メモリ圧迫を早期に特定することで、障害を防ぐことができます。

ノードと JVM のモニタリングについては、[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/tiers-and-nodes/troubleshoot-node-problems) と [こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/tiers-and-nodes/monitor-jvms) で詳しく説明しています。

![PS Old Gen](images/ps-old-gen.png)

## まとめ

このラボでは、AppDynamics を効果的に使用して、アプリケーションのエラーとノードの健全性の問題を特定およびトラブルシューティングする方法を学びました。まず、Errors ダッシュボードを使用して特定のエラーや例外を見つけ、その頻度、タイプ、アプリケーションへの影響を理解しました。エラースナップショットとスタックトレースをドリルダウンして、障害の根本原因を特定しました。

次に、Application Dashboard の視覚的なインジケーターを解釈し、Health Rule Violations を調査することで、ノードの健全性モニタリングを探索しました。JVM メモリメトリクスを分析して、ガベージコレクションとヒープ使用量に関連する潜在的なパフォーマンスのボトルネックを検出する方法を学びました。

これらのスキルを組み合わせることで、プロアクティブなモニタリングと迅速なトラブルシューティングが可能になり、アプリケーションのパフォーマンスと信頼性を維持できます。
