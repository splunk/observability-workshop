---
title: 3. Helmを使用してOBIを有効化
weight: 3
---

アプリケーションコードを一切変更せず、Helmのアップグレード1つでクラスター全体にトレーシングを追加します。

## OBIを有効にしてCollectorをアップグレード

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

変更点は `--set="obi.enabled=true"` の1つだけです。Helmチャートがそれ以外のすべてを処理します。

- **OBI DaemonSet** をデプロイ（ノードごとに1つのPod）
- RBACを構成（ServiceAccount、ClusterRole、ClusterRoleBinding）
- OBIをCollectorに自動的に接続
- eBPFに必要なLinuxケーパビリティを付与

### OBIに必要なものは？

OBI PodはeBPFがカーネルレベルで動作するため、昇格された権限で実行されます。

``` yaml
hostPID: true        # See all processes on the node, including other pods
hostNetwork: true    # Observe and inject trace context into network traffic
privileged: true     # Attach eBPF probes to the kernel
```

クラスターポリシーで権限の縮小が必要な場合の詳細は、[OBI Security Documentation](https://opentelemetry.io/docs/zero-code/obi/security/)を参照してください。

## OBIが実行中であることを確認

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
kubectl get pods  -n obi-workshop -l app.kubernetes.io/name=obi
kubectl logs  -n obi-workshop -l app.kubernetes.io/name=obi --tail=20
```

{{% /tab %}}
{{% tab title="期待される出力例" %}}

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

トラフィックを生成します。

``` bash
curl -s http://localhost:30000/create-order | jq
```

## Splunk APMを確認

トレースが流れるまで30〜60秒待ちます。

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: `frontend` -> `order-processor` -> `payment-service` の3つのサービスが表示されます。
2. **Traces**: 任意のトレースをクリックします。3つのサービスすべてにまたがる分散トレースが、各ホップのタイミングとともに表示されます。
3. **フェーズ2と同じ**: コード変更ゼロ。1つのフラグで `helm upgrade` を1回実行するだけです。

{{% /notice %}}
