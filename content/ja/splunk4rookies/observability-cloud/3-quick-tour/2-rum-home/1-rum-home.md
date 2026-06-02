---
title: Real User Monitoring Home Page
linkTitle: 2.1 RUM Home Page
weight: 2
---

メインメニューで **Digital Experience** をクリックし、Real User Monitoring の下の **Overview** をクリックすると、RUM のメインホーム画面（ランディングページ）が表示されます。このページの主なコンセプトは、選択したすべての RUM アプリケーションの全体的なステータスを、フルダッシュボードまたはコンパクトビューのいずれかで一目で把握できるようにすることです。

使用するステータスダッシュボードの種類に関係なく、RUM ホームページは 3 つの異なるセクションで構成されています。

![RUM Page](../images/rum-main.png)

1. **Onboarding Pane:** Splunk RUM を使い始めるためのトレーニングビデオやドキュメントへのリンクが表示されます。（画面領域が必要な場合は、このペインを非表示にできます）
2. **Filter Pane:** 時間枠、environment、application、source type でフィルタリングできます。
3. **Application Summary Pane:** RUM データを送信しているすべてのアプリケーションのサマリーが表示されます。

{{% notice title="RUM Environments & Application and Source Type" style="info" %}}

* Splunk Observability は、RUM トレース（Web サイトやモバイルアプリへの操作ごとに作成される）の一部として送信される **environments** タグを使用して、「Production」や「Development」など、異なる環境からのデータを分離します。
* さらに **Applications** タグによって分離することもできます。これにより、同じ環境内で動作する個別のブラウザ／モバイルアプリケーションを区別できます。
* Splunk RUM はブラウザアプリケーションとモバイルアプリケーションの両方で利用可能で、**Source Type** によってそれらを区別できます。ただし、このワークショップではブラウザベースの RUM のみを使用します。

{{% /notice %}}

{{% exercise title="Filter RUM and follow a JS error" %}}

* 時間枠が **-15m** に設定されていることを確認します
* ドロップダウンボックスからワークショップ用の environment を選択します。命名規則は **[NAME OF WORKSHOP]-workshop** です（これを選択することで、ワークショップ用 RUM アプリケーションが確実に表示されます）
* **App** 名を選択します。命名規則は **[NAME OF WORKSHOP]-store** です。**Source** は **All** のままにしてください
* **JavaScript Errors** タイルで、*Cannot read properties of undefined (reading 'Prcie')* と表示されている **TypeError** のエントリーをクリックすると、詳細が表示されます。Web サイトのどの部分でエラーが発生したかが素早く示されており、迅速に修正できることに注目してください。
* ペインを閉じます。
* 3 番目のタイルは **Web Vitals** をレポートします。これはユーザー体験における 3 つの重要な側面、*loading*、*interactivity*、*visual stability* に焦点を当てたメトリクスです。
{{< tabs >}}
{{% tab title="Question" %}}
**Web Vitals** メトリクスに基づいて、このサイトの現在の Web パフォーマンスをどのように評価しますか？
{{% /tab %}}
{{% tab title="Answer" %}}
*Web Vitals* メトリクスによると、サイトの初期ロードは問題なく、*Good* と評価されています
{{% /tab %}}
{{< /tabs >}}

* 最後のタイルである **Most recent detectors** タイルには、アプリケーションに対してアラートがトリガーされたかどうかが表示されます。
* アプリケーション名の前にある下向き **⌵** 矢印をクリックすると、コンパクトスタイルのビューに切り替わります。このビューでも主要な情報がすべて利用できることを確認してください。コンパクトビュー内の任意の場所をクリックすると、フルビューに戻ります。

{{% /exercise %}}

次は、**Splunk Application Performance Monitoring (APM)** を確認しましょう。
