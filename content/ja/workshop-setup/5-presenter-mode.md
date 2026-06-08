---
title: Presenter Mode
weight: 5
time: false
---

## **Presenter Mode とは？**

Presenter Mode は、タイミングのヒント、「今バックグラウンドでこれを開始してください」というプロンプト、その他ワークショップを進行する人向けのガイダンスなど、デフォルトでは参加者に表示されない進行用の手がかりを表示します。ノートは関連するステップの横にインラインで記述されるため、プレゼンテーション中にコンテキストを確認しながら進めることができます。

---

### **Presenter Mode をオンにする**

**任意の**ワークショップ URL に `?presenter=1` を追加して、ページを一度読み込みます。例

```text
https://splunk.github.io/observability-workshop/en/?presenter=1
```

読み込み後、すべてのページの右下にマゼンタ色の **Presenter on** ピルが表示され、プレゼンターノートが見えるようになります。この設定はブラウザに記憶されるため、デバイスごとに一度だけ行えば十分です。

{{% notice style="tip" title="ブックマークしましょう" %}}
`?presenter=1` を URL に含めた状態でワークショップのホームページをブックマークしてください。新しいブラウザやデバイスでそのブックマークを開くと、Presenter Mode が自動的にオンになります。
{{% /notice %}}

### **Presenter Mode をオフにする**

右下のマゼンタ色の **Presenter on** ピルをクリックします。ピルが消え、ノートは再び非表示になります。

### **プレゼンターノートの作成**

ガイダンスを `presenter` ショートコードで囲みます。ノートには通常の Markdown（リスト、コード、リンク、画像）を含めることができます

```markdown
{{</* presenter */>}}
Start the EC2 instance now — boot takes ~3 minutes.
{{</* /presenter */>}}

{{</* presenter title="Timing" */>}}
Allow ~10 minutes for attendees to finish this section.
{{</* /presenter */>}}
```

オプションの `title` 属性は、ノート上部の小さなラベルを変更します（デフォルトは "Presenter note"）。

以下はライブの例です — 現在 Presenter Mode がオンの場合のみ表示されます

{{< presenter title="Example" >}}
This is what a presenter note looks like. If you can read this, presenter mode is on.
{{< /presenter >}}

### **参加者に見えるもの**

何も見えません。ノートはレンダリングされず、トグルピルも参加者には表示されません。

{{% notice style="warning" title="非表示であり、秘密ではありません" %}}
プレゼンターノートは CSS で非表示にされていますが、ページの HTML ソースには**存在しています**。この機能は進行の手がかりやタイミングに使用してください。解答キー、認証情報、または参加者から本当に隠す必要があるものには使用**しないでください**。
{{% /notice %}}
