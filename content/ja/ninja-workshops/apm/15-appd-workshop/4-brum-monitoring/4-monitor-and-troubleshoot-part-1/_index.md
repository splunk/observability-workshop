---
title: モニタリングとトラブルシューティング - パート 1
time: 2 minutes
weight: 4
description: この演習では、ダッシュボードを確認し、デモアプリを操作します。
---

この演習では、以下のタスクを実行します。

* Browser Application Overview ダッシュボードの確認
* Browser Application Geo ダッシュボードの確認
* Browser Application Usage Stats ダッシュボードの確認
* Supercar-Trader アプリケーション Web ページの操作

## Browser Application Overview ダッシュボードの確認

User Experience ダッシュボードに移動し、以下の手順で Browser Application Overview ダッシュボードにドリルダウンします。

1. 左メニューの **User Experience** タブをクリックします。
2. ご自身の Web アプリケーション **Supercar-Trader-Web-##-###** を検索します。
3. **Details** をクリックするか、アプリケーション名をダブルクリックします。

![BRUM Dash 1](images/04-brum-app.png)

Overview ダッシュボードには、設定可能なウィジェットのセットが表示されます。デフォルトのウィジェットには、アプリケーションパフォーマンスの一般的なハイレベル指標を示す複数のグラフとリストが含まれています。たとえば次のとおりです。

* End User Response Time Distribution
* End User Response Time Trend
* Total Page Requests by Geo
* End User Response Time by Geo
* Top 10 Browsers
* Top 10 Devices
* Page Requests per Minute
* Top 5 Pages by Total Requests
* Top 5 Countries by Total Page Requests

ダッシュボードの機能を試してみましょう。

1. **+** をクリックして、ダッシュボードに追加するグラフやウィジェットを選択します。
2. 任意のウィジェットの右下隅をクリックしてドラッグすると、サイズを変更できます。
3. ウィジェット内の枠線で囲まれた領域を選択し、ダッシュボード上で移動・配置します。
4. 任意のウィジェットのタイトルをクリックすると、詳細ダッシュボードにドリルダウンします。
5. 任意のウィジェットの右上隅にある **X** をクリックすると、ダッシュボードからウィジェットを削除できます。

ダッシュボードのウィジェットレイアウトに加えた変更は自動的に保存されます。

Browser Application Overview ダッシュボードの詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/overview) を参照してください。

![BRUM Dash 2](images/04-brum-overview.png)

## Browser Application Geo ダッシュボードの確認

Geo Dashboard では、ページロードに基づいて地理的な位置ごとの主要パフォーマンス指標が表示されます。ダッシュボード全体に表示される指標は、マップまたはグリッドで現在選択されているリージョンのものです。マップビューには、右側のパネルに表示されるキータイミングメトリクスに該当する国のラベル付きロードサークルが表示されます。ただし、一部の国やリージョンはグリッドビューにのみ表示されます。

Browser Application Geo ダッシュボードに移動し、以下に説明するダッシュボードの機能を試してみましょう。

1. **Geo Dashboard** オプションをクリックします。
2. ロードサークルの 1 つをクリックして、リージョンにドリルダウンします。
3. リージョンの 1 つにマウスオーバーすると、リージョンの詳細が表示されます。
4. ズームスライダーを使用してズームレベルを調整します。
5. **Configuration** をクリックして、マップオプションを試してみましょう。
6. グリッドビューとマップビューを切り替えます。

Browser Application Geo ダッシュボードの詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/geo-tab) を参照してください。

![BRUM Dash 3](images/04-brum-geomap.png)

## Browser Application Usage Stats ダッシュボードの確認

**Usage Stats** ダッシュボードでは、ユーザーのブラウザタイプとデバイス/プラットフォームに基づき、集計されたページロードの利用統計データが表示されます。

Browser Application Usage Stats ダッシュボードでは、以下の点を把握できます。

* エンドユーザー応答時間の合計が最も遅いブラウザ
* 応答ページのレンダリングが最も遅いブラウザ
* 多くのエンドユーザーが使用しているブラウザ
* 特定の国または地域で多くのエンドユーザーが使用しているブラウザ

Browser Application Usage Stats ダッシュボードに移動し、以下に説明するダッシュボードの機能を試してみましょう。

1. **Usage Stats** オプションをクリックします。
2. **Show Versions** オプションをクリックします。
3. ロード別に、さまざまなブラウザとバージョンを確認します。
4. 円グラフのセクションにマウスオーバーすると、詳細が表示されます。

![BRUM Dash 4](images/04-brum-usage-stats.png)

以下の手順で、ブラウザとバージョン別にさらに多くのメトリクスを確認します。

1. 右側のスクロールバーを使用して、ページの一番下までスクロールします。
2. ブラウザとバージョン別に利用可能なメトリクスを確認します。
3. 国別に利用可能なメトリクスを確認します。

![BRUM Dash 5](images/04-brum-usage-stats2.png)

Devices ダッシュボードに移動し、以下に説明するダッシュボードの機能を試してみましょう。

1. **Devices** オプションをクリックします。
2. デバイス別のロード内訳を確認します。
3. 円グラフのセクションにマウスオーバーすると、詳細が表示されます。
4. デバイス別に利用可能なパフォーマンスメトリクスを確認します。

Browser Application Usage Stats ダッシュボードの詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/usage-stats) を参照してください。

![BRUM Dash 6](images/04-brum-device.png)

## Supercar-Trader アプリケーション Web ページの操作

Browser Real User Monitoring エージェントを設定し、最初の一連の機能を確認できたので、次は Supercar-Trader アプリケーションの Web ページを操作して、追加のロードを生成し、固有のブラウザセッションを記録してみましょう。

Web ブラウザでアプリのメインページを開きます。以下の URL の例では、ご自身の Application VM の IP アドレスまたは完全修飾ドメイン名に置き換えてください。

``` bash
http://[application-vm-ip-address]:8080/Supercar-Trader/home.do
```

アプリケーションのホームページが表示されます。

![App Page 1](images/04-brum-supercar-homepage.jpeg)

利用可能な Ferrari の一覧を開きます。

1. 上部メニューの **Supercars** タブをクリックします。
2. Ferrari のロゴをクリックします。

![App Page 2](images/05-app-page-02.png)

Ferrari の一覧が表示されます。

![App Page 3](images/05-app-page-03.png)

最初の Ferrari の画像をクリックします。

1. **View Enquiries** をクリックします。
2. **Enquire** をクリックします。

![App Page 4](images/05-app-page-04.png)

その車に関する問い合わせを送信します。

1. 問い合わせフォームの各項目に適切なデータを入力します。
2. **Submit** をクリックします。

![App Page 5](images/05-app-page-05.png)

車を検索し、引き続きサイトを閲覧します。

1. 上部メニューの **Search** タブをクリックします。
2. 検索ボックスに **A** の文字を入力し、**Search** をクリックします。
3. 残りのタブをクリックして、Web サイトを操作してみましょう。

![App Page 6](images/05-app-page-06.png)
