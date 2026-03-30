---
title: 3. Enable OBI via Helm
weight: 3
---

アプリケーションコードを一切変更せずに、クラスター全体にトレースを追加します。必要なのはHelmのアップグレード1回だけです。

## OBI を有効にして Collector をアップグレード

{{% notice title="Exercise" style="green" icon="running" %}}

``` bash
helm -n obi-workshop  upgrade splunk-otel-collector \
  splunk-otel-collector-chart/splunk-otel-collector \
  --set="splunkObservability.realm=${REALM}" \
  --set="splunkObservability.accessToken=${ACCESS_TOKEN}" \
  --set="clusterName=${INSTANCE}-k8s" \
  --set="environment=${INSTANCE}-ebpf" \
  --set="obi.enabled=true"
```

{{% /notice %}}

`--set="obi.enabled=true"` の追加が唯一の変更点です。Helmチャートが他のすべてを処理します：

- **OBI DaemonSet** をデプロイ（各ノードに1つのPod）
- RBACを設定（ServiceAccount、ClusterRole、ClusterRoleBinding）
- OBIを自動的にCollectorに接続
- eBPFに必要なLinux権限を付与

### OBI に必要なものは？

OBI Podは昇格された権限で実行されます。これはeBPFがカーネルレベルで動作するためです：

``` yaml
hostPID: true        # ノード上のすべてのプロセスを確認（他の Pod を含む）
hostNetwork: true    # ネットワークトラフィックを監視し、トレースコンテキストを注入
privileged: true     # カーネルに eBPF プローブをアタッチ
```

クラスターポリシーで必要な場合、権限を削減する方法の詳細については [OBI Security Documentation](https://opentelemetry.io/docs/zero-code/obi/security/) を参照してください。

## OBI が実行されていることを確認

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods  -n obi-workshop -l app.kubernetes.io/name=obi
kubectl logs  -n obi-workshop -l app.kubernetes.io/name=obi --tail=20
```

{{% /tab %}}
{{% tab title="Example Output to look for" %}}

``` text
NAME        READY   STATUS    RESTARTS   AGE
obi-abc12   1/1     Running   0          45s

...
level=INFO msg="instrumenting process" service=payment-service
...
level=INFO msg="instrumenting process" service=order-processor
...
level=INFO msg="instrumenting process" service=frontend
```

{{% /tab %}}
{{< /tabs >}}

トラフィックを生成します：

``` bash
curl -s http://localhost:30000/create-order | python3 -m json.tool
```

## Splunk APM で確認

トレースが流れるまで30〜60秒待ちます。

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: 3つのサービスが表示されるはずです：`frontend` -> `order-processor` -> `payment-service`
2. **Traces**: 任意のトレースをクリックしてください。3つのサービスすべてにまたがる完全な分散トレースと、各ホップのタイミングが表示されます。
3. **Phase 2 と同様**: コード変更ゼロ。1つのフラグを指定した `helm upgrade` のみ。

{{% /notice %}}
