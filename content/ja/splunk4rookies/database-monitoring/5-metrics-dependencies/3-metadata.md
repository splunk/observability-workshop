---
title: 3. メタデータ
weight: 3
---

**Metadata** タブは Navigator の中で最も小さく、見落としやすいタブですが、調査対象のインスタンスに関する基本情報を確認する場所です。エンジンバージョン、ホスト、エディション、設定パラメータがすべてここに表示されます。

次のような疑問に答えるために使用します。*これは想定しているエンジンバージョンか？プライマリかレプリカか？同じクラスター内の他のインスタンスと設定は同じか？*

{{% notice title="演習" style="green" icon="running" %}}

* Navigator で **Metadata** タブをクリックします。
* メタデータフィールドを確認し、インスタンスの **engine version** と **host** を記録します。

<!-- TODO screenshot: Metadata tab showing engine version, host, and other instance configuration details -->
![メタデータ](../images/metadata.png)

{{< tabs >}}
{{% tab title="質問" %}}
**クエリのチューニングに時間を費やす前に、エンジンバージョンを確認する価値があるのはなぜですか？**
{{% /tab %}}
{{% tab title="回答" %}}
**オプティマイザの動作、サポートされる構文、さらにはデフォルトのインデックス戦略はバージョン間で変わります** — 別のバージョンで有効だった修正が適用できない場合があり、発生している問題がより新しいバージョンでは既に修正されている可能性もあります。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
