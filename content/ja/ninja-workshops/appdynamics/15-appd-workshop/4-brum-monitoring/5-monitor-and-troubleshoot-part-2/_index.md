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

## 作成した Browser Session を確認する

セッションは、ユーザーがアプリケーションとやり取りする体験を分析するための時間ベースのコンテキストと考えることができます。ブラウザセッションを調べることで、アプリケーションのパフォーマンスやユーザーがどのようにアプリケーションとやり取りしているかを理解できます。これにより、UI の変更やサーバーサイドのパフォーマンス最適化など、アプリケーションをより適切に管理・改善できるようになります。

Sessions ダッシュボードに移動し、前の演習で Web アプリケーションのページをナビゲートした際に作成されたブラウザセッションを見つけます。以下の手順に従ってください。

{{% notice title="Note" style="orange"  %}}
Web アプリケーションの最後のページにアクセスしてから、セッションリストにブラウザセッションが表示されるまで10分ほどかかる場合があります。10分経ってもセッションが表示されない場合は、使用中の Java Agent のバージョンに問題がある可能性があります。
{{% /notice %}}
  
1. 左メニューの **Sessions** タブをクリックします。  
2. Session Fields リストで **IP Address** を確認します。  
3. 自分の IP Address でセッションを見つけます。  
4. セッションをクリックし、**View Details** をクリックします。  

![BRUM Dash 1](images/05-brum-sessions.png)

作成したセッションを見つけて開いたら、以下の手順に従ってセッションビューのさまざまな機能を確認します。

> _Note:_ セッションのどのページにも **View Snapshot** リンクがない場合があります（手順5を参照）。この演習の後半で、リンクがあるセッションを見つけて確認します。

1. **Session Summary** リンクをクリックしてサマリーデータを表示します。
2. 左側のリストに表示されているページをクリックすると、右側にそのページの詳細が表示されます。
3. 左側のリストで選択したページのフルネームは常に確認できます。
4. ウォーターフォールビューの水平の青いバーをクリックすると、そのアイテムの詳細が表示されます。
5. 一部のページには、サーバーサイドでキャプチャされた関連スナップショットへのリンクがある場合があります。
6. 設定アイコンをクリックして、ページリストに表示される列を変更します。

Browser RUM Sessions の詳細については[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/browser-rum-sessions)をご覧ください。

![BRUM Dash 2](images/05-brum-session-details.png)

## Pages & AJAX Requests ダッシュボードを確認する

Pages & AJAX Requests ダッシュボードに移動し、オプションを確認して、以下の手順で特定の Base Page ダッシュボードを開きます。

1. 左メニューの **Pages & AJAX Requests** タブをクリックします。
2. ツールバーのオプションを確認します。
3. **localhost:8080/supercar-trader/car.do** ページをクリックします。
4. **Details** をクリックして Base Page ダッシュボードを開きます。

![BRUM Dash 3](images/05-brum-ajax-list.png)

## 特定の Base Page のダッシュボードを確認する

Base Page ダッシュボードの上部には、Controller UI の右上にある時間範囲ドロップダウンで選択された期間における主要パフォーマンス指標（End User Response Time、Load、Cache Hits、Page Views with JS errors）が表示されます。Cache Hits は、ソースからではなく CDN などのキャッシュから取得されたリソースを示します。

Timing Breakdown セクションには、ページロードプロセスの各段階に必要な平均時間を表示するウォーターフォールグラフが表示されます。各メトリクスが何を測定しているかについての詳細は、左側の名前にカーソルを合わせるとポップアップで定義が表示されます。より詳細な情報については、[**Browser RUM Metrics**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/browser-rum-metrics) を参照してください。

以下の手順で **localhost:8080/supercar-trader/car.do** Base Page の詳細を確認します。

1. 時間範囲ドロップダウンを **last 2 hours** に変更します。
2. 主要パフォーマンス指標を確認します。
3. ウォーターフォールビューのメトリクスを確認します。
4. 垂直スクロールバーを使用してページを下にスクロールします。
5. すべての KPI Trends のグラフを確認します。

Base Page ダッシュボードの詳細については[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-real-user-monitoring/overview-of-the-controller-ui-for-browser-rum/pages-and-ajax-requests/page-ajax-and-iframe-dashboards/page-and-iframe-dashboards)をご覧ください。

![BRUM Dash 4](images/05-brum-main-page-summary.png)

## Browser Snapshot のトラブルシューティング

{{% notice title="Note" style="orange"  %}}
アプリケーションにブラウザスナップショットがない場合があり、その場合はワークフロー全体を実行できません。別のデモアプリケーションでこのセクションを進めたい場合は、ブラウザアプリケーション **AD-Ecommerce-Browser** に切り替えることができます。
{{% /notice %}}

Browser Snapshots リストダッシュボードに移動し、以下の手順で特定の Browser Snapshot を開きます。

1. **Browser Snapshots** オプションをクリックします。
2. **End User Response Time** 列ヘッダーを2回クリックして、最大のレスポンスタイムを上部に表示します。
3. 左から3番目の列にグレーまたは青のアイコンがあるブラウザスナップショットをクリックします。
4. **Details** をクリックしてブラウザスナップショットを開きます。

![BRUM Dash 6](images/06-brum-dashboard-06.png)

ブラウザスナップショットを開いたら、以下の手順で詳細を確認し、大きなレスポンスタイムの根本原因を特定します。

1. ウォーターフォールビューを確認して、レスポンスタイムがどこで影響を受けたかを理解します。
2. **Server Time** メトリクスが長くなっていることに注目します。**Server Time** のラベルにカーソルを合わせてその意味を確認します。
3. ブラウザスナップショットに自動的にキャプチャされ関連付けられたサーバーサイドトランザクションをクリックします。
4. **View Details** をクリックして、関連するサーバーサイドスナップショットを開きます。

![BRUM Dash 7](images/06-brum-dashboard-07.png)

関連するサーバーサイドスナップショットを開いたら、以下の手順でパフォーマンス低下の根本原因を特定します。

1. ブラウザで費やされたトランザクション時間の割合は最小限であることがわかります。
2. ブラウザと Web-Portal Tier 間のタイミングは、ブラウザからの初期接続から完全なレスポンスが返されるまでを表しています。
3. JDBC コールが最も時間を費やしていることがわかります。
4. **Drill Down** をクリックして、Enquiry-Services Tier 内のコードレベルビューを確認します。

![BRUM Dash 8](images/06-brum-dashboard-08.png)

Enquiry-Services Tier のスナップショットセグメントを開くと、トランザクションに問題を引き起こしたデータベースへの JDBC コールがあったことがわかります。

1. 最も時間がかかった **JDBC** リンクをクリックして、JDBC コールの詳細パネルを開きます。
2. JDBC exit コールの詳細パネルには、最も時間がかかった特定のクエリが表示されます。
3. SQL パラメータ値とともに完全な SQL ステートメントを確認できます。

Browser Snapshots の詳細については[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/browser-snapshots_1)および[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/browser-snapshots_1/page-snapshots)をご覧ください。

![BRUM Dash 9](images/06-brum-dashboard-09.png)
