---
title: ノートの追加とダッシュボードレイアウト
linkTitle: 1.10 ノートとレイアウト
weight: 1.10
---

## 1. ノートの追加

ダッシュボードでは、利用者を支援する短い「説明」ペインを配置することがよくあります。{{% button %}}**New Text Note**{{% /button %}} ボタンをクリックして追加してみましょう。

![three charts](../../images/add-notes.png)

これによりノートエディターが開きます。

![Notes 1](../../images/notes-editor.png)

テキスト以外の要素もノートに追加できるよう、Splunk ではこれらのノート/ペインで Markdown が使用できるようになっています。
Markdown は、プレーンテキストを使ってフォーマット済みのテキストを作成するための軽量なマークアップ言語で、Web ページなどでよく利用されています。

利用できる要素には以下が含まれます (ただしこれらに限定されません):

* ヘッダー (様々なサイズ)
* 強調スタイル
* リストとテーブル
* リンク。外部 Web ページ (ドキュメント等) や、他の Splunk IM ダッシュボードへの直接リンクなど

以下は、ノートで使用できる上記の Markdown オプションの例です。

{{% tab title="Sample Markdown text" %}}

``` markdown
# h1 Big headings

###### h6 To small headings

##### Emphasis

**This is bold text**, *This is italic text* , ~~Strikethrough~~

##### Lists

Unordered

+ Create a list by starting a line with `+`, `-`, or `*`
- Sub-lists are made by indenting 2 spaces:
- Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
* Very easy!

Ordered

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa

##### Tables

| Option | Description |
| ------ | ----------- |
| chart  | path to data files to supply the data that will be passed into templates. |
| engine | engine to be used for processing templates. Handlebars is the default. |
| ext    | extension to be used for dest files. |

#### Links

[link to webpage](https://www.splunk.com)

[link to dashboard with title](https://app.eu0.signalfx.com/#/dashboard/EaJHrbPAEAA?groupId=EaJHgrsAIAA&configId=EaJHsHzAEAA "Link to the Sample chart Dashboard!")
```

{{% /tab %}}

コピーボタンで上記をコピーし、*Edit* ボックスに貼り付けてください。
プレビューには、表示される見た目が示されます。

---

## 2. チャートの保存

ノートチャートに名前を付けます。例では *Example text chart* を使用しました。次に {{% button style="blue" %}}Save And Close{{% /button %}} ボタンを押してください。

![saving note](../../images/notes-with-example.png)

ダッシュボードに戻ると、ノートが追加された状態になっています。

![three charts and note](../../images/3-charts-and-note.png)

---

## 3. チャートの並び替えとサイズ変更

チャートのデフォルトの順序やサイズが好みに合わない場合は、ウィンドウのドラッグ操作で目的の場所に移動したり、サイズを変更したりできます。

チャートの **上端** をつかむと、マウスポインターがドラッグアイコンに変わります (下図参照)。

![dragging charts](../../images/M-Notes-4.png)

それでは、**Latency vs Load** チャートをドラッグして、**Latency History** チャートと **Example text chart** の間に配置してください。

![sizing](../../images/M-Notes-5.png)

また、ウィンドウの左端、右端、下端をドラッグしてリサイズすることもできます。

最後の演習として、ノートチャートの幅を他のチャートの約 3 分の 1 まで縮小してください。チャートはサポートされているサイズのいずれかに自動的にスナップします。他の 3 つのチャートをダッシュボードの約 3 分の 1 の幅まで広げます。ノートを他のチャートの右側にドラッグし、3 つのチャートと高さが揃うようサイズを調整してください。**Time** を **-1h** に設定すれば、以下のようなダッシュボードができあがります!

![TaDA!](../../images/M-Notes-6.png)
