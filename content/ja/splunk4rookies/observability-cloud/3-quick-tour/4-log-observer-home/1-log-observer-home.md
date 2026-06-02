---
title: Log Observer Home Page
linkTitle: 4.1 Log Observer Home Page
weight: 2
---

メインメニューの **Logs** をクリックし、続いて **Log Observer** をクリックします。Log Observer のホームページは、4 つのセクションで構成されています。

![Lo Page](../images/log-observer-main.png)

1. **Onboarding Pane:** Splunk Log Observer を使い始めるためのトレーニング動画やドキュメントへのリンクです。
2. **Filter Bar:** 時間、インデックス、フィールドでフィルタリングしたり、クエリーを保存したりできます。
3. **Logs Table Pane:** 現在のフィルター条件に一致するログエントリーの一覧です。
4. **Fields Pane:** 現在選択されているインデックスで利用可能なフィールドの一覧です。

{{% notice title=" Splunkインデックス" style="info" %}}

Splunkにおける「インデックス」とは、一般的にデータが格納されるために指定された場所を指します。データのフォルダーやコンテナーのようなものです。Splunkインデックス内のデータは、検索や分析が容易になるように整理・構造化されています。特定のタイプのデータを格納するために、異なるインデックスを作成できます。たとえば、Webサーバーのログ用に1つのインデックスを用意し、アプリケーションログ用に別のインデックスを用意するといった具合です。

{{% /notice %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}

これまでに Splunk Enterprise や Splunk Cloud を使用したことがある方は、ログから調査を始めることに慣れているかもしれません。次の演習で見ていくように、Splunk Observability Cloud でも同じことができます。ただし、このワークショップでは調査に **OpenTelemetry** シグナルをすべて活用していきます。

{{% /notice %}}

それでは、簡単な検索演習を行ってみましょう。

{{% exercise title="Visaトランザクションに絞ってLog Observerをフィルタリング" %}}

* 時間範囲を **-15m** に設定します。
* フィルターバーの {{% button style="gray" %}}Add Filter{{% /button %}} をクリックし、ダイアログで **Fields** をクリックします。
* **cardType** と入力して選択します。
* **Top values** の下にある **visa** をクリックし、続いて **=** をクリックしてフィルターに追加します。
* {{% button style="blue" %}}Run search{{% /button %}} をクリックします。

  ![logo search](../images/log-filter-bar.png?width=920px)

* Logsテーブル内のログエントリーのいずれかをクリックして、エントリーに `cardType: "visa"` が含まれていることを確認します。
* 次に、出荷されたすべての注文を見つけてみましょう。フィルターバーの **Clear All** をクリックして、前のフィルターを削除します。
* もう一度フィルターバーの {{% button style="gray" %}}Add Filter{{% /button %}} をクリックし、**Keyword** を選択します。続いて **Enter Keyword...** ボックスに `order` と入力し、Enter キーを押します。
* {{% button style="blue" %}}Run search{{% /button %}} をクリックします。
* これで `order` という単語を含むログ行のみが表示されるはずです。それでもまだログ行が多いので、さらにフィルタリングを行いましょう。
* もう1つフィルターを追加します。今回は **Fields** ボックスを選択し、**Find a field ...** 検索ボックスに `severity` と入力して選択します。
  ![severity](../images/find-severity.png?width=15vw&classes=left)
* **Top values** の下にある **error** をクリックし、続いて **=** をクリックしてフィルターに追加します。
* {{% button style="blue" %}}Run search{{% /button %}} をクリックします。
* これで、過去15分間に完了に失敗した注文のリストが表示されるはずです。

{{% /exercise %}}

次は、**Splunk Synthetics** を見ていきましょう。
