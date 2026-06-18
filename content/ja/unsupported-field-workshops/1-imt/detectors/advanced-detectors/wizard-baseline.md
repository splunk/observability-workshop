---
title: Historical Anomaly Detector
linkTitle: 4.2.1 Historical Anomaly with Detector Wizard
weight: 3
---

## 目的

Detector Wizard を使用して Historical Anomaly（過去の基準値に基づく異常検知）ディテクターを作成し、生成されるアラートメッセージを確認します。

---

## ステップ 1 – Detector の作成

以下に移動します

**Alerts & Detectors → {{% button style="blue" %}}Create Detector{{% /button %}} → Custom Detector**

提案されたディテクター名の前に**自分のイニシャルを追加**してください。

{{% notice title="ディテクターの命名" style="info" %}}
提案されたディテクター名の前にイニシャルを追加することが重要です。

例**XYZ's Advanced Detector** のようにしてください。
{{% /notice %}}

{{% button style="blue" %}}Create Alert Rule{{% /button %}}

アラートシグナルで以下を設定します

- **Signal (A):** `system.cpu.utilization`

{{% button style="blue" %}}Add Filter{{% /button %}}

- **Filter:** `deployment.environment : astronomy-shop`

{{% button style="blue" %}}Proceed to Alert Condition{{% /button %}} をクリックし、Historical Anomaly を選択してから

{{% button style="blue" %}}Proceed to Alert Settings{{% /button %}} をクリックします

- **Cycle length:** `1d`
- **Alert when:** `Too high`
- **Trigger Sensitivity:** `High`

詳細設定を表示して確認します

{{% button style="blue" %}}Proceed to Alert Message{{% /button %}} をクリックします。

---

## ステップ 2 – デフォルトのアラートメッセージを確認する

Message Preview の下で、**Customize** をクリックして生成されたメッセージを確認します

```handlebars
{{#if anomalous}}
 Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" triggered at {{timestamp}}.
{{else}}
 Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" cleared at {{timestamp}}.
{{/if}}

{{#if anomalous}}
Triggering condition: {{{readableRule}}}
{{/if}}

Mean value of signal in the last {{event_annotations.current_window}}: {{inputs.summary.value}}
{{#if anomalous}}Trigger threshold: {{inputs.fire_top.value}}
{{else}}Clear threshold: {{inputs.clear_top.value}}.
{{/if}}

{{#notEmpty dimensions}}
Signal details:
{{{dimensions}}}
{{/notEmpty}}

{{#if anomalous}}
{{#if runbookUrl}}Runbook: {{{runbookUrl}}}{{/if}}
{{#if tip}}Tip: {{{tip}}}{{/if}}
{{/if}}

{{#if detectorTags}}Tags: {{detectorTags}}{{/if}}

{{#if detectorTeams}}
Teams:{{#each detectorTeams}} {{name}}{{#unless @last}},{{/unless}}{{/each}}.
{{/if}}
```

---

### このメッセージの動作

このメッセージは条件ブロックを使用して、ディテクターがトリガー中かクリア中かに応じて異なるコンテンツをレンダリングします。

- `{{#if anomalous}}` はディテクターが発火しているときのみコンテンツをレンダリングします。
- `{{else}}` ブランチはディテクターがクリアしたときにレンダリングされます。

これにより、1つのテンプレートでトリガー通知とクリア通知の両方を処理できます。

---

### アラートメッセージで使用可能な重要な変数

以下の変数が自動的に使用可能です

- `{{ruleName}}` – アラートルールの名前
- `{{detectorName}}` – ディテクターの名前
- `{{timestamp}}` – イベントの発生時刻
- `{{readableRule}}` – 人間が読める形式の発火条件
- `{{event_annotations.current_window}}` – 評価ウィンドウの期間
- `{{inputs.summary.value}}` – 評価ウィンドウの集計メトリクス値
- `{{inputs.fire_top.value}}` – Historical Anomaly のトリガー閾値
- `{{inputs.clear_top.value}}` – Historical Anomaly のクリア閾値
- `{{dimensions}}` – ディメンションのキー/値ペア（host、environment など）
- `{{runbookUrl}}` – 設定されたランブックリンク（設定されている場合）
- `{{tip}}` – 設定されたヒント（設定されている場合）
- `{{detectorTags}}` – ディテクターに割り当てられたタグ
- `{{detectorTeams}}` – 割り当てられたチーム

SignalFlow で公開されたストリームは以下の形式で使用可能です
`{{inputs.<stream_name>.value}}`

{{% button style="blue" %}}Done Editing{{% /button %}} をクリックしてカスタムメッセージを閉じます。

{{% button style="blue" %}}Proceed to Alert Recipients{{% /button %}} をクリックし、何も選択しないでください。このシナリオでは実際に通知を送信する必要はありません。

{{% button style="blue" %}}Proceed to Alert Activation{{% /button %}}

{{% button style="blue" %}}Activate Alert Rule{{% /button %}}

Missing Alert Notification Policy について確認を求められたら、{{% button style="blue" %}}Save{{% /button %}} を選択してください。
