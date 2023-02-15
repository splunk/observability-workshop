---
title: 6. RUMメトリクスの分析
linkTitle: 6. RUMメトリクスの分析
weight: 6
isCJKLanguage: true
---

* RUM UIでRUMメトリクスとセッション情報を見る
* RUM & APM UIで相関するAPMトレースを見る

---

## 1. RUM Overview Pages

RUM Application Summaryダッシュボードの右側のトリプルドット ![trippleburger](../images/trippleburger.png) メニューから *Open Application Overview* を選択するか、アプリケーション名のリンク（以下の例では *jmcj-rum-app* ）をクリックして Application Overviewページを開き、詳細情報を確認することができます。

![RUM-SummaryHeader](../images/summaryHeader.png)

以下のような RUM Application Overview ページが表示されます。

![RUM-1](../images/RUM-1.png)

## 2. RUM Browserの概要

### 2.1. ヘッダー

RUMのUIは、大きく6つのセクションで構成されています。一つ目は選択ヘッダーで、多くのオプションを設定/フィルタリングすることができます。

* レビューする時間ウィンドウを選択するドロップダウン（この場合は過去15分）。
* 比較ウィンドウを選択するためのドロップダウン（現在のパフォーマンスをローリングウィンドウで比較します - この場合は1時間前と比較）。
* Environmentを選択するドロップダウン (ワークショップ講師が提供するもの、またはこの例のように *All* を選択）。
* 様々なWebアプリのドロップダウン（ワークショップ講師が提供するものか、 *All* を使用）。
* ***オプション*** ブラウザまたはモバイルメトリクスを選択するドロップダウン（*ワークショップでは恐らく利用できません*)
![RUM-Header](../images/RUM-Header.png)

### 2.2. 概要ペイン

ページの左側にある概要ペインでは、ロード時間が長くなったページの概要を確認することができます。

この例では **checkout** と **cart** ページに黄色の三角形でエラーを示しており、ロード時間が 2.38 秒から 5.50 秒に増加したことがわかります。

<!-- ![RUM-Top](../images/RUM-TOP.png) -->

![RUM-Top](../images/RUM-Page-Load-Times.png)

また、1分あたりのFrontend ErrorとBackend Errorsの件数の概要が表示され、このサイトでは3種類のJavaScriptエラーが発生していることが分かります。

![RUM-Top](../images/RUM-JS-Errors.png)

最後の2つのペインでは、**Top Page Views** と **Top Network Requests** が表示されます。

![RUM-Top](../images/RUM-Page-Views-Network.png)

### 2.3. Key Metricsペイン

Key Metricsペインでは、毎分の **JavaScript Errors** と **Network Errors** の件数、また **Backend/Resource Request Duration** を確認できます。これらのメトリクスはサイトで問題が発生した場合に、発生個所を特定するのに非常に便利です。

![RUM-KeyMetrics](../images/RUM-Key-Metrics.png)

### 2.4. Web Vitalsペイン

Web Vitalsペインは、Web Vitalのメトリクスに基づいてエンドユーザーに提供しているエクスペリエンスに関する洞察を得たい場合に使用する場所です。
Web Vitalは、ウェブ上で優れたユーザーエクスペリエンスを提供するために不可欠な品質シグナルの統一ガイダンスを提供するGoogleのイニシアチブであり、3つの主要なパラメーターに焦点を当てています。

* **Largest Contentful Paint (LCP)** （最大コンテンツの描画）：読み込みのパフォーマンスを測定するものです。良いユーザーエクスペリエンスを提供するために、LCPはページが読み込まれてから2.5秒以内に発生する必要があります。
* **First Input Delay (FID)** （初回入力までの遅延時間）：インタラクティブ性を評価するものです。良いユーザーエクスペリエンスを提供するために、ページのFIDは100ミリ秒以下であるべきです。
* **Cumulative Layout Shift (CLS)** （累積レイアウトシフト数）：視覚的な安定性を測定します。良いユーザーエクスペリエンスを提供するためには、CLSを 0.1 以下で維持する必要があります。

![RUM-WebVitals](../images/RUM-Web-Vitals.png)

### 2.5. Other Metricsペイン

Other Metricsペインでは、ページの初期ロード時間や完了までに時間がかかりすぎているタスクなどを中心に、その他のパフォーマンスメトリクスを確認することができます。

* **Time To First Byte (TTFB)** ：クライアントのブラウザーがサーバーからレスポンスの最初のバイトを受信するまでの時間を測定します。サーバーがリクエストを処理し、レスポンスを送信するまでの時間が長いほど、訪問者のブラウザーがページを表示する際の速度が遅くなります。
* **Long Task Duration** ：開発者がユーザーエクスペリエンス悪化を理解するために使用できるパフォーマンスメトリクスであり、問題の兆候である可能性もあります。
* **Long Task Count** ：長いタスクの発生頻度を示すメトリクスで、これもユーザーエクスペリエンスの調査や問題の検出に使用されます。

![RUM-Other](../images/RUM-Other.png)

### 2.6. Custom Eventペイン

Custom Eventペインでは、監視しているウェブページに自分で追加したイベントのメトリクスが表示されます。

RUMを有効化したサイトで見れるように、以下の2行を追加しています。

```javascript
const Provider = SplunkRum.provider;
var tracer=Provider.getTracer('appModuleLoader');
```

これらの行は、すべての新しいページに対して自動的にカスタムイベントを作成します。また、フレームワークや作成したイベントの一部ではないカスタムコードにこれらを追加することで、アプリケーションのフローをより良く理解することができます。
**Custom Event Requests** 、 **Custom Event Error Rates** 、 **Custom Event Latency** をサポートしています。

![RUM-CustomMetrics](../images/RUM-Custom-Events.png)
