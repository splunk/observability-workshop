---
title: RUM Overview
linkTitle: 1. RUM Overview
weight: 1
time: 5 minutes
---

この演習では、RUM Overviewダッシュボードを開きます。ここで表示されるデータは生成されたものであり、あなた自身を含むすべての参加者のデータも含まれています。先ほどAstronomy Shopで行ったブラウジングやショッピングが、ページビュー、エラー、読み込みパフォーマンスなどの実ユーザーメトリクスとして表示されます。Real User Monitoringを通じて自分のセッションを確認できます。

{{% exercise title="ストアでフィルタリング" %}}

* Splunk Observability Cloudのメインメニューで **Digital Experience** にカーソルを合わせ、以下に示すように **Real User Monitoring** セクションから **Overview** **(1)** をクリックします。

![RUM](../images/rum-de.png)

* **Application Summary Dashboard** が開きます。このセクションでは、モニタリングされている **すべての** アプリケーションの概要が表示されます。

* Splunk Observability CloudのReal User Monitoring（RUM）Overviewダッシュボードは、実際のユーザーがWebアプリケーションをどのように体験しているかを可視化します。実際のユーザーセッションで発生するブラウザ側のパフォーマンスメトリクス、JavaScriptエラー、ネットワークリクエストの失敗をキャプチャします。ダッシュボードはCore Web Vitals（LCP、INP、CLS）を表示してページ読み込みパフォーマンスを測定し、時系列のエラートレンドを表示し、最近のアラートを表示することで、フロントエンドチームがエンドユーザー体験に影響する問題を特定して解決するために必要なインサイトを提供します。
* 正しいデータを表示していることを確認するために、自分のストアにフィルタリングして、以降のモジュールが自分の環境に焦点を当てるようにします。
* フィルターを以下のように設定します **(2)**
  * **Time frame** を **-15m** に設定します。
  * **Environment** で **[NAME OF WORKSHOP]-workshop** を選択します。
  * **App** で **[NAME OF WORKSHOP]-store** を選択します。
  * **Source** を **Browser** に設定します。
* 次に、**Page Views / JavaScript Errors** チャートの上にある **[NAME OF WORKSHOP]-store** **(3)** をクリックします。

![main page](../images/rum-dashboard.png)

{{% /exercise %}}
