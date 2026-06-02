---
title: モニタリングとトラブルシューティング - パート 2
time: 2 minutes
weight: 5
description: この演習では、ダッシュボードを確認し、Browser Snapshot のトラブルシューティングを行います。
---

この演習では、以下のタスクを完了します。

* 作成した Browser Session を確認します。
* Pages & AJAX Requests Dashboard を確認します。
* 特定の Base Page のダッシュボードを確認します。
* Browser Snapshot のトラブルシューティングを行います。

## 作成した Browser Session を確認する

セッションは、ユーザーがアプリケーションを操作する体験を分析するための時間ベースのコンテキストとして考えることができます。ブラウザセッションを調べることで、アプリケーションがどのように動作しているか、ユーザーがどのように操作しているかを理解できます。これにより、UI の修正やサーバー側のパフォーマンス最適化など、アプリケーションをより適切に管理し改善することが可能になります。

Sessions ダッシュボードに移動し、前の演習で Web アプリケーションのページを操作することによって作成したブラウザセッションを見つけます。以下の手順に従ってください。

{{% notice title="Note" style="orange"  %}}
Web アプリケーションで最後のページにアクセスしてから、ブラウザセッションがセッションリストに表示されるまで 10 分ほど待つ必要がある場合があります。10 分経ってもセッションが表示されない場合は、使用している Java Agent のバージョンに問題がある可能性があります。
{{% /notice %}}
  
1. 左メニューの **Sessions** タブをクリックします。  
2. Session Fields リストで **IP Address** にチェックを入れます。  
3. ご自身の IP アドレスで作成したセッションを見つけます。  
4. ご自身のセッションをクリックし、**View Details** をクリックします。  

![BRUM Dash 1](images/05-brum-sessions.png)

作成したセッションを見つけて開いたら、以下の手順に従ってセッションビューのさまざまな機能を探索します。

> _Note:_ ご自身のセッションでは、いずれのページにも **View Snapshot** リンクがない場合があります（手順 5 のように）。この演習の後半で、リンクがあるセッションを見つけて探索します。

1. **Session Summary** リンクをクリックして、サマリーデータを表示します。
2. 左側に表示されているページをクリックすると、そのページの詳細が右側に表示されます。
3. 左側のリストで選択しているページの完全な名前は常に確認できます。
4. ウォーターフォールビューの水平な青色のバーをクリックすると、その項目の詳細が表示されます。
5. ページによっては、サーバー側で取得された相関スナップショットへのリンクがある場合があります。
6. 設定アイコンをクリックすると、ページリストに表示される列を変更できます。

Browser RUM Sessions の詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/browser-rum-sessions) を参照してください。

![BRUM Dash 2](images/05-brum-session-details.png)

## Pages & AJAX Requests Dashboard を確認する

Pages & AJAX Requests ダッシュボードに移動し、そこにあるオプションを確認して、特定の Base Page ダッシュボードを開きます。以下の手順に従ってください。

1. 左メニューの **Pages & AJAX Requests** タブをクリックします。
2. ツールバーのオプションを探索します。
3. **localhost:8080/supercar-trader/car.do** ページをクリックします。
4. **Details** をクリックして Base Page ダッシュボードを開きます。

![BRUM Dash 3](images/05-brum-ajax-list.png)

## 特定の Base Page のダッシュボードを確認する

Base Page ダッシュボードの上部には、Controller UI の右上にある時間範囲ドロップダウンで選択された期間における主要なパフォーマンス指標として、End User Response Time、Load、Cache Hits、Page Views with JS errors が表示されます。Cache Hits は、ソースからではなく、CDN などのキャッシュから取得されたリソースを示します。

Timing Breakdown セクションには、ページ読み込みプロセスの各側面に必要な平均時間を表示するウォーターフォールグラフが表示されます。各メトリクスが何を測定しているかの詳細については、左側にある名前にカーソルを合わせてください。定義のポップアップが表示されます。さらに詳細な情報については、[**Browser RUM Metrics**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/browser-rum-metrics) を参照してください。

以下の手順に従って、**localhost:8080/supercar-trader/car.do** Base Page の詳細を確認します。

1. 時間範囲ドロップダウンを **last 2 hours** に変更します。
2. 主要なパフォーマンス指標を探索します。
3. ウォーターフォールビューのメトリクスを探索します。
4. 縦のスクロールバーを使用してページを下に移動します。
5. すべての KPI Trends のグラフを探索します。

Base Page ダッシュボードの詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/pages-and-ajax-requests/page-ajax-and-iframe-dashboards/page-and-iframe-dashboards) を参照してください。

![BRUM Dash 4](images/05-brum-main-page-summary.png)

## Browser Snapshot のトラブルシューティング

{{% notice title="Note" style="orange"  %}}
ご自身のアプリケーションには Browser Snapshot が存在しない場合があり、その場合はワークフロー全体を進めることができません。別のデモアプリケーションでこのセクションを進めたい場合は、ブラウザアプリケーション **AD-Ecommerce-Browser** に切り替えることができます。
{{% /notice %}}

Browser Snapshots リストダッシュボードに移動し、特定の Browser Snapshot を開きます。以下の手順に従ってください。

1. **Browser Snapshots** オプションをクリックします。
2. **End User Response Time** 列のヘッダーを 2 回クリックして、最大の応答時間が上に表示されるようにします。
3. 左から 3 列目にグレーまたは青のアイコンがある Browser Snapshot をクリックします。
4. **Details** をクリックして Browser Snapshot を開きます。

![BRUM Dash 6](images/06-brum-dashboard-06.png)

Browser Snapshot を開いたら、以下の手順に従って詳細を確認し、応答時間が長くなった根本原因を見つけます。

1. ウォーターフォールビューを確認して、応答時間がどこで影響を受けたかを把握します。
2. 延長された **Server Time** メトリクスに注目します。**Server Time** のラベルにカーソルを合わせてその意味を理解します。
3. Browser Snapshot に自動的にキャプチャされ相関付けされたサーバー側のトランザクションをクリックします。
4. **View Details** をクリックして、関連するサーバー側のスナップショットを開きます。

![BRUM Dash 7](images/06-brum-dashboard-07.png)

相関付けされたサーバー側のスナップショットを開いたら、以下の手順を使用してパフォーマンス低下の根本原因を特定します。

1. ブラウザで費やされたトランザクション時間の割合が最小限であることがわかります。
2. ブラウザと Web-Portal Tier の間のタイミングは、ブラウザからの初期接続から完全な応答が返されるまでを表しています。
3. JDBC 呼び出しが最も時間を要していることがわかります。
4. **Drill Down** をクリックして、Enquiry-Services Tier 内のコードレベルビューを確認します。

![BRUM Dash 8](images/06-brum-dashboard-08.png)

Enquiry-Services Tier のスナップショットセグメントを開くと、トランザクションに問題を引き起こしたデータベースへの JDBC 呼び出しがあったことがわかります。

1. 最大時間がかかっている **JDBC** リンクをクリックして、JDBC 呼び出しの詳細パネルを開きます。
2. JDBC 終了呼び出しの詳細パネルには、最も時間を要した特定のクエリが表示されます。
3. SQL パラメータ値とともに、完全な SQL ステートメントを確認できます。

Browser Snapshots の詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/browser-snapshots_1) および [**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/browser-snapshots_1/page-snapshots) を参照してください。

![BRUM Dash 9](images/06-brum-dashboard-09.png)
