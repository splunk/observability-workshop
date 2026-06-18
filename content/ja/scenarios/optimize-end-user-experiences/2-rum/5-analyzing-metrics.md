---
title: RUM メトリクスの分析
linkTitle: 5. RUM メトリクスの分析
weight: 5
---

* RUM UI で RUM メトリクスとセッション情報を確認します
* RUM & APM UI で相関する APM トレースを確認します

---

## 1. RUM Overview Pages

RUM Application Summary Dashboard から、右側の三点メニュー ![trippleburger](../images/trippleburger.png?classes=inline&height=25px) で *Open Application Overview* を選択するか、アプリケーション名のリンク（以下の例では *jmcj-rum-app*）をクリックして、Application Overview Page を開くことで詳細情報を確認できます。

![RUM-SummaryHeader](../images/summaryHeader.png)

これにより、以下に示す RUM Application Overview Page 画面に移動します。

![RUM app overview with UX metrics](../images/rum-ux-metrics.png)

## 2. RUM Browser Overview

### 2.1. Header

RUM UI は5つの主要セクションで構成されています。最初のセクションは選択ヘッダーで、いくつかのオプションを設定/フィルタリングできます

* 確認する時間枠のドロップダウン（この場合、過去15分間を表示しています）
* 比較ウィンドウを選択するドロップダウン（ローリングウィンドウで現在のパフォーマンスを比較しています - この場合、1時間前と比較）
* 利用可能な Environment を表示するドロップダウン
* 各種 Web アプリのドロップダウンリスト
* ***オプション*** Browser または Mobile メトリクスを選択するドロップダウン（*ワークショップでは利用できない場合があります*）

![RUM-Header](../images/rum-header.png)

### 2.2. UX Metrics

デフォルトでは、RUM はエンドユーザーの体験を最も直接的に反映するメトリクスを優先的に表示します。

{{% notice title="Additional Tags" style="info" %}}
すべてのダッシュボードチャートでは、時間の経過に伴うトレンドの比較、ディテクターの作成、クリックスルーによる問題の詳細な診断が可能です。
{{% /notice %}}

まず、ページロードとルート変更の情報が表示されます。これにより、予期しない何かがユーザートラフィックのトレンドに影響を与えているかどうかを把握できます。

![Page load and route change charts](../images/page-load-route-change.png)

次に、Google は読み込み、インタラクティビティ、視覚的安定性によって測定されるユーザー体験を定量化するために Core Web Vitals を定義しています。Splunk RUM は Google のしきい値を UI に組み込んでいるため、メトリクスが許容範囲内にあるかどうかを簡単に確認できます。

![Core Web Vitals charts](../images/core-web-vitals-overview.png)

* **Largest Contentful Paint (LCP)** は、読み込みパフォーマンスを測定します。ビューポート内の最大のコンテンツブロックが読み込まれるまでにどのくらいの時間がかかるでしょうか？良好なユーザー体験を提供するために、LCP はページの読み込み開始から2.5秒以内に発生する必要があります。
* **First Input Delay (FID)** は、インタラクティビティを測定します。アプリを操作できるようになるまでにどのくらいの時間がかかるでしょうか？良好なユーザー体験を提供するために、ページの FID は100ミリ秒以下である必要があります。
* **Cumulative Layout Shift (CLS)** は、視覚的安定性を測定します。初期読み込み後にコンテンツがどの程度移動するでしょうか？良好なユーザー体験を提供するために、ページの CLS は0.1以下を維持する必要があります。

Web Vitals の改善はエンドユーザー体験の最適化における重要な要素であるため、これらを素早く理解し、しきい値を超えた場合にディテクターを作成できることが非常に重要です。

さらに詳しく学びたい場合は、Google が優れたリソースを提供しています。例えば [the business impact of Core Web Vitals](https://web.dev/case-studies/vitals-business-impact) をご覧ください。

### 2.3. Front-end health

フロントエンドの問題の一般的な原因は JavaScript エラーとロングタスクであり、特にインタラクティビティに影響を与える可能性があります。これらのインジケーターにディテクターを作成することで、ユーザーから報告される前にインタラクティビティの問題を調査でき、必要に応じてワークアラウンドの構築や関連リリースのロールバックをより迅速に行うことができます。エンドユーザー体験を向上させるための[ロングタスクの最適化](https://web.dev/articles/optimize-long-tasks)について詳しく学びましょう！

![JS error charts](../images/rum-js-errors.png)
![Long task charts](../images/rum-long-tasks.png)

### 2.4. Back-end health

ユーザー体験に影響を与える一般的なバックエンドの問題は、ネットワークの問題とリソースリクエストです。この例では、Time To First Byte のスパイクがリソースリクエストのスパイクと一致していることが明確に確認でき、調査を始める良い出発点がすでにあります。

![Back-end health charts](../images/rum-be-health.png)

* **Time To First Byte (TTFB)** は、クライアントのブラウザがサーバーからのレスポンスの最初のバイトを受信するまでにかかる時間を測定します。サーバーがリクエストを処理してレスポンスを送信するのに時間がかかるほど、訪問者のブラウザがページを表示するのが遅くなります。

<!-- in progress
### 2.5. Custom Events

The Custom Events tab is where you will find the metrics for any event you may have added yourself to the web pages you are monitoring. See the docs for an [example scenario instrumenting Custom Events for RUM](https://docs.splunk.com/observability/en/rum/rum-scenario-library/spa-custom-event.html#create-a-custom-event-to-measure-user-engagement-on-blog-posts).

As we have seen in the RUM enabled website, we have added the following two lines:

```javascript
const Provider = SplunkRum.provider;
var tracer=Provider.getTracer('appModuleLoader');
```

These lines  will automatically create custom Events for every new Page, and you can also add these to pieces of custom code that are not part of a framework or an event you created so you can better understand the flow though your application. We support **Custom Event Requests**, **Custom Event Error Rates** and **Custom Event Latency** metrics.

![RUM custom event charts](../../images/rum-custom-events.png)
-->
