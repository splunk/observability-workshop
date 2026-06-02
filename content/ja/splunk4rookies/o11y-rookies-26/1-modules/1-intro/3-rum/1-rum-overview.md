---
title: RUM Overview
linkTitle: 1. RUM Overview
weight: 1
time: 5 minutes
---

{{% exercise title="Filter to your store" %}}

* Splunk Observability Cloud のメインメニューから **Digital Experience** にカーソルを合わせ、下図のように **Real User Monitoring** セクションの **Overview** **(1)** をクリックします。

![RUM](../images/rum-de.png)

* **Application Summary Dashboard** が開きます。このセクションでは、監視対象となっている **すべての** アプリケーションの概要を素早く確認できます。

* Splunk Observability Cloud の Real User Monitoring (RUM) Overview ダッシュボードは、実際のユーザーが Web アプリケーションをどのように体験しているかを可視化します。実際のユーザーセッションで発生するブラウザ側のパフォーマンスメトリクス、JavaScript エラー、ネットワークリクエストの失敗を捕捉します。ダッシュボードでは、ページ読み込みのパフォーマンスを測定するための Core Web Vitals (LCP、INP、CLS) を表示し、エラー傾向の推移や最近のアラートを示します。これにより、フロントエンドチームはエンドユーザー体験に影響する問題を特定して解決するために必要な洞察を得られます。

* 正しいデータを確認するために、以下の設定 **(2)** を確認してください。
  * **Time frame** が **-15m** に設定されていること。
  * 選択されている **Environment** が **[NAME OF WORKSHOP]-workshop** であること。
  * 選択されている **App** が **[NAME OF WORKSHOP]-store** であること。
  * **Source** が **Browser** に設定されていること。
* 次に、**Page Views / JavaScript Errors** チャートの上にある **[NAME OF WORKSHOP]-store** **(3)** をクリックします。

![main page](../images/rum-dashboard.png)

{{% /exercise %}}
