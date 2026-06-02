---
title: RUM の概要
linkTitle: 1. RUM の概要
weight: 1
time: 5 minutes
---

{{% exercise title="自分のストアでフィルタリングする" %}}

* Splunk Observability Cloud のメインメニューで **Digital Experience** にカーソルを合わせ、下図のように **Real User Monitoring** セクションの **Overview** **(1)** をクリックします。

![RUM](../images/rum-de.png)

* これにより **Application Summary Dashboard** が開きます。このセクションでは、監視対象の **すべての** アプリケーションの概要を一目で確認できます。

* Splunk Observability Cloud の Real User Monitoring (RUM) Overview ダッシュボードは、実際のユーザーが Web アプリケーションをどのように体験しているかを可視化します。実際のユーザーセッションで発生するブラウザ側のパフォーマンスメトリクス、JavaScript エラー、ネットワークリクエストの失敗をキャプチャします。ダッシュボードはページロードのパフォーマンスを測定する Core Web Vitals (LCP、INP、CLS) を表示し、エラーの推移を時系列で示すとともに、最近のアラートも表示します。これにより、フロントエンドチームはエンドユーザー体験に影響を与える問題を特定し解決するために必要なインサイトを得られます。

* 適切なデータを参照していることを確認するため、以下の設定 **(2)** を確認してください:
  * **Time frame** が **-15m** に設定されている。
  * **Environment** に **[NAME OF WORKSHOP]-workshop** が選択されている。
  * **App** に **[NAME OF WORKSHOP]-store** が選択されている。
  * **Source** が **Browser** に設定されている。
* 次に、**Page Views / JavaScript Errors** チャートの上にある **[NAME OF WORKSHOP]-store** **(3)** をクリックします。

![main page](../images/rum-dashboard.png)

{{% /exercise %}}
