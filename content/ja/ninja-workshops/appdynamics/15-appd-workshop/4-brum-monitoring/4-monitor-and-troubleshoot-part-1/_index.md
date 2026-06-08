---
title: 監視とトラブルシューティング - パート 1
time: 2 minutes
weight: 4
description: この演習では、ダッシュボードを確認し、デモアプリをナビゲートします。
---

この演習では、以下のタスクを完了します

* Browser Application Overview Dashboard の確認
* Browser Application Geo Dashboard の確認
* Browser Application Usage Stats Dashboard の確認
* Supercar-Trader アプリケーションの Web ページのナビゲーション

## Browser Application Overview Dashboard の確認

User Experience ダッシュボードに移動し、以下の手順に従って Browser Application Overview ダッシュボードにドリルインします。

1. 左メニューの **User Experience** タブをクリックします。
2. Web アプリケーション **Supercar-Trader-Web-##-###** を検索します。
3. **Details** をクリックするか、アプリケーション名をダブルクリックします。

![BRUM Dash 1](images/04-brum-app.png)

Overview ダッシュボードには、設定可能なウィジェットのセットが表示されます。デフォルトのウィジェットには、アプリケーションパフォーマンスの一般的な高レベル指標を示す複数のグラフとリストが含まれています

* End User Response Time Distribution
* End User Response Time Trend
* Total Page Requests by Geo
* End User Response Time by Geo
* Top 10 Browsers
* Top 10 Devices
* Page Requests per Minute
* Top 5 Pages by Total Requests
* Top 5 Countries by Total Page Requests

ダッシュボードの機能を確認します。

4. **+** をクリックして、ダッシュボードに追加するグラフやウィジェットを選択します。
5. ウィジェットの右下隅をクリックしてドラッグし、サイズを変更します。
6. ウィジェット内の枠線で囲まれた領域を選択して、ダッシュボード上で移動・配置します。
7. ウィジェットのタイトルをクリックして、詳細ダッシュボードにドリルインします。
8. ウィジェットの右上隅の **X** をクリックして、ダッシュボードから削除します。

ダッシュボードのウィジェットレイアウトに加えた変更は、自動的に保存されます。

Browser Application Overview ダッシュボードの詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/overview)を参照してください。

![BRUM Dash 2](images/04-brum-overview.png)

## Browser Application Geo Dashboard の確認

Geo Dashboard は、ページロードに基づく地理的位置ごとの主要なパフォーマンスメトリクスを表示します。ダッシュボード全体に表示されるメトリクスは、マップまたはグリッドで現在選択されているリージョンのものです。Map ビューでは、右パネルに表示される主要なタイミングメトリクスに含まれる国のラベル付きロードサークルが表示されます。ただし、一部の国やリージョンはグリッドビューでのみ表示されます。

Browser Application Geo ダッシュボードに移動し、以下に説明するダッシュボードの機能を確認します。

1. **Geo Dashboard** オプションをクリックします。
2. ロードサークルの1つをクリックして、リージョンにドリルダウンします。
3. リージョンの1つにカーソルを合わせて、リージョンの詳細を表示します。
4. ズームスライダーを使用して、ズームレベルを調整します。
5. **Configuration** をクリックして、マップオプションを確認します。
6. グリッドビューとマップビューを切り替えます。

Browser Application Geo ダッシュボードの詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/geo-tab)を参照してください。

![BRUM Dash 3](images/04-brum-geomap.png)

## Browser Application Usage Stats Dashboard の確認

**Usage Stats** ダッシュボードは、ユーザーのブラウザタイプとデバイス/プラットフォームに基づいた集約されたページロード使用データを表示します。

Browser Application Usage Stats ダッシュボードでは、以下のことを確認できます

* 合計エンドユーザー応答時間において最も遅いブラウザ
* レスポンスページのレンダリングが最も遅いブラウザ
* エンドユーザーが最も多く使用しているブラウザ
* 特定の国やリージョンでエンドユーザーが最も多く使用しているブラウザ

Browser Application Usage Stats ダッシュボードに移動し、以下に説明するダッシュボードの機能を確認します。

1. **Usage Stats** オプションをクリックします。
2. **Show Versions** オプションをクリックします。
3. ロード別のブラウザとバージョンの違いを確認します。
4. 円グラフのセクションにカーソルを合わせて、詳細を表示します。

![BRUM Dash 4](images/04-brum-usage-stats.png)

以下の手順で、ブラウザとバージョン別のメトリクスをさらに確認します。

5. 右側のスクロールバーを使用して、ページの下部までスクロールします。
6. ブラウザとバージョン別の利用可能なメトリクスを確認します。
7. 国別の利用可能なメトリクスを確認します。

![BRUM Dash 5](images/04-brum-usage-stats2.png)

Devices ダッシュボードに移動し、以下に説明するダッシュボードの機能を確認します。

8. **Devices** オプションをクリックします。
9. デバイス別のロードの内訳を確認します。
10. 円グラフのセクションにカーソルを合わせて、詳細を表示します。
11. デバイス別の利用可能なパフォーマンスメトリクスを確認します。

Browser Application Usage Stats ダッシュボードの詳細については、[**こちら**](https://help.splunk.com/en/appdynamics-saas/end-user-monitoring/25.7.0/end-user-monitoring/browser-monitoring/browser-app-dashboard/usage-stats)を参照してください。

![BRUM Dash 6](images/04-brum-device.png)

## Supercar-Trader アプリケーションの Web ページのナビゲーション

Browser Real User Monitoring エージェントを設定し、最初の一連の機能を確認したので、Supercar-Trader アプリケーションの Web ページをナビゲートして、追加の負荷を生成し、あなた固有のブラウザセッションを記録しましょう。

Web ブラウザでアプリのメインページを開きます。以下の URL 例では、Application VM の IP アドレスまたは完全修飾ドメイン名に置き換えてください。

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

車の問い合わせを送信します。

1. 問い合わせフォームのフィールドに適切なデータを入力します。
2. **Submit** をクリックします。

![App Page 5](images/05-app-page-05.png)

車を検索し、サイトの閲覧を続けます。

1. 上部メニューの **Search** タブをクリックします。
2. 検索ボックスに文字 **A** を入力し、**Search** をクリックします。
3. 残りのタブをクリックして、Web サイトを確認します。

![App Page 6](images/05-app-page-06.png)
