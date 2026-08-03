---
title: トレースの確認
linkTitle: 1. Explore a Trace
weight: 1
time: 5 minutes
---

Splunk Agent Observabilityを開き、先ほど生成したトラフィックから実際のトレースを確認します。

{{< exercise title="エージェントの動作を調査する" >}}

{{< step title="プロジェクトとログストリームを開く" >}}

**1.** ブラウザで `https://console.multitenant.galileocloud.io` のSplunk Agent Observabilityコンソールにアクセスし、 **`workshop`** orgを選択します

**2.** 前のステップで **`GALILEO_PROJECT`** フィールドに設定した名前（例: `project-44`）を使用してプロジェクトを開きます

**3.** `default` ログストリームを選択します

![プロジェクトとログストリームの選択](../../images/galileo-project.png?width=750px)

{{< /step >}}

{{< step title="トレースリストを確認する" >}}

最近のトレースのリストを確認します。送信したメッセージごとに1つのトレースがあります。入力トークン数、出力トークン数、Span数など、一目で確認できる主要なシグナルに注目してください。

![トレースリスト](../../images/galileo-traces.png?width=750px)

{{< /step >}}

{{< step title="トレースを開いてSpanツリーを確認する" >}}

Lisinoprilの用量に関する質問のトレースを開きます。チャットボットノードのネストされた **LLM span** と、`search_medicine_qa`（検索）の **tool span** を含む単一のトレースが表示されます。ツリーを展開して、エージェントのパスをエンドツーエンドで追跡します。

![ネストされたSpanを含むトレース詳細](../../images/galileo-trace-view.png?width=750px)

{{< /step >}}

{{< step title="Spanを検査する" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact span-panel steps + screenshot once finalized -->

**`Healthcare Assistant`** Spanを選択し、 **システムメッセージとユーザーメッセージ** 、 **Available Tools** 、 **Output** 、 **Token Counts** 、 **Latency** 、 **Agent Cost** がキャプチャされていることを確認します。これは、エージェントがなぜそのように回答したかを説明するための詳細情報です。

![Span詳細](../../images/galileo-llm-span.png?width=750px)

{{< /step >}}

{{< step title="Trace Graphを表示する" >}}

次に、 **`Trace graph`** タブをクリックします。このタブは、この特定のインタラクションがシステム全体でどのようにステップごとに実行されたかを視覚的に表示します。

![Trace Graph](../../images/galileo-trace-graph.png?width=750px)

{{< /step >}}

{{< /exercise >}}
