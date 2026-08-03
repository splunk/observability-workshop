---
title: RUM Overview
linkTitle: 1. RUM Overview
weight: 1
time: 5 minutes
---

この演習では、RUM Overviewダッシュボードを開きます。ここで表示されるデータは生成されたものであり、あなた自身を含むすべての参加者のデータも含まれています。これは、先ほどAstronomy Shopで全員が行ったブラウジングやショッピングをキャプチャしたもので、ページビュー、エラー、読み込みパフォーマンスなどの実際のユーザーメトリクスとして表示されます。Real User Monitoringのレンズを通して自分自身のセッションを確認する機会です。

{{% exercise title="ストアでフィルタリング" %}}

* Splunk Observability Cloudのメインメニューから **Digital Experience** にカーソルを合わせ、以下に示すように **Real User Monitoring** セクションの **Overview** **(1)** をクリックします。

![RUM](../images/rum-de.png)

* Application Summary Dashboardが開き、すべての監視対象アプリケーションの概要が表示されます。

* Splunk Observability CloudのReal User Monitoring（RUM）Overviewダッシュボードは、実際のユーザーがWebアプリケーションをどのように体験しているかを示します。実際のユーザーセッションからブラウザ側のパフォーマンスメトリクス、JavaScriptエラー、失敗したネットワークリクエストをキャプチャします。ダッシュボードにはCore Web Vitals（LCP、INP、CLS）、エラーの傾向、最近のアラートも表示されます。これらのインサイトにより、フロントエンドチームはエンドユーザー体験に影響を与える問題を特定し解決できます。

{{< notice tip >}}
スクリーンショットに表示されているワークショップの名前は **workshop** です。そのため、スクリーンショットではアプリケーション名の例として **workshop-store** を使用しています。手順に従う際は、以下の説明に従い、[NAME OF WORKSHOP]をあなたのワークショップに割り当てられた名前に置き換えてください。
{{< /notice >}}

* 正しいデータを表示していることを確認するために、ダッシュボードをフィルタリングして自分のワークショップ環境のみを表示します。このモジュールの残りの部分では、自分のストアに焦点を当てます。

* フィルタを以下のように設定してください **(2)**
  * **Time frame** を **-15m** に設定します。
  * **Environment** で **[NAME OF WORKSHOP]-workshop** を選択します。
  * **App** で **[NAME OF WORKSHOP]-store** を選択します。
  * **Source** を **Browser** に設定します。

* 次に、**Page Views / JavaScript Errors** チャートの上にある **[NAME OF WORKSHOP]-store** **(3)** をクリックします。

![main page](../images/rum-dashboard.png)

{{% /exercise %}}
