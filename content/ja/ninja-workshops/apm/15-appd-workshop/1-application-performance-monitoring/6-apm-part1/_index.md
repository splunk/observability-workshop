---
title: 6. 遅いトランザクションのトラブルシューティング
weight: 6
description: このセクションでは、スナップショットを利用して遅いトランザクションをトラブルシューティングする方法を学びます
---

この演習では、以下のタスクを実行します。

- アプリケーションダッシュボードとフローマップを監視する。
- 遅いトランザクションのスナップショットをトラブルシューティングする。

## アプリケーションダッシュボードとフローマップの監視

これまでの演習では、Application Flow Map の基本的な機能をいくつか確認してきました。ここでは、Application Dashboard と Flow Map を活用して、アプリケーション内の問題を即座に特定する方法をより深く見ていきます。

1. Health Rule Violations、Node Health の問題、および Business Transactions の健全性は、選択した時間枠について常にこのエリアに表示されます。ここで利用できるリンクをクリックすると、詳細にドリルダウンできます。
2. Transaction Scorecard では、normal、slow、very slow、stalled、およびエラーが発生したトランザクションの数と割合が表示されます。スコアカードでは、例外タイプの上位カテゴリも確認できます。ここで利用できるリンクをクリックすると、詳細にドリルダウンできます。
3. 異なるアプリケーションコンポーネントを接続している青い線のいずれかを左クリック（シングルクリック）すると、2 つのコンポーネント間のやり取りの概要が表示されます。
4. Tier の色付きリングの中を左クリック（シングルクリック）すると、Flow Map に留まったまま、その Tier に関する詳細情報が表示されます。
5. ダッシュボード下部にある 3 つのチャート（Load、Response Time、Errors）のいずれかの時系列にカーソルを合わせると、記録されたメトリクスの詳細が表示されます。

    ![Flow Map Components](images/flow-map-components.png)

次に、Dynamic Baselines と、ダッシュボード下部のチャートのオプションについて見ていきます。

1. チャート上のメトリクスを、各メトリクスについて自動的に計算された Dynamic Baseline と比較します。
2. Dynamic Baseline は、以下の画像に示されているように、load チャートと response time チャートに青い点線で表示されます。
3. ダッシュボード下部にある 3 つのチャートのいずれかで見られるスパイクをハイライトするには、左クリックしたままマウスボタンを押し続け、左から右にドラッグします。
4. マウスボタンを離し、ポップアップメニューに表示される 3 つのオプションのいずれかを選択します。

    ![Flow Map Components](images/flowmap_components2.png)

AppDynamics 独自の Dynamic Baselining の精度は時間の経過とともに向上し、アプリケーション、そのコンポーネント、およびビジネストランザクションの状態を正確に把握できるようにします。これにより、状況がクリティカルな状態になる前にプロアクティブにアラートを受け取り、エンドユーザーに影響が及ぶ前に対応できます。

AppDynamics の Dynamic Baselines については、[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/monitor-the-business-transaction-performance/dynamic-baselines) で詳しく説明しています。

## 遅いトランザクションスナップショットのトラブルシューティング

次の手順に従って、ビジネストランザクションを確認し、very slow なトランザクションが最も多いものを見つけてみましょう。

1. 左メニューの **Business Transactions** オプションをクリックします。
2. **View Options** ボタンをクリックします。
3. オプションのチェックボックスを、以下の画像と一致するようにオンまたはオフにします。

    ![BTs Column Config](images/bt-configure-columns.png)

4. /Supercar-Trader/car.do という名前の Business Transaction を見つけ、その Very Slow Transactions の数値をクリックして、very slow なトランザクションのスナップショットにドリルダウンします。

{{% notice title="ヒント" style="primary"  icon="lightbulb" %}}
/Supercar-Trader/car.do BT に Very Slow Transactions が存在しない場合は、Very Slow Transactions が発生している別の Business Transaction を見つけ、その列の数値をクリックしてください。スクリーンショットは多少異なる場合がありますが、概念は同じです。
{{% /notice %}}

    ![Very Slow Transaction](images/very-slow-transaction.png)

5. very slow なトランザクションのスナップショット一覧が表示されます。以下のように、最も応答時間が長いスナップショットをダブルクリックします。

    ![snapshot list](images/snapshot.png)

    トランザクションスナップショットビューアが開くと、この特定のトランザクションに含まれていたすべてのコンポーネントの flow map ビューが表示されます。このスナップショットでは、トランザクションが以下のコンポーネントを順に通過したことが示されています。

    - Web-Portal Tier
    - Api-Services Tier
    - Enquiry-Services Tier
    - MySQL Database

    左側の Potential Issues パネルでは、slow methods と slow remote services がハイライト表示されます。Potential Issues パネルからコールグラフへ直接ドリルダウンすることもできますが、この例ではスナップショット内の Flow Map を使用してトランザクション全体を追跡します。

6. スナップショットの Flow Map に表示されている Web-Portal Tier の Drill Down をクリックします。

    ![Web Portal Drilldown](images/webportal-drilldown.png)

    開いたタブには、Web-Portal Tier のコールグラフが表示されます。ほとんどの時間が outbound HTTP call で消費されていることがわかります。

7. ブロックをクリックして、問題が発生しているセグメントにドリルダウンします。HTTP リンクをクリックして、ダウンストリーム呼び出しの詳細を表示します。

    ![Call Graph](images/callgraph.png)

    ダウンストリーム呼び出しの詳細パネルには、Web-Portal Tier が Api-Services Tier に対して outbound HTTP call を行ったことが示されています。HTTP call をたどって Api-Services Tier に進みます。

8. Drill Down into Downstream Call をクリックします。

    ![Call Graph Downstream](images/callgraph_downstream.png)

    次に開くタブには、Api-Services Tier のコールグラフが表示されます。100% の時間が outbound HTTP call によるものだったことがわかります。

9. HTTP リンクをクリックして、ダウンストリーム呼び出しの詳細パネルを開きます。

    ![Downstream Call Graph](images/downstream_callgraph.png)

    ダウンストリーム呼び出しの詳細パネルには、Api-Services Tier が Enquiry-Services Tier に対して outbound HTTP call を行ったことが示されています。HTTP call をたどって Enquiry-Services Tier に進みます。

10. Drill Down into Downstream Call をクリックします。

    ![API service downstream](images/apiservices-downstream.png)

    次に開くタブには、Enquiry-Services Tier のコールグラフが表示されます。データベースへの JDBC calls がトランザクションの問題を引き起こしていたことがわかります。

11. 最も時間がかかっている JDBC リンクをクリックして、JDBC calls の詳細パネルを開きます。

    ![JDBC Callgraph](images/jdbc-callgraph.png)

    JDBC exit calls の詳細パネルには、最も時間を消費した特定のクエリが表示されます。完全な SQL ステートメントと、SQL パラメータの値を確認できます。

    ![DB Call Details](images/db-query-details.png)

## まとめ

このラボでは、まず Business Transactions を使用して、トラブルシューティングが必要な very slow なトランザクションを特定しました。次にコールグラフを調査して、遅延の原因となっているコードの具体的な箇所を特定しました。その後、ダウンストリームサービスとデータベースにドリルダウンして、遅延の根本原因をさらに分析しました。最終的に、パフォーマンスの問題の原因となっていた非効率な SQL クエリを正確に特定することができました。この一連のアプローチは、AppDynamics がトランザクションのボトルネックを効果的に切り分けて解決するのにどのように役立つかを示しています。
