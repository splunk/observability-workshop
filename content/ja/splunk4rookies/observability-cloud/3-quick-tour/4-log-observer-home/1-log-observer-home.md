---
title: Log Observerホームページ
linkTitle: 4.1 Log Observerホームページ
weight: 2
---

メインメニューの**Log Observer**をクリックすると、Log Observer ホームページが表示されます。Log Observer ホームページは 4 つの明確なセクションで構成されています：

![LOページ](../images/log-observer-main.png)

1. **オンボーディングペイン:** SplunkLog Observer の使用を開始するためのトレーニングビデオとドキュメントへのリンク。
2. **フィルターバー:** 時間、インデックス、フィールドでフィルタリングし、クエリを保存することもできます。
3. **ログテーブルペイン:** 現在のフィルター条件に一致するログエントリのリスト。
4. **フィールドペイン:** 現在選択されているインデックスで利用可能なフィールドのリスト。

{{% notice title="Splunk Index" style="info" %}}

一般的に、Splunk では、「Index」はデータが保存される指定された場所を指します。これはデータのフォルダやコンテナのようなものです。Splunk では、「Index」はデータが保存される指定された場所を指します。これはデータのフォルダやコンテナのようなものです。Splunk 内のデータは、検索や分析が容易になるように整理され構造化されています。特定のタイプのデータを保存するために異なるインデックスを作成できます。たとえば、Web サーバーログ用のインデックス、アプリケーションログ用の別のインデックスなどがあります。

{{% /notice %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}

以前に Splunk Enterprise または Splunk Cloud を使用したことがある場合は、おそらくログから調査を開始することに慣れているでしょう。以下の演習で見るように、Splunk Observability Cloud でも同様のことができます。ただし、このワークショップでは、調査に**OpenTelemetry**のすべてのシグナルを使用します。

{{% /notice %}}

簡単な検索演習を行いましょう：

{{% notice title="演習" style="green" icon="running" %}}

- 時間枠を **-15m** に設定します。
- フィルターバーで{{% button style="gray" %}}Add Filter{{% /button %}}をクリックし、ダイアログで**Field**をクリックします。
- **cardType**と入力して選択します。
- **トップ値**の下で**visa**をクリックし、次に **=** をクリックしてフィルターに追加します。

  ![ロゴ検索](../images/log-filter-bar.png?width=920px)

- ログテーブルのログエントリの 1 つをクリックして、エントリに`cardType: "visa"`が含まれていることを確認します。
- 出荷されたすべての注文を見つけましょう。フィルターバーの**Clear All**をクリックして、前のフィルターを削除します。
- フィルターバーで再び{{% button style="gray" %}}Add Filter{{% /button %}}をクリックし、**キーワード**を選択します。次に**キーワードを入力...**ボックスに`order:`と入力し、Enter キーを押します。
- これで「order:」という単語を含むログ行のみが表示されるはずです。まだたくさんのログ行があるので、さらにフィルタリングしましょう。
- 別のフィルターを追加します。今回は**Field**ボックスを選択し、**Find a field ...** 検索ボックスに`severity`と入力して選択します。
  ![重要度](../images/find-severity.png?width=15vw&classes=left)
- 注文ログ行には重要度が割り当てられていないため、ダイアログボックスの下部にある{{% button style="gray" %}}**Exclude all logs with this field**{{% /button %}}をクリックしてください。これにより、他のログが削除されます。
- 上部にオンボーディングコンテンツがまだ表示されている場合は、**Exclude all logs with this field**ボタンを見るためにページを下にスクロールする必要があるかもしれません。
- これで、過去 15 分間に販売された注文のリストが表示されるはずです。

{{% /notice %}}

次に、**Splunk Synthetics**を確認しましょう。
