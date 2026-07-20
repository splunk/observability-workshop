---
title: 6. 遅いトランザクションのトラブルシューティング
weight: 6
description: このセクションでは、スナップショットを活用して遅いトランザクションをトラブルシューティングする方法を学びます
---

この演習では、以下のタスクを完了します。

- アプリケーションダッシュボードとフローマップを監視します。
- 遅いトランザクションスナップショットをトラブルシューティングします。

## アプリケーションダッシュボードとフローマップの監視

前の演習では、Application Flow Mapの基本機能をいくつか確認しました。Application DashboardとFlow Mapを使用してアプリケーション内の問題を即座に特定する方法をさらに詳しく見ていきましょう。

1. 正常性ルール違反、Node Healthの問題、およびBusiness Transactionsの正常性は、選択した時間枠に対して常にこのエリアに表示されます。ここにあるリンクをクリックして詳細にドリルダウンできます。
2. Transaction Scorecardには、正常、遅い、非常に遅い、停止、エラーのあるトランザクションの数とパーセンテージが表示されます。Scorecardには例外タイプの上位カテゴリも表示されます。ここにあるリンクをクリックして詳細にドリルダウンできます。
3. 異なるアプリケーションコンポーネントを接続する青い線のいずれかを左クリック（シングルクリック）すると、2つのコンポーネント間のインタラクションの概要が表示されます。
4. Tierの色付きリング内を左クリック（シングルクリック）すると、Flow Map上に留まりながらそのTierの詳細情報が表示されます。
5. ダッシュボード下部にある3つのチャート（Load、Response Time、Errors）のいずれかの時系列にカーソルを合わせると、記録されたメトリクスの詳細が表示されます。

    ![Flow Map Components](images/flow-map-components.png)

次に、Dynamic Baselineとダッシュボード下部のチャートのオプションを見てみましょう。

1. チャート上のメトリクスを、各メトリクスに対して自動的に計算されたDynamic Baselineと比較します。
2. Dynamic Baselineは、以下の画像に示すように、LoadチャートとResponse Timeチャートに青い点線で表示されます。
3. ダッシュボード下部にある3つのチャートのいずれかでスパイクが見られる箇所を、マウスボタンを左クリックして押したまま左から右にドラッグしてハイライトします。
4. マウスボタンを離し、ポップアップメニューの3つのオプションから1つを選択します。

    ![Flow Map Components](images/flowmap_components2.png)

AppDynamics独自のDynamic Baseliningの精度は時間とともに向上し、アプリケーション、そのコンポーネント、およびBusiness Transactionsの状態を正確に把握できるようになります。これにより、クリティカルな状態になる前にプロアクティブにアラートを受け取り、エンドユーザーに影響が出る前にアクションを取ることができます。

AppDynamicsのDynamic Baselineの詳細は[こちら](https://help.splunk.com/en/appdynamics-saas/application-performance-monitoring/25.7.0/business-transactions/monitor-the-business-transaction-performance/dynamic-baselines)を参照してください。

## 遅いトランザクションスナップショットのトラブルシューティング

Business Transactionsを確認し、非常に遅いトランザクションの数が最も多いものを以下の手順で見つけましょう。

1. 左メニューの **Business Transactions** オプションをクリックします。
2. **View Options** ボタンをクリックします。
3. 以下の画像に一致するようにオプションのチェックボックスをオン/オフにします。

    ![BTs Column Config](images/bt-configure-columns.png)

4. /Supercar-Trader/car.doという名前のBusiness Transactionを見つけ、そのBusiness TransactionのVery Slow Transactionsの数字をクリックして、非常に遅いトランザクションスナップショットにドリルダウンします。

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
/Supercar-Trader/car.doのBTにVery Slow Transactionsがない場合は、Very Slow Transactionsがある別のBusiness Transactionを見つけ、そのカラムの数字をクリックしてください。以降のスクリーンショットは若干異なる場合がありますが、コンセプトは同じです。
{{% /notice %}}
  
    ![Very Slow Transaction](images/very-slow-transaction.png)

5. 非常に遅いトランザクションスナップショットのリストが表示されます。以下に示すように、最もレスポンスタイムが高いスナップショットをダブルクリックします。

    ![snapshot list](images/snapshot.png)
  
    トランザクションスナップショットビューアが開くと、この特定のトランザクションに関与したすべてのコンポーネントのフローマップビューが表示されます。このスナップショットは、トランザクションが以下のコンポーネントを順番に通過したことを示しています。

    - Web-Portal Tier
    - Api-Services Tier
    - Enquiry-Services Tier
    - MySQL Database

    左側のPotential Issuesパネルには、遅いメソッドと遅いリモートサービスがハイライトされます。Potential Issuesパネルからコールグラフに直接ドリルダウンすることもできますが、この例ではスナップショット内のFlow Mapを使用してトランザクション全体を追跡します。

6. スナップショットのFlow Mapに表示されているWeb-Portal Tierの **Drill Down** をクリックします。

    ![Web Portal Drilldown](images/webportal-drilldown.png)

    開いたタブにはWeb-Portal Tierのコールグラフが表示されます。時間の大部分がアウトバウンドHTTPコールによるものであることがわかります。

7. 問題が発生しているセグメントにドリルダウンするためにブロックをクリックします。HTTPリンクをクリックしてダウンストリームコールの詳細を表示します。

    ![Call Graph](images/callgraph.png)

    ダウンストリームコールの詳細パネルには、Web-Portal TierがApi-Services TierへアウトバウンドHTTPコールを行ったことが表示されます。HTTPコールをたどってApi-Services Tierに進みます。

8. **Drill Down into Downstream Call** をクリックします。

    ![Call Graph Downstream](images/callgraph_downstream.png)

    次に開いたタブにはApi-Services Tierのコールグラフが表示されます。時間の100%がアウトバウンドHTTPコールによるものであることがわかります。

9. HTTPリンクをクリックしてダウンストリームコールの詳細パネルを開きます。

    ![Downstream Call Graph](images/downstream_callgraph.png)

    ダウンストリームコールの詳細パネルには、Api-Services TierがEnquiry-Services TierへアウトバウンドHTTPコールを行ったことが表示されます。HTTPコールをたどってEnquiry-Services Tierに進みます。

10. **Drill Down into Downstream Call** をクリックします。

    ![API service downstream](images/apiservices-downstream.png)  

    次に開いたタブにはEnquiry-Services Tierのコールグラフが表示されます。データベースへのJDBCコールがトランザクションの問題を引き起こしていたことがわかります。

11. 最も時間がかかっているJDBCリンクをクリックして、JDBCコールの詳細パネルを開きます。

    ![JDBC Callgraph](images/jdbc-callgraph.png)  

    JDBC exitコールの詳細パネルには、最も時間がかかった特定のクエリが表示されます。完全なSQL文とSQLパラメータ値を確認できます。

    ![DB Call Details](images/db-query-details.png)  

## まとめ

この演習では、まずBusiness Transactionsを使用してトラブルシューティングが必要な非常に遅いトランザクションを特定しました。次に、コールグラフを調べて遅延を引き起こしているコードの特定部分を突き止めました。その後、ダウンストリームサービスとデータベースにドリルダウンして遅延の根本原因をさらに分析しました。最終的に、パフォーマンス問題の原因となっている非効率なSQLクエリを正確に特定することができました。この包括的なアプローチは、AppDynamicsがトランザクションのボトルネックを効果的に分離し解決するのにどのように役立つかを示しています。
