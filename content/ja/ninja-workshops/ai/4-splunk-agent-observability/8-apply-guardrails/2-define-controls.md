---
title: コンソールでコントロールを定義する
linkTitle: 2. コンソールでコントロールを定義する
weight: 2
time: 7 minutes
---

{{% notice style="warning" title="TODO" %}}
ワークショップで使用する組織を確認してください。
{{% /notice %}}

アプリは制御可能なステップを *登録* しましたが、*ルールを定義* するのはGalileoコンソールです。どのステップを管理するか、どの条件でトリガーするか、一致した場合にブロックするかステアリングするかを設定します。

{{< exercise title="Galileoでコントロールを定義する" >}}

{{< step title="Controls タブを開く" >}}

<!-- PLACEHOLDER UI NAVIGATION: replace with exact console steps + screenshot once finalized -->

Galileoコンソール（`https://console.multitenant.galileocloud.io`、 **`workshop`** org）で、プロジェクト / **`default`** log streamを開き、 **Controls** タブをクリックします。

![Log Stream Controls](../../images/galileo-log-stream-controls.png?width=750px)

{{< /step >}}

{{< step title="エージェントにコントロールを追加する" >}}

`Add control` ボタンをクリックして、log streamにコントロールを追加します。
log streamにクローンしてアタッチできるコントロールのリストと、新しいコントロールを作成するオプションが表示されます。

![Log Stream Add Controls](../../images/galileo-log-stream-add-controls.png?width=750px)

{{< /step >}}

{{< step title="Block Harmful SQL コントロールを追加する" >}}

次に、既存のコントロール `Block-harmful-sql` をlog streamに追加します。
`Block-harmful-sql` コントロールの横にある `Clone and attach` ボタンをクリックします。

![Create a blocking control](../../images/galileo-agent-control-block.png?width=750px)

コントロール名をクリックして、コントロールの詳細を確認します。

![Block Control Details](../../images/galileo-block-control-details.png?width=750px)

このコントロールは、すべての `DELETE` SQL操作を検出してブロックするために使用されます。関連するツール呼び出しの **前に** 実行され、エージェントが実行時に患者レコードを削除することを防ぎます。

`Discard Edits` をクリックして、log streamのコントロールリストに戻ります。

{{< /step >}}

{{< step title="LLMをステアリングするコントロールを作成する" >}}

次に、 **Healthcare Assistant** LLMステップを対象とする2つ目のコントロールを追加します。このコントロールはレスポンスを **ステアリング** し、例えば回答をヘルスケアの範囲内に保つか、免責事項を強制します。

`Add control` ボタンをクリックし、 `steer-output-pii` コントロールの横にある `Clone and attach` をクリックします。

コントロールが追加されたら、クリックして詳細を確認します。

![Create a steering control](../../images/galileo-agent-control-steer.png?width=750px)

このコントロールはLLM呼び出しの **後に** 実行され、LLMレスポンスに電話番号や住所が検出された場合、エージェントは最終レスポンスからこれらのフィールドを削除するように「ステアリング」されます。

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

コンソール内のステップ名（`delete_patient_record`、`Healthcare Assistant`）はどこから来ていますか？

{{< details summary="ここをクリックして回答を確認" >}}
アプリケーションコードから来ています。`@control(step_name=...)` デコレータ（LLMステップは `LLM_STEP_NAME = "Healthcare Assistant"`）とツールステップの登録です。アプリは起動時にこれらのステップをAgent Controlに登録するため、コンソールに表示されルールの対象として設定できます。
{{< /details >}}
