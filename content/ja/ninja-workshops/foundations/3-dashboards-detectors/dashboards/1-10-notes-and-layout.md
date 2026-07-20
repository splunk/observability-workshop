---
title: ノートとダッシュボードレイアウトの追加
linkTitle: 1.10 ノートとレイアウト
weight: 1.10
---

## 1. ノートの追加

ダッシュボードでは、ユーザーを助ける短い「説明」ペインを配置することが有効な場合があります。{{% button %}}**New Text Note**{{% /button %}} ボタンをクリックしてノートを追加します。

![three charts](../../images/add-notes.png)

ノートエディタが開きます。

![Notes 1](../../images/notes-editor.png)

Splunkではノートにテキスト以外も追加できるよう、Markdownを使用できます。
Markdownは、プレーンテキストを使用してフォーマットされたテキストを作成する軽量マークアップ言語で、Webページでよく使われます。

以下の機能が含まれます（これに限定されません）

* 見出し（さまざまなサイズ）
* 強調スタイル
* リストとテーブル
* リンク。外部のWebページ（ドキュメントなど）や他のSplunk IM Dashboardへの直接リンクが可能です

以下は、ノートで使用できる上記のMarkdownオプションの例です。

{{% tab title="Markdownテキストのサンプル" %}}

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

コピーボタンを使用して上記をコピーし、 *Edit* ボックスに貼り付けます。プレビューで表示結果を確認できます。

---

## 2. チャートの保存

ノートチャートに名前を付けます。この例では *Example text chart* を使用しました。次に {{% button style="blue" %}}Save And Close{{% /button %}} ボタンを押します。

![saving note](../../images/notes-with-example.png)

ダッシュボードに戻り、ノートが追加されています。

![three charts and note](../../images/3-charts-and-note.png)

---

## 3. チャートの並べ替えとサイズ変更

チャートのデフォルトの順序やサイズが好みでない場合、ウィンドウのドラッグ操作で目的の位置に移動やサイズ変更ができます。

チャートの **上部** の境界線をつかむと、マウスポインターがドラッグアイコンに変わります（下の画像を参照）。

![dragging charts](../../images/M-Notes-4.png)

**Latency vs Load** チャートを **Latency History** チャートと **Example text chart** の間にドラッグします。

![sizing](../../images/M-Notes-5.png)

左端、右端、下端からドラッグしてウィンドウのサイズを変更することもできます。

最後の演習として、ノートチャートの幅を他のチャートの約3分の1に縮小します。チャートはサポートされているサイズのいずれかに自動的にスナップします。他の3つのチャートをダッシュボードの約3分の1の幅に広げます。ノートを他のチャートの右側にドラッグし、3つのチャートに合わせてサイズを変更します。 **Time** を **-1h** に設定すると、以下のようなダッシュボードが表示されます。

![TaDA!](../../images/M-Notes-6.png)
