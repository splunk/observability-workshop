---
title: Kubernetes 監査ログの確認
linkTitle: 3.2 Kubernetes 監査ログの確認
weight: 3
---

このセクションでは、収集されている Kubernetes 監査ログを確認します。これらのイベントは非常にリッチであるため、そのままチャート化するのは効率的ではないことがわかります。この問題に対処するため、Ingest Processor で Ingest Pipeline を作成し、これらのイベントを Splunk Observability Cloud に送信されるメトリクスに変換します。これにより、イベントをはるかに効率的にチャート化でき、Splunk Observability Cloud のリアルタイムストリーミングメトリクスの利点を活用できるようになります。

{{% notice title="演習: Ingest Pipeline の作成" style="green" icon="running" %}}

**1.** Splunk Show のワークショップ詳細に記載されている URL を使って、**Ingest Processor Cloud Stack** インスタンスを開きます。

**2.** **Apps** → **Search and Reporting** に移動します。

![Search and Reporting](../../images/search_and_reporting.png?width=20vw)

**3.** 検索バーに次の SPL 検索文字列を入力します。

{{% notice title="Note" style="primary" icon="lightbulb" %}}
`USER_ID` は、Splunk Show インスタンス情報に記載されているユーザー ID に置き換えてください。
{{% /notice %}}

``` sh
### Replace USER_ID with the User ID provided in your Splunk Show instance information
index=main sourcetype="kube:apiserver:audit:USER_ID"
```

**4.** **Enter** キーを押すか、緑色の虫眼鏡アイコンをクリックして検索を実行します。

![Kubernetes Audit Log](../../images/k8s_audit_log.png)

{{% notice title="Note" style="info" %}}
これで、環境の Kubernetes 監査ログが表示されているはずです。イベントがかなりリッチであることに気付くでしょう。利用可能なフィールドを調べ、どの情報がメトリクスやディメンションの候補として適しているか考え始めてください。次のように自問してみてください: どのフィールドをチャート化したいか、それらのフィールドをどのようにフィルター、グループ化、または分割できるようにしたいか?
{{% /notice %}}

{{%/ notice %}}
