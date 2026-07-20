---
title: モニタリングとトラブルシューティング - パート2
time: 2 minutes
weight: 5
description: この演習では、ダッシュボードの確認とBrowser Snapshotのトラブルシューティングを行います。
---

この演習では、以下のタスクを完了します。

* 作成したBrowser Sessionの確認
* Pages & AJAX Requestsダッシュボードの確認
* 特定のBase Pageのダッシュボードの確認
* Browser Snapshotのトラブルシューティング

## 作成したBrowser Sessionの確認

セッションは、アプリケーションとのユーザーインタラクション体験を分析するための時間ベースのコンテキストと考えることができます。ブラウザセッションを調べることで、アプリケーションのパフォーマンスやユーザーがどのように操作しているかを理解できます。これにより、UIの変更やサーバーサイドのパフォーマンス最適化など、アプリケーションの管理と改善をより効果的に行えます。

Sessionsダッシュボードに移動し、前の演習でWebアプリケーションのページをナビゲートした際に作成したブラウザセッションを見つけます。以下の手順に従います。

{{% notice title="注意" style="orange"  %}}
Webアプリケーションの最後のページにアクセスしてから、セッションリストにブラウザセッションが表示されるまで10分ほど待つ必要がある場合があります。10分経ってもセッションが表示されない場合は、使用中のJava Agentバージョンの問題が原因である可能性があります。
{{% /notice %}}
  
1. 左メニューの **Sessions** タブをクリックします。  
2. Session Fieldsリストの **IP Address** を確認します。  
3. 自分のIPアドレスで作成したセッションを見つけます。  
4. セッションをクリックし、 **View Details** をクリックします。  

![BRUM Dash 1](images/05-brum-sessions.png)

作成したセッションを見つけて開いたら、以下の手順でセッションビューのさまざまな機能を確認します。

> _注意:_ セッションのどのページにも **View Snapshot** リンクがない場合があります（ステップ5を参照）。この演習の後半で、リンクがあるセッションを見つけて確認します。

1. **Session Summary** リンクをクリックしてサマリーデータを表示します。
2. 左側に一覧表示されているページをクリックすると、右側にそのページの詳細が表示されます。
3. 左側のリストで選択したページのフルネームを常に確認できます。
4. ウォーターフォールビューの水平の青いバーをクリックすると、そのアイテムの詳細が表示されます。
5. 一部のページには、サーバーサイドでキャプチャされた相関スナップショットへのリンクがある場合があります。
6. 設定アイコンをクリックして、ページリストに表示される列を変更します。

Browser RUM Sessionsの詳細については[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/browser-rum-sessions)を参照してください。

![BRUM Dash 2](images/05-brum-session-details.png)

## Pages & AJAX Requestsダッシュボードの確認

Pages & AJAX Requestsダッシュボードに移動し、オプションを確認して、以下の手順で特定のBase Pageダッシュボードを開きます。

1. 左メニューの **Pages & AJAX Requests** タブをクリックします。
2. ツールバーのオプションを確認します。
3. **localhost:8080/supercar-trader/car.do** ページをクリックします。
4. **Details** をクリックしてBase Pageダッシュボードを開きます。

![BRUM Dash 3](images/05-brum-ajax-list.png)

## 特定のBase Pageのダッシュボードの確認

Base Pageダッシュボードの上部には、Controller UIの右上にある時間範囲ドロップダウンで選択された期間にわたる主要パフォーマンス指標（End User Response Time、Load、Cache Hits、Page Views with JS errors）が表示されます。Cache Hitsは、ソースからではなくCDNなどのキャッシュから取得されたリソースを示します。

Timing Breakdownセクションには、ページロードプロセスの各側面に必要な平均時間を表示するウォーターフォールグラフが表示されます。各メトリクスが何を測定しているかの詳細については、左側の名前にカーソルを合わせてください。定義がポップアップ表示されます。より詳細な情報については、[**Browser RUM Metrics**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/browser-rum-metrics)を参照してください。

以下の手順で **localhost:8080/supercar-trader/car.do** Base Pageの詳細を確認します。

1. 時間範囲ドロップダウンを **last 2 hours** に変更します。
2. 主要パフォーマンス指標を確認します。
3. ウォーターフォールビューのメトリクスを確認します。
4. 垂直スクロールバーを使用してページを下にスクロールします。
5. すべてのKPI Trendsのグラフを確認します。

Base Pageダッシュボードの詳細については[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/pages-and-ajax-requests/page-ajax-and-iframe-dashboards/page-and-iframe-dashboards)を参照してください。

![BRUM Dash 4](images/05-brum-main-page-summary.png)

## Browser Snapshotのトラブルシューティング

{{% notice title="注意" style="orange"  %}}
アプリケーションにブラウザスナップショットがない場合、ワークフロー全体を実行できないことがあります。別のデモアプリケーションでこのセクションを実行したい場合は、ブラウザアプリケーション **AD-Ecommerce-Browser** に切り替えることができます。
{{% /notice %}}

Browser Snapshotsリストダッシュボードに移動し、以下の手順で特定のBrowser Snapshotを開きます。

1. **Browser Snapshots** オプションをクリックします。
2. **End User Response Time** 列ヘッダーを2回クリックして、最大の応答時間を上部に表示します。
3. 左から3番目の列にグレーまたは青のアイコンがあるブラウザスナップショットをクリックします。
4. **Details** をクリックしてブラウザスナップショットを開きます。

![BRUM Dash 6](images/06-brum-dashboard-06.png)

ブラウザスナップショットを開いたら、以下の手順で詳細を確認し、大きな応答時間の根本原因を見つけます。

1. ウォーターフォールビューを確認して、応答時間がどこで影響を受けたかを理解します。
2. 延長された **Server Time** メトリクスに注目します。 **Server Time** のラベルにカーソルを合わせてその意味を確認します。
3. ブラウザスナップショットに自動的にキャプチャされ相関付けられたサーバーサイドトランザクションをクリックします。
4. **View Details** をクリックして、関連するサーバーサイドスナップショットを開きます。

![BRUM Dash 7](images/06-brum-dashboard-07.png)

相関するサーバーサイドスナップショットを開いたら、以下の手順でパフォーマンス低下の根本原因を特定します。

1. ブラウザで費やされたトランザクション時間の割合が最小限であることが確認できます。
2. ブラウザとWeb-Portal Tier間のタイミングは、ブラウザからの初期接続から完全なレスポンスが返されるまでを表しています。
3. JDBC呼び出しが最も時間を消費していることが確認できます。
4. **Drill Down** をクリックして、Enquiry-Services Tier内のコードレベルビューを確認します。

![BRUM Dash 8](images/06-brum-dashboard-08.png)

Enquiry-Services Tierのスナップショットセグメントを開くと、トランザクションに問題を引き起こしたデータベースへのJDBC呼び出しがあったことが確認できます。

1. 最大時間の **JDBC** リンクをクリックして、JDBC呼び出しの詳細パネルを開きます。
2. JDBC exit呼び出しの詳細パネルには、最も時間がかかった特定のクエリが表示されます。
3. 完全なSQLステートメントとSQLパラメータ値を確認できます。

Browser Snapshotsの詳細については[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/browser-snapshots_1)と[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/browser-snapshots_1/page-snapshots)を参照してください。

![BRUM Dash 9](images/06-brum-dashboard-09.png)
