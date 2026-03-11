---
title: Kubernetes Audit ログの確認
linkTitle: 3.2 Kubernetes Audit ログの確認
weight: 3
---

このセクションでは、収集されているKubernetes Auditログを確認します。イベントが非常に充実していることがわかります。これにより、チャート作成が非効率になる可能性があります。これに対処するために、Ingest ProcessorでIngest Pipelineを作成し、これらのイベントをSplunk Observability Cloudに送信されるメトリクスに変換します。これにより、イベントをより効率的にチャート化し、Splunk Observability Cloudのリアルタイムストリーミングメトリクスを活用できるようになります。

{{% notice title="演習: Ingest Pipelineの作成" style="green" icon="running" %}}

**1.** Splunk Showワークショップの詳細に記載されているURLを使用して、**Ingest Processor Cloud Stack** インスタンスを開きます。

**2.** **Apps** → **Search and Reporting** に移動します。

![Search and Reporting](../../images/search_and_reporting.png?width=20vw)

**3.** 検索バーに、以下のSPL検索文字列を入力します。

{{% notice title="Note" style="primary" icon="lightbulb" %}}
`USER_ID` をSplunk Showインスタンス情報に記載されているUser IDに置き換えてください。
{{% /notice %}}

``` sh
### Replace USER_ID with the User ID provided in your Splunk Show instance information
index=main sourcetype="kube:apiserver:audit:USER_ID"
```

**4.** **Enter** を押すか、緑色の虫眼鏡をクリックして検索を実行します。

![Kubernetes Audit Log](../../images/k8s_audit_log.png)

{{% notice title="Note" style="info" %}}
これで、環境のKubernetes Auditログが表示されるはずです。イベントがかなり充実していることに注目してください。利用可能なフィールドを探索し、どの情報がメトリクスとディメンションの良い候補になるか考え始めてください。自問してください：どのフィールドをチャート化したいか、それらのフィールドをどのようにフィルタリング、グループ化、または分割したいか？
{{% /notice %}}

{{%/ notice %}}
