---
title: Browser Application の健全性を一目で確認する
linkTitle: 4. Browser Application Summary
weight: 4
---

* このランディングページで利用可能な UI とオプションに慣れましょう
* Page Views/JavaScript Errors と Request/Errors を単一のビューで確認します</br>
  Web Vitals メトリクスと、Browser Application に関連して発火した Detector を確認します

---

## Application Summary Dashboard

### 1. Header Bar

前のセクションで見たように、RUM Application Summary Dashboard は 5 つの主要セクションで構成されています。</br>
最初のセクションは選択ヘッダーで、![RUM-browser](../images/browser.png?classes=inline&height=25px) Browser アイコンまたはアプリケーション名の前にある **>** をクリックしてペインを折りたたむことができます。以下の例ではアプリケーション名は *jmcj-store* です。また、アプリケーション名のリンク（以下の例では *jmcj-store*）をクリックすると、*Application Overview* ページにアクセスできます。

さらに、右側の三点メニュー ![trippleburger](../images/trippleburger.png?classes=inline&height=25px) から *Application Overview* または *App Health Dashboard* を開くこともできます。

![RUM-SummaryHeader](../images/summaryHeader.png)

ここでは、Application Summary Dashboard で得られる高レベルの情報を見ていきましょう。

RUM Application Summary Dashboard は、アプリケーションの状態を*一目で*把握できるハイライトを提供することに重点を置いています。

### 2. Page Views / JavaScript Errors & Network Requests / Errors

最初のセクションには *Page Views / JavaScript Errors* と *Network Requests and Errors* のチャートが表示され、アプリケーションにおけるこれらの問題の数量とトレンドを示します。これは JavaScript エラーやバックエンドサービスへの失敗したネットワーク呼び出しなどです。

![RUM-chart](../images/Rum-chart.png)

上の例では、Network チャートに失敗したネットワーク呼び出しはありませんが、Page View チャートではいくつかのページでエラーが発生していることがわかります。これらは通常のユーザーには見えないことが多いですが、Web サイトのパフォーマンスに深刻な影響を与える可能性があります。

チャートにカーソルを合わせると、Page Views / Network Requests / Errors の数を確認できます。

![RUM-chart-clicked](../images/RUM-Chart-Clicked.png)

### 3. JavaScript Errors

RUM Application Summary Dashboard の 2 番目のセクションでは、アプリケーションで発生している JavaScript エラーの概要と各エラーの発生回数を表示します。

![RUM-javascript](../images/RUM-Javascripterrors.png)

上の例では、3 つの JavaScript エラーがあり、1 つは選択した時間枠で 29 回発生し、他の 2 つはそれぞれ 12 回発生しています。

エラーの 1 つをクリックすると、ポップアウトが開き、時間の経過に伴うエラーのサマリー（下図）と JavaScript エラーの Stack Trace が表示され、問題が発生した場所を示します。（これについては、後続のセクションでより詳しく見ていきます）

![RUM-javascript-chart](../images/type-error-detail.png)

### 4. Web Vitals

RUM Application Summary Dashboard の次のセクションでは、[Google's Core Web Vitals](https://web.dev/articles/vitals) を表示します。これは Google が検索ランキングシステムで使用するだけでなく、読み込み、インタラクティビティ、視覚的安定性の観点からエンドユーザーエクスペリエンスを定量化する 3 つのメトリクスです。

![WEB-vitals](../images/RUM-QuickWebVitals.png)

ご覧のとおり、私たちのサイトは適切に動作しており、3 つのメトリクスすべてで *Good* のスコアを獲得しています。これらのメトリクスを使用して、アプリケーションへの変更がもたらす影響を特定し、サイトのパフォーマンスを改善するのに役立てることができます。

Web Vitals ペインに表示されているメトリクスのいずれかをクリックすると、対応する Tag Spotlight Dashboard に移動します。例えば、**Largest Contentful Paint (LCP)** のチャートレットをクリックすると、下のスクリーンショットのようなダッシュボードに移動し、このメトリクスのパフォーマンスのタイムラインとテーブルビューが表示されます。これにより、トレンドを把握し、オペレーティングシステム、地理的位置、ブラウザバージョンなど、問題がより多く発生している箇所を特定できます。

![WEB-vitals-tag](../images/RUM-Tag-Spotlight.png)

### 5. Most Recent Detectors

RUM Application Summary Dashboard の最後のセクションでは、アプリケーションに対してトリガーされた最近の Detector の概要を提供します。このスクリーンショットでは Detector を作成していますが、現時点ではペインは空になっています。次のセクションの 1 つで、サイトに Detector を追加し、トリガーされるようにします。

![detectors](../images/rum-detector.png)

スクリーンショットでは、*RUM Aggregated View Detector* のクリティカルアラートと、選択した時間枠でこのアラートがトリガーされた回数が表示されています。アラートが表示されている場合は、アラートの名前（青いリンクとして表示）をクリックすると、アラートの詳細を示す Alert Overview ページに移動します（注意：これにより現在のページから移動します。概要ページに戻るにはブラウザの**戻る**オプションを使用してください）。

![alert](../images/click-alert.png)

---
{{% notice title="演習" style="green" icon="running" %}}
次のセクションに進む前に、数分間 RUM Application Summary Dashboard とその基盤となるチャートやダッシュボードを操作してみてください。
{{% /notice %}}
