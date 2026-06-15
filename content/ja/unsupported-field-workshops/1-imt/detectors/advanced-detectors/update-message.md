---
title: アラートメッセージとアラートルールの更新
linkTitle: 4.2.3 Alert Message and Description
weight: 4
---

## 目的

以下の方法で、複合条件の検出ロジックを正確に反映するようにアラートメッセージをカスタマイズします

- ウィザードで生成されたメッセージが削除された理由の説明
- パブリッシュされたしきい値ストリームの参照
- 履歴異常と静的ガードレールの両方の条件を明示的に伝達

---

## ステップ 1 – Detector の保存

右上の {{% button style="blue" %}}Save{{% /button %}} をクリックします。

---

## ステップ 2 – アラートメッセージの編集

Detector の **Alert Rules** タブに移動します。

既存の Alert Rule の {{% button style="blue" %}}Edit{{% /button %}} をクリックします。

**Alert message** タブを選択し、**Customize** をクリックします。

{{% notice icon="user" style="orange" title="確認" %}}

以前ウィザードで生成されたメッセージ本文が表示されなくなっていることに注目してください。

> SignalFlow で Detector を編集した後、なぜデフォルトのメッセージが消えたのでしょうか？

{{% /notice %}}

{{% notice style="info" title="メッセージが削除された理由" %}}

SignalFlow で Detector を編集した時点で、ウィザードが管理するヘルパー関数の範囲を超えました。

検出ロジックがカスタムストリームと手動で構成された `detect()` ステートメントを使用するようになったため、プラットフォームは以下を安全に推測できなくなりました

- どの条件がアラートをトリガーしたか
- どのしきい値が権威あるものか
- 検出ロジックをどのように説明するか

検出ロジックの所有権を持つ場合、アラートメッセージの所有権も持つ必要があります。

{{% /notice %}}

メッセージ本文を以下に置き換えます

```handlebars
{{#if anomalous}}
 Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" triggered at {{timestamp}}.
{{else}}
 Rule "{{{ruleName}}}" in detector "{{{detectorName}}}" cleared at {{timestamp}}.
{{/if}}

{{#if anomalous}}
Triggering condition: {{{readableRule}}}
{{/if}}

Mean value of signal in the last {{event_annotations.current_window}}: {{inputs.CPU.value}}

{{#if anomalous}}
Historical anomaly threshold: {{inputs.CPU_top_threshold.value}}
Static guardrail threshold: {{inputs.CPU_static_threshold.value}}
{{else}}
Clear threshold: {{inputs.clear_top.value}}
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

これにより、以下を明示的に参照しています

- `{{inputs.CPU_top_threshold.value}}` → 動的異常しきい値
- `{{inputs.CPU_static_threshold.value}}` → 静的 90% ガードレール

これらの変数は、両方のストリームが SignalFlow でパブリッシュされているため使用可能です。

---

{{% button style="blue" %}}Done Editing{{% /button %}} をクリックしてカスタムメッセージを保存します。

{{% button style="blue" %}}ProceedAlert Recipients.{{% /button %}} をクリックします。

---

## ステップ 3 – アラートルールの説明の更新

{{% button style="blue" %}}Proceed to Alert Activation{{% /button %}}

**Activate...** ステップで、**Description** を以下に更新します

```
The 10m moving average of system.cpu.utilization (assumed to be cyclical over 1d periods) is more than 2.5 standard deviation(s) above its historical norm and has exceeded 90% for 15 minutes.
```

{{% button style="blue" %}}Update Alert Rule{{% /button %}} をクリックして変更を保存します。

---

## まとめ

ここまでで以下を完了しました

- ウィザードを使用して履歴ベースラインパラメータを設定
- 生成された SignalFlow をリファクタリングしてしきい値ストリームを公開
- 複合条件アラートロジック（履歴異常 + 静的ガードレール）を追加
- 異常しきい値と静的しきい値の両方を再利用のためにパブリッシュ
- 検出ロジックを明確に伝えるためにアラートメッセージと説明を更新
