---
title: モニタリングとトラブルシューティング - パート 2
time: 2 minutes
weight: 5
description: この演習では、ダッシュボードの確認と Browser Snapshot のトラブルシューティングを行います。
---

この演習では、以下のタスクを完了します

* 作成した Browser Session を確認する。
* Pages & AJAX Requests ダッシュボードを確認する。
* 特定の Base Page のダッシュボードを確認する。
* Browser Snapshot のトラブルシューティングを行う。

## 作成した Browser Session の確認

セッションは、ユーザーがアプリケーションとやり取りする体験を分析するための時間ベースのコンテキストと考えることができます。ブラウザセッションを調べることで、アプリケーションのパフォーマンスやユーザーの操作方法を把握できます。これにより、UI の変更やサーバーサイドのパフォーマンス最適化など、アプリケーションの管理と改善をより効果的に行うことができます。

Sessions ダッシュボードに移動し、前の演習で Web アプリケーションのページを操作して作成したブラウザセッションを見つけます。以下の手順に従ってください。

{{% notice title="Note" style="orange"  %}}
Web アプリケーションの最後のページにアクセスしてから、ブラウザセッションがセッションリストに表示されるまで 10 分ほど待つ必要がある場合があります。10 分経ってもセッションが表示されない場合は、使用中の Java Agent のバージョンに問題がある可能性があります。
{{% /notice %}}
  
1. 左メニューの **Sessions** タブをクリックします。  
2. Session Fields リストの **IP Address** を確認します。  
3. IP Address で作成したセッションを見つけます。  
4. セッションをクリックし、**View Details** をクリックします。  

![BRUM Dash 1](images/05-brum-sessions.png)

作成したセッションを見つけて開いたら、以下の手順に従ってセッションビューのさまざまな機能を確認します。

> _Note:_ セッションのページに **View Snapshot** リンクがない場合があります（手順 5 を参照）。この演習の後半で、リンクがあるセッションを見つけて確認します。

5. **Session Summary** リンクをクリックして、サマリーデータを表示します。
6. 左側に表示されたページをクリックすると、右側にそのページの詳細が表示されます。
7. 左のリストで選択したページのフルネームを常に確認できます。
8. ウォーターフォールビューの青い水平バーをクリックすると、そのアイテムの詳細が表示されます。
9. 一部のページには、サーバーサイドでキャプチャされた関連スナップショットへのリンクがある場合があります。
10. 設定アイコンをクリックして、ページリストに表示する列を変更します。

Browser RUM Sessions の詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/browser-rum-sessions)をご覧ください。

![BRUM Dash 2](images/05-brum-session-details.png)

## Pages & AJAX Requests ダッシュボードの確認

Pages & AJAX Requests ダッシュボードに移動し、オプションを確認して、以下の手順に従って特定の Base Page ダッシュボードを開きます。

1. 左メニューの **Pages & AJAX Requests** タブをクリックします。
2. ツールバーのオプションを確認します。
3. **localhost:8080/supercar-trader/car.do** ページをクリックします。
4. **Details** をクリックして Base Page ダッシュボードを開きます。

![BRUM Dash 3](images/05-brum-ajax-list.png)

## 特定の Base Page のダッシュボードの確認

Base Page ダッシュボードの上部には、Controller UI の右上にある時間範囲ドロップダウンで選択した期間にわたる主要パフォーマンス指標（End User Response Time、Load、Cache Hits、Page Views with JS errors）が表示されます。Cache Hits は、ソースからではなく CDN などのキャッシュから取得されたリソースを示します。

Timing Breakdown セクションには、ページロードプロセスの各側面に必要な平均時間を表示するウォーターフォールグラフがあります。各メトリクスが何を測定しているかの詳細については、左側のメトリクス名にマウスオーバーしてください。定義を含むポップアップが表示されます。より詳細な情報については、[**Browser RUM Metrics**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/browser-rum-metrics)を参照してください。

以下の手順に従って、**localhost:8080/supercar-trader/car.do** Base Page の詳細を確認します。

1. 時間範囲ドロップダウンを **last 2 hours** に変更します。
2. 主要パフォーマンス指標を確認します。
3. ウォーターフォールビューのメトリクスを確認します。
4. 垂直スクロールバーを使用してページを下にスクロールします。
5. すべての KPI Trends のグラフを確認します。

Base Page ダッシュボードの詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/pages-and-ajax-requests/page-ajax-and-iframe-dashboards/page-and-iframe-dashboards)をご覧ください。

![BRUM Dash 4](images/05-brum-main-page-summary.png)

## Browser Snapshot のトラブルシューティング

{{% notice title="Note" style="orange"  %}}
アプリケーションにブラウザスナップショットがない場合、ワークフロー全体を実行できないことがあります。別のデモアプリケーションでこのセクションを進めたい場合は、ブラウザアプリケーション **AD-Ecommerce-Browser** に切り替えることができます。
{{% /notice %}}

Browser Snapshots リストダッシュボードに移動し、以下の手順に従って特定の Browser Snapshot を開きます。

1. **Browser Snapshots** オプションをクリックします。
2. **End User Response Time** 列ヘッダーを 2 回クリックして、最大のレスポンスタイムを上部に表示します。
3. 左から 3 番目の列にグレーまたは青のアイコンがあるブラウザスナップショットをクリックします。
4. **Details** をクリックしてブラウザスナップショットを開きます。

![BRUM Dash 6](images/06-brum-dashboard-06.png)

ブラウザスナップショットを開いたら、以下の手順に従って詳細を確認し、レスポンスタイムが大きい原因を特定します。

1. ウォーターフォールビューを確認して、レスポンスタイムが影響を受けた箇所を把握します。
2. 延長された **Server Time** メトリクスに注目します。**Server Time** のラベルにマウスオーバーして、その意味を確認します。
3. ブラウザスナップショットに自動的にキャプチャおよび関連付けられたサーバーサイドトランザクションをクリックします。
4. **View Details** をクリックして、関連するサーバーサイドスナップショットを開きます。

![BRUM Dash 7](images/06-brum-dashboard-07.png)

関連するサーバーサイドスナップショットを開いたら、以下の手順に従ってパフォーマンス低下の根本原因を特定します。

1. ブラウザで費やされたトランザクション時間の割合が最小限であることが確認できます。
2. ブラウザと Web-Portal Tier 間のタイミングは、ブラウザからの最初の接続からフルレスポンスが返されるまでを表しています。
3. JDBC コールが最も時間を費やしていることが確認できます。
4. **Drill Down** をクリックして、Enquiry-Services Tier 内のコードレベルビューを確認します。

![BRUM Dash 8](images/06-brum-dashboard-08.png)

Enquiry-Services Tier のスナップショットセグメントを開くと、トランザクションに問題を引き起こしたデータベースへの JDBC コールがあることが確認できます。

1. 最大時間の **JDBC** リンクをクリックして、JDBC コールの詳細パネルを開きます。
2. JDBC 出口コールの詳細パネルには、最も時間がかかった特定のクエリが表示されます。
3. 完全な SQL ステートメントと SQL パラメータ値を確認できます。

Browser Snapshots の詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/browser-snapshots_1)および[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/browser-snapshots_1/page-snapshots)をご覧ください。

![BRUM Dash 9](images/06-brum-dashboard-09.png)
