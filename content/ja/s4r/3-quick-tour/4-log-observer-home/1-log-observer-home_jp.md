---
title: Log Observer Home Page
linkTitle: 4.1 Log Observer Home Page
weight: 2
---

メインメニューで **Log Observer** をクリックすると、Log Observerホームページが4つの異なるセクションで構成されます：

![Lo Page](../images/log-observer-main.png)

1. **オンボーディングパネル:** Splunk Log Observerを始めるためのトレーニングビデオとドキュメンテーションへのリンク。
2. **フィルターバー:** 時間、インデックス、およびフィールドでフィルタリングし、クエリを保存することもできます。
3. **ログテーブルパネル:** 現在のフィルタ条件に一致するログエントリのリスト。
4. **フィールドパネル:** 現在選択されているインデックスで使用可能なフィールドのリスト。

{{% notice title="Splunkインデックス" style="info" %}}

一般的に、Splunkでは「インデックス」はデータが保存される指定された場所を指します。これはデータのためのフォルダまたはコンテナのようなものです。 Splunkインデックス内のデータは検索と分析が容易になるように整理され構造化されています。異なるインデックスを作成して特定のタイプのデータを格納することができます。たとえば、Webサーバーログ用の1つのインデックス、アプリケーションログ用の別のインデックスなどが考えられます。

{{% /notice %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}

以前にSplunk EnterpriseまたはSplunk Cloudを使用したことがある場合、おそらくログから調査を開始することに慣れているでしょう。次の演習でも同じようにできますが、このワークショップでは調査にすべての **OpenTelemetry** シグナルを使用します。

{{% /notice %}}

さて、小さな検索演習を行いましょう：

{{% notice title="演習" style="green" icon="running" %}}

* 時間枠を **-15分** に設定します。
* フィルターバーで {{% button style="gray" %}}フィルターの追加{{% /button %}} をクリックし、次にダイアログで **Fields** をクリックします。
* **cardType** と入力して選択します。
* **Top values** の下で **visa** をクリックし、その後 **=** をクリックしてフィルターに追加します。

  ![logo search](../images/log-filter-bar.png?width=920px)

* ログテーブル内のログエントリの1つをクリックして、そのエントリに `cardType: "visa"` が含まれていることを確認します。
* 出荷されたすべての注文を見つけましょう。フィルターバーで **Clear All** をクリックして前のフィルターを削除します。
* 再度フィルターバーで {{% button style="gray" %}}フィルターの追加{{% /button %}} をクリックし、次に **Keyword** を選択します。次に **Enter Keyword...** ボックスに `order:` と入力してエンターキーを押します。
* これで「order：」という単語を含むログ行しか表示されなくなります。まだ多くのログ行がありますので、さらにフィルタリングしましょう。
* 別のフィルターを追加します。今度は **Fields** ボックスを選択し、**Find a field...** 検索ボックスに `severity` と入力して選択します。
  ![severity](../images/find-severity.png?width=15vw&classes=left)
* ダイアログボックスの下部にある {{% button style="gray" %}}**Exclude all logs with this fields**{{% /button %}} をクリックしてください。なぜなら、注文ログ行には重要度が割り当てられていないからです。これにより他のログが削除されます。
* まだ画面上部にオンボーディングコンテンツが表示されている場合は、**Exclude all logs with this fields** ボタンを見るためにページをスクロールする必要があります。
* これで過去15分間に販売された注文のリストが表示されます。

{{% /notice %}}

次に、**Splunk Synthetics** を確認しましょう。
