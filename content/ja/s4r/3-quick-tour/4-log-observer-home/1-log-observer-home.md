---
title: Log Observer ホームページ
linkTitle: 4.1 Log Observer ホームページ
weight: 2
---

メインメニューで **Log Observer** をクリックしてみましょう。Log Observer ホームページは4つのセクションで構成されます。

![Lo Page](../images/log-observer-main.png)

1. **オンボーディングパネル:** Splunk Log Observer を始めるためのトレーニングビデオとドキュメンテーションへのリンク。
2. **フィルターパネル:** 時間枠、index、および Field に基づいてログをフィルタリングすることができます。また、事前に保存しておいたクエリを利用することもできます。
3. **Log table:** 現在のフィルタ条件に一致するログエントリーのリスト。
4. **Fields:** 現在選択されている index で使用可能なフィールドのリスト。

{{% notice title="Splunk index" style="info" %}}

一般的に、Splunk では「index」はデータが保存される指定された場所を指します。これはデータを格納するフォルダまたはコンテナのようなものです。 Splunk index 内のデータは検索と分析が容易になるように整理され構造化されています。異なるインデックスを作成して特定のタイプのデータを格納することができます。たとえば、Web サーバーログ用に1つの index、アプリケーションログ用に別の index を作成しておくようなことが可能です。

{{% /notice %}}

{{% notice title="Tip" style="primary" icon="lightbulb" %}}

これまでに Splunk Enterprise または Splunk Cloud を使用したことがある場合、おそらくログから調査を開始することに慣れているでしょう。このあとの Exercise でも同じように取り組むことは可能ですが、このワークショップでは調査にあたってすべての **OpenTelemetry** シグナルを使用していきます。

{{% /notice %}}

さて、簡単なログ検索の演習を行いましょう。

{{% notice title="Exercise" style="green" icon="running" %}}

まず、`visa` を使用した注文を検索してみます。

* 時間枠を **-15分** に設定してください
* Filter で {{% button style="gray" %}}Add Filter{{% /button %}} をクリックし、次にダイアログで **Fields** をクリックしてください。
* **cardType** と入力して選択してください
* **Top values** の下にある **visa** をクリックし、その後 **=** をクリックしてフィルターに追加しましょう。

  ![logo search](../images/log-filter-bar.png?width=920px)

* ログテーブル内のログエントリの1つをクリックして、そのエントリに `cardType: "visa"` が含まれていることを確認してください。

今度は出荷されたすべての注文を探してみましょう。

* Filter で **Clear All** をクリックして前のフィルターを削除してください。
* 再度 Filter で {{% button style="gray" %}}Add Filter{{% /button %}} をクリックし、次に **Keyword** を選択します。次に **Enter Keyword...** ボックスに `order:` と入力してエンターキーを押してください。
* これで `order:` という単語を含むログ行しか表示されなくなります。まだ多くのログ行がありますので、さらにフィルタリングしていきましょう。
* 別のフィルターを追加します。今度は **Fields** ボックスを選択し、**Find a field...** と表示されている検索ボックスに `severity` と入力して選択してください。
  ![severity](../images/find-severity.png?width=15vw&classes=left)
* ダイアログボックスの下部にある {{% button style="gray" %}}**Exclude all logs with this fields**{{% /button %}} をクリックしてください。注文ログ行には `severity` が割り当てられていないため、これにより不要なログ行を除外することができます。
* 画面上部にオンボーディングコンテンツが表示されている場合は、**Exclude all logs with this fields** ボタンを押すためにページをスクロールする必要があるかもしれません。
* これで過去15分間に販売された注文のリストが表示されたはずです。

{{% /notice %}}

次に、**Splunk Synthetics** を確認しましょう。
