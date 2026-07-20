---
title: Kubernetes Audit Logの確認
linkTitle: 3.2 Kubernetes Audit Logの確認
weight: 3
---

このセクションでは、収集されているKubernetes Audit Logを確認します。イベントは非常に詳細であるため、チャート化が非効率になる場合があります。これに対処するため、Ingest Processorでイベントをメトリクスに変換し、Splunk Observability Cloudに送信するIngest Pipelineを作成します。これにより、イベントをより効率的にチャート化し、Splunk Observability Cloudのリアルタイムストリーミングメトリクスを活用できます。

{{% notice title="演習: Ingest Pipelineの作成" style="green" icon="running" %}}

**1.** Splunk Showワークショップの詳細に記載されているURLを使用して、**Ingest Processor Cloud Stack** インスタンスを開きます。

**2.** **Apps** → **Search and Reporting** に移動します

![Search and Reporting](../../images/search_and_reporting.png?width=20vw)

**3.** 検索バーに以下のSPL検索文字列を入力します。

{{% notice title="注意" style="primary" icon="lightbulb" %}}
`USER_ID` をSplunk Showインスタンス情報に記載されているUser IDに置き換えてください。
{{% /notice %}}

``` sh
### Replace USER_ID with the User ID provided in your Splunk Show instance information
index=main sourcetype="kube:apiserver:audit:USER_ID"
```

**4.** **Enter** を押すか、緑色の虫眼鏡アイコンをクリックして検索を実行します。

![Kubernetes Audit Log](../../images/k8s_audit_log.png)

{{% notice title="注意" style="info" %}}
お使いの環境のKubernetes Audit Logが表示されます。イベントが非常に詳細であることに注目してください。利用可能なフィールドを探索し、メトリクスやディメンションの候補として適切な情報について考えてみましょう。どのフィールドをチャート化したいか、そしてそれらのフィールドをどのようにフィルタリング、グループ化、または分割したいかを考えてみてください。
{{% /notice %}}

{{%/ notice %}}
