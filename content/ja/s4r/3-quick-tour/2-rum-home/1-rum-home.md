---
title: RUM ホームページ
linkTitle: 2.1 RUM ホームページ
weight: 2
---

メインメニューで **RUM** をクリックすると、RUM のメインとなるホーム画面、ランディングページに移動します。このページでは、選択したすべての RUM アプリケーション全体のステータスを一目で確認できることに主眼が置かれています。フルサイズ、あるいは、コンパクトビューのいずれかの形式で表示することができます。

ステータスダッシュボードの表示タイプがいずれの場合でも、RUM ホームページは3つのセクションで構成されています。

![RUM ページ](../images/rum-main.png)

1. **オンボーディングパネル：** Splunk RUM を始めるためのトレーニングビデオとドキュメンテーションへのリンク（画面のスペースが必要な場合は、このパネルを非表示にできます）
2. **フィルターパネル：** 時間枠、環境、アプリケーション、ソースタイプでフィルタリングすることができます
3. **アプリケーションサマリーパネル：** RUM データを送信するすべてのアプリケーションのサマリーが表示されます

{{% notice title="RUM における 環境（Environment）,アプリケーション（App）,ソースタイプ（Source）" style="info" %}}

* Splunk Observability は、RUM トレースの一部として送信される **Environment** タグを使用して、"Production" や "Development" などの異なる環境からのデータを区分します。
* さらに **App** タグによる区分も可能です。これにより、同じ環境で動作する別々のブラウザ/モバイルアプリケーションを区別することができます。
* Splunk RUM はブラウザとモバイルアプリケーションの両方で利用可能であり、**Source** を使用してそれらを区別することができます。このワークショップでは、ブラウザベースの RUM のみを使用します。

{{% /notice %}}

{{% notice title="Exercise" style="green" icon="running" %}}

* 時間枠が **-15m** に設定されていることを確認してください
* ドロップダウンボックスからワークショップの Environment を選択してください。命名規則は **[ワークショップの名前]-workshop** です（これを選択すると、ワークショップの RUM アプリケーションが表示されるはずです）
* **App** を選択します。命名規則は **[ワークショップの名前]-store** です。**Source** は **All** に設定したままにしてください。
* **JavaScript Errors** タイルで *Cannot read properties of undefined (reading 'Prcie')* と表示される **TypeError** エントリをクリックし、詳細を確認してください。エラーが発生したウェブサイトのどの部分か、すぐに見つけることができるはずです。これにより迅速に問題を修正することができます。
* パネルを閉じます。
* 3列目のタイルには **Web Vitals** が表示されています。これはユーザーエクスペリエンスの3つの重要な側面である*ページのローディング*、*対話性*、および*視覚的安定性*に焦点を当てたメトリックです。
{{< tabs >}}
{{% tab title="質問" %}}
**Web Vitals メトリクスに基づいて、現在のウェブサイトのパフォーマンスをどのように評価しますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**Web Vitals メトリクスによれば、サイトの初期ロードはOKで、*良好* と評価できます**
{{% /tab %}}
{{< /tabs >}}

* 最後のタイル、**Most recent detectors** タイルは、アプリケーションでトリガーされたアラートがあるかどうかを表示します。
* アプリケーション名の前の下向き **⌵** 矢印をクリックして、ビューをコンパクトスタイルに切り替えます。このビューでも主要な情報がすべて利用可能です。コンパクトビューの任意の場所をクリックしてフルビューに戻ります。

{{% /notice %}}

{{% notice title="Additional Exercise" style="red" icon="running" %}}

RUM ホームページではフロントエンドの概要をシンプルに確認することができますが、詳細なステータス確認や問題調査が必要になるケースもあるはずです。

フロントエンドの問題特定・原因調査を行う方法は、**[5. Splunk RUM](https://splunk.github.io/observability-workshop/latest/ja/s4r/5-rum/index.html)** を見てみましょう。

お時間がある方は、更にいくつかの機能を確認してみましょう。

* **[ワークショップの名前]-store** をクリックします。詳細なダッシュボードビューが表示されます。
* **UX Metrics**, **Front-end Health**, **Back-end Health**, **Custom Events** というメニュータブをそれぞれ開いてみましょう。
  * それぞれのページで、どんなメトリクスが表示されているか確認してみてください
* **Custom Events** をクリックします。
  * **Custom Events** は、特定の操作（例：カートに商品を追加するボタンを押す、商品詳細ページを開く、など）をイベントとして記録し、集計したものです。

![RUM Dashboard](../images/rum-details-dashboard.png)

{{< tabs >}}
{{% tab title="質問" %}}
**Custom Events として記録された処理で、1分あたりのリクエスト回数が最も多い処理は何ですか？**
{{% /tab %}}
{{% tab title="回答" %}}
***AddToCart*です**
{{% /tab %}}
{{< /tabs >}}

* **Custom Event Requests** のすぐ下の **see all** をクリックします
* **Tag Spotlight** というビューが表示されたはずです
  * Tag Spotlight は取得したテレメトリーデータに含まれるタグ情報ごとの傾向を表示・分析する機能です

![RUM Tag Spotlight](../images/rum-tagspotlight.png)

* **Custom Event Name** というタイルの中で _AddToCart_ という項目を探します。みつけたらクリックして **Add to filter** をクリックしてください
  * これにより、_AddToCart_ 処理だけに注目をして、分析を行うことができます。![RUM Tag Filtering](../images/rum-filtering.png)


{{< tabs >}}
{{% tab title="質問" %}}
**このアプリケーションに対してアクセス元として最も多い国はどこですか？ またそれはどのタイルから分かりますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**アメリカ _(US)_ です。Countryタイルから分かります**
{{% /tab %}}
{{< /tabs >}}

* **User Sessions** をクリックします
* Duration をクリックして、処理時間が長い順に並べ替えます
  * *AddToCart* に該当する処理を実施したユーザーのセッションを確認することができます
* 最も処理時間が長いユーザーセッションの *Session ID* をクリックします
![RUM User Sessions](../images/rum-usersessions.png)
* 画面右上にある **Replay** ボタンを押してみたり、各処理の時間やタグ情報を確認したり、_APM_ というリンクにカーソルを当ててみたりしましょう
![RUM Waterfall](../images/rum-waterfall.png)

{{% /notice %}}

次に、**Splunk Application Performance Monitoring (APM)** をチェックしましょう。