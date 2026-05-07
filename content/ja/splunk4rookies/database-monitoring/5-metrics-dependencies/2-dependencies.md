---
title: 2. 依存関係
weight: 2
---

**Dependencies** タブは、従来のデータベースツールでは答えられない問いに答えます。*実際にこのデータベースを呼び出しているのはどのアプリケーションとホストか？* Database Monitoring は、検出した接続を Splunk Observability Cloud にすでに存在するアプリケーションテレメトリと相関させることで、匿名の接続文字列のリストではなく、クライアントのリストを提供します。

これにより、データベースの調査が*エンジニアリング*の調査に変わります。オンコールの DBA を呼び出す代わりに、負荷の高い呼び出し元を所有するチームに直接問題を転送できます。

{{% notice title="演習" style="green" icon="running" %}}

* Navigator で **Dependencies** タブをクリックします。
* 選択した時間範囲でこのインスタンスに接続したアプリケーションとホストのリストを確認します。
* クエリボリュームの最大シェアを占めるアプリケーションを特定します。

<!-- TODO screenshot: Dependencies tab showing a list of client applications and hosts ranked by query volume -->
![依存関係](../images/dependencies.png)

{{< tabs >}}
{{% tab title="質問" %}}
**候補となるクエリがあり、それを呼び出しているアプリケーションもわかっています。次に誰に話しますか？**
{{% /tab %}}
{{% tab title="回答" %}}
**呼び出し元のアプリケーションを所有するチーム**です — クエリだけでなく、次の章ではトレースへの直接リンクも渡すことができます。
{{% /tab %}}
{{< /tabs >}}

{{% /notice %}}
