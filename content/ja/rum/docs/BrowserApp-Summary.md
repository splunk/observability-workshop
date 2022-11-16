---
title: ブラウザーアプリケーションの健全性を一目で確認
linkTitle: ブラウザーアプリケーションの健全性を一目で確認
weight: 2
isCJKLanguage: true
---

* ランディングページで利用できるUIとオプションに慣れる
* ページビュー/エラー、リクエスト/エラー、およびJavaScriptエラーを1つのビューで識別しする</br>
  Web Vitalメトリクスと、ブラウザーアプリケーションに関連して発生したディテクターを確認する

---

## 1. Application Summary ダッシュボードの概要

### 1.1. ヘッダーバー

前のセクションで見たように、RUM Application Summary ダッシュボードは5つの主要セクションで構成されています</br>。
最初のセクションは選択ヘッダーで、 ![RUM-browser](../../images/browser.png) ブラウザーアイコンまたはアプリケーション名の前の **>** を使用してペインを折りたたむことができます。また、アプリケーション名(下の例では *jmcj-rum-app* )のリンクをクリックすると、*Application Overview* ページにアクセスできます。

また、右側のトリプルドット ![trippleburger](../../images/trippleburger.png) メニューから、 *Application Overview* や *App Health ダッシュボード* を開くことができます。

![RUM-SummaryHeader](../../images/summaryHeader.png)

まず *View Dashboard* リンクをクリックし Browser App Health ダッシュボード を開きます（別タブで開かれます）。 次に元のRUMタブに戻り *Open Application Overview* リンクか、アプリの名前をクリックして、Application Overview ダッシュボードを開きます。

*Application Overview* と *Browser App Health* ダッシュボードを次のセクションで詳しく見ていきます。

## 2. Application Overview

RUM Application Overview ダッシュボードでは *一目で* アプリケーションの状態の概要を確認できます。

### 2.1. Page Views / Network Requests / Errors

最初セクションに表示されている *Page Views / Errors* と *Network Requests and Errors* チャートはアプリケーション内のリクエスト数と問題の傾向を示しています。 これは、Javascriptのエラーや、バックエンドサービスへのネットワーク呼び出しに失敗した可能性があります。

![RUM-chart](../../images/Rum-chart.png)

上の例では、Networkチャートではネットワーク呼び出しに失敗していないことがわかりますが、Page Viewsチャートでは多くのページで何らかのエラーが発生していることが確認できます。このようなエラーは一般ユーザーからは見えないことが多いのですが、Web サイトのパフォーマンスに重大な影響を与える可能性があります。

チャート上にカーソルをホバーすると Page Views / Network Requests / Errors の件数を確認できます。

![RUM-chart-clicked](../../images/RUM-Chart-Clicked.png)

### 2.2. JavaScript Errors

2番目のセクションでは、アプリケーションで発生したJavaScriptエラーの概要と、各エラーの件数が表示されます。
![RUM-javascript](../../images/RUM-Javascripterrors.png)

上の例では、3種類のJavaScriptエラーがあることがわかります。1つは選択した時間帯に29回発生し、他の2つはそれぞれ12回発生しています。

エラーの一つをクリックすると、ポップアウトが開き、時系列でエラーの概要（下図）が表示されます。また、JavaScript エラーのスタックトレースが表示され、問題が発生した場所を知ることができます（詳細については、次のセクションで説明します）。

![RUM-javascript-chart](../../images/expandedRUmJAVAscript-error.png)

### 2.3. Web Vitals

3番目のセクションでは、Googleがランキングシステムで使用する3つのメトリクスである重要な（Google）Web Vitalsを表示しており、エンドユーザーにとってのサイトの表示速度を非常によく表しています。

![WEB-vitals](../../images/RUM-QuickWebVitals.png)

ご覧の通り、当サイトは3つのメトリクスすべてで *Good* スコアを獲得し、良好な動作をしています。これらのメトリクスは、アプリケーションの変更がもたらす影響を特定し、サイトのパフォーマンスを向上させるために使用することができます。

Web Vitalsペインに表示されているメトリクスをクリックすると、対応する Tag Spotlight ダッシュボードに移動します。例えば **Largest Contentful Paint (LCP)** をクリックすると、以下のスクリーンショットのようなダッシュボードが表示され、このメトリクスのパフォーマンスに関するタイムラインとテーブルビューを見ることができます。これにより、OS やブラウザーのバージョンなど、より一般的な問題の傾向を把握することができます。

![WEB-vitals-tag](../../images/RUM-Tag-Spotlight.png)

### 2.4. Most Recent Detectors

4番目であり最後のセクションでは、アプリケーションでトリガーされたディテクターの概要を表示することにフォーカスしています。このスクリーンショット用にディテクターを作成しているため、皆さんのペインでは何も表示されていないはずです。次のセクションで実際にディテクターを追加し、トリガーされるようにします。

![detectors](../../images/rum-detector.png)

下のスクリーンショットでは、 *RUM Aggregated View Detector* のクリティカルアラートと、選択した時間ウィンドウでこのアラートが何回トリガーされたかを示す件数が表示されています。アラートが表示されている場合は、アラートの名前（青いリンクで表示されている）をクリックすると、アラートの詳細を表示するアラート概要ページに移動します（注意：この操作を行うと、現在のページから離れることになります。）

![alert](../../images/click-alert.png)

---

次のセクションに進む前に、RUM Application Summaryダッシュボードとその基礎となるチャートとダッシュボードを数分間試してみてください。
