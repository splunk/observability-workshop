---
title: ノートとダッシュボードレイアウトの追加
linkTitle: 1.10 Notes and layout
weight: 1.10
---

## 1. ノートの追加

ダッシュボードでは、ユーザーを支援する短い「説明」ペインを配置することが有効な場合がよくあります。{{% button %}}**New Text Note**{{% /button %}} ボタンをクリックして、今すぐ追加しましょう。

![three charts](../../images/add-notes.png)

これによりノートエディタが開きます。

![Notes 1](../../images/notes-editor.png)

テキストだけでなくさらに多くのものをノートに追加できるように、Splunkではこれらのノート/ペインでMarkdownを使用できます。
Markdownは、Webページでよく使用される、プレーンテキストを使用してフォーマットされたテキストを作成するための軽量なマークアップ言語です。

これには以下が含まれます（ただし、これらに限定されません）：

* ヘッダー（さまざまなサイズで）
* 強調スタイル
* リストとテーブル
* リンク。外部のWebページ（ドキュメントなど）または他のSplunk IMダッシュボードへの直接リンクが可能です

以下は、ノートで使用できる上記のMarkdownオプションの例です。

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

コピーボタンを使用して上記をコピーし、*Edit* ボックスに貼り付けます。
プレビューでどのように表示されるかを確認できます。

---

## 2. チャートの保存

ノートチャートに名前を付けます。この例では *Example text chart* を使用しました。次に、{{% button style="blue" %}}Save And Close{{% /button %}} ボタンを押します。

![saving note](../../images/notes-with-example.png)

これにより、ノートを含むダッシュボードに戻ります。

![three charts and note](../../images/3-charts-and-note.png)

---

## 3. チャートの順序とサイズ

チャートのデフォルトの順序とサイズが気に入らない場合は、ウィンドウのドラッグ技術を使用して、目的の場所に移動およびサイズ変更できます。

チャートの **上部** の境界線をつかむと、マウスポインターがドラッグアイコンに変わるのが確認できます（下の図を参照）。

![dragging charts](../../images/M-Notes-4.png)

**Latency vs Load** チャートを **Latency History** チャートと **Example text chart** の間にドラッグします。

![sizing](../../images/M-Notes-5.png)

左、右、下の端からドラッグして、ウィンドウのサイズを変更することもできます。

最後の演習として、ノートチャートの幅を他のチャートの約3分の1に縮小します。チャートは、サポートするサイズの1つに自動的にスナップします。他の3つのチャートをダッシュボードの約3分の1の幅に広げます。ノートを他のチャートの右側にドラッグし、他の3つのチャートと一致するようにサイズを変更します。**Time** を **-1h** に設定すると、以下のようなダッシュボードができあがります！

![TaDA!](../../images/M-Notes-6.png)
