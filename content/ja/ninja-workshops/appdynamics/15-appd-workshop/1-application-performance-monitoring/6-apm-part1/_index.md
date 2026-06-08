---
title: 6. 遅いトランザクションのトラブルシューティング
weight: 6
description: このセクションでは、スナップショットを活用して遅いトランザクションのトラブルシューティング方法を学びます
---

この演習では、以下のタスクを完了します

- アプリケーションダッシュボードとフローマップの監視
- 遅いトランザクションスナップショットのトラブルシューティング

## アプリケーションダッシュボードとフローマップの監視

前の演習では、Application Flow Map の基本的な機能をいくつか確認しました。ここでは、Application Dashboard と Flow Map を使用してアプリケーション内の問題を即座に特定する方法をより詳しく見ていきましょう。

1. Health Rule Violations、Node Health の問題、および Business Transactions の健全性は、選択した時間枠に対して常にこのエリアに表示されます。ここに表示されるリンクをクリックして詳細にドリルダウンできます。
2. Transaction Scorecard には、正常、遅い、非常に遅い、停止している、エラーがあるトランザクションの数と割合が表示されます。スコアカードには、例外タイプの上位カテゴリも表示されます。ここに表示されるリンクをクリックして詳細にドリルダウンできます。
3. 異なるアプリケーションコンポーネントを接続する青い線のいずれかを左クリック（シングルクリック）すると、2つのコンポーネント間のインタラクションの概要が表示されます。
4. Tier の色付きリングの内側を左クリック（シングルクリック）すると、Flow Map に留まりながらその Tier の詳細情報が表示されます。
5. ダッシュボード下部にある3つのチャート（Load、Response Time、Errors）のいずれかの時系列にカーソルを合わせると、記録されたメトリクスの詳細が表示されます。

    ![Flow Map Components](images/flow-map-components.png)

次に、Dynamics Baselines とダッシュボード下部のチャートのオプションを見てみましょう。

1. チャート上のメトリクスを、各メトリクスに対して自動的に計算された Dynamic Baseline と比較します。
2. Dynamic Baseline は、以下の画像に示されている青い点線としてロードおよびレスポンスタイムチャートに表示されます。
3. ダッシュボード下部にある3つのチャートのいずれかに表示されるスパイクをハイライトするために、左クリックしてマウスボタンを押したまま左から右にドラッグします。
4. マウスボタンを離し、ポップアップメニューの3つのオプションのいずれかを選択します。

    ![Flow Map Components](images/flowmap_components2.png)

AppDynamics 独自の Dynamic Baselining の精度は時間とともに向上し、アプリケーション、そのコンポーネント、およびビジネストランザクションの状態を正確に把握できるようになります。これにより、事態がクリティカルな状態になる前にプロアクティブにアラートを受け取り、エンドユーザーに影響が及ぶ前にアクションを起こすことができます。

AppDynamics Dynamic Baselines の詳細については[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/monitor-the-business-transaction-performance/dynamic-baselines)をご覧ください。

## 遅いトランザクションスナップショットのトラブルシューティング
  
ビジネストランザクションを確認し、非常に遅いトランザクションの数が最も多いものを見つけましょう。以下の手順に従ってください。

1. 左メニューの **Business Transactions** オプションをクリックします。
2. **View Options** ボタンをクリックします。
3. 以下の画像に表示されているものと一致するように、オプションのチェックボックスをオンまたはオフにします

    ![BTs Column Config](images/bt-configure-columns.png)

4. /Supercar-Trader/car.do という名前の Business Transaction を見つけ、その Business Transaction の Very Slow Transactions の数をクリックして、非常に遅いトランザクションスナップショットにドリルダウンします。

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
/Supercar-Trader/car.do BT に Very Slow Transactions がない場合は、いくつかある Business Transaction を見つけ、その列の数字をクリックしてください。今後のスクリーンショットは若干異なる場合がありますが、コンセプトは同じです。
{{% /notice %}}
  
    ![Very Slow Transaction](images/very-slow-transaction.png)

5. 非常に遅いトランザクションスナップショットのリストが表示されます。以下に示すように、最も高いレスポンスタイムを持つスナップショットをダブルクリックします。

    ![snapshot list](images/snapshot.png)
  
    トランザクションスナップショットビューアが開くと、この特定のトランザクションに含まれるすべてのコンポーネントのフローマップビューが表示されます。このスナップショットは、トランザクションが以下のコンポーネントを順番に通過したことを示しています。

    - Web-Portal Tier
    - Api-Services Tier
    - Enquiry-Services Tier
    - MySQL Database

    左側の Potential Issues パネルには、遅いメソッドと遅いリモートサービスがハイライトされています。Potential Issues パネルを使用してコールグラフに直接ドリルダウンすることもできますが、この例ではスナップショット内の Flow Map を使用して完全なトランザクションを追跡します。

6. スナップショットの Flow Map に表示されている Web-Portal Tier の Drill Down をクリックします。

    ![Web Portal Drilldown](images/webportal-drilldown.png)

    開いたタブには、Web-Portal Tier のコールグラフが表示されます。時間の大部分がアウトバウンド HTTP コールによるものであることがわかります。

7. ブロックをクリックして、問題が発生しているセグメントにドリルダウンします。HTTP リンクをクリックしてダウンストリームコールの詳細を確認します。

    ![Call Graph](images/callgraph.png)

    ダウンストリームコールの詳細パネルには、Web-Portal Tier が Api-Services Tier にアウトバウンド HTTP コールを行ったことが表示されます。HTTP コールを追って Api-Services Tier に進みます。

8. Drill Down into Downstream Call をクリックします。

    ![Call Graph Downstream](images/callgraph_downstream.png)

    次に開くタブには、Api-Services Tier のコールグラフが表示されます。時間の100%がアウトバウンド HTTP コールによるものであることがわかります。

9. HTTP リンクをクリックして、ダウンストリームコールの詳細パネルを開きます。

    ![Downstream Call Graph](images/downstream_callgraph.png)

    ダウンストリームコールの詳細パネルには、Api-Services Tier が Enquiry-Services Tier にアウトバウンド HTTP コールを行ったことが表示されます。HTTP コールを追って Enquiry-Services Tier に進みます。

10. Drill Down into Downstream Call をクリックします。

    ![API service downstream](images/apiservices-downstream.png)

    次に開くタブには、Enquiry-Services Tier のコールグラフが表示されます。トランザクションに問題を引き起こしたデータベースへの JDBC コールがあったことがわかります。

11. 最も時間がかかった JDBC リンクをクリックして、JDBC コールの詳細パネルを開きます。

    ![JDBC Callgraph](images/jdbc-callgraph.png)

    JDBC exit コールの詳細パネルには、最も時間がかかった特定のクエリが表示されます。完全な SQL ステートメントと SQL パラメータ値を確認できます。

    ![DB Call Details](images/db-query-details.png)

## まとめ

このラボでは、まず Business Transactions を使用して、トラブルシューティングが必要な非常に遅いトランザクションを特定しました。次に、コールグラフを調べて遅延の原因となっているコードの特定の部分を突き止めました。その後、ダウンストリームサービスとデータベースにドリルダウンして、遅延の根本原因をさらに分析しました。最終的に、パフォーマンス問題の原因となっている非効率な SQL クエリを正確に特定することに成功しました。この包括的なアプローチは、AppDynamics がトランザクションのボトルネックを効果的に特定し解決する方法を示しています。
