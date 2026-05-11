---
title: 3. Helm で OBI を有効化する
weight: 3
---

アプリケーションコードを一切変更せずに、Helm のアップグレード1つでクラスター全体にトレーシングを追加します。

## OBI を有効にして Collector をアップグレードする

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

変更点は `--set="obi.enabled=true"` の1つだけです。それ以外はすべて Helm チャートが処理します

- **OBI DaemonSet** をデプロイします（ノードごとに1つの Pod）
- RBAC（ServiceAccount、ClusterRole、ClusterRoleBinding）を構成します
- OBI を自動的に Collector に接続します
- eBPF に必要な Linux ケーパビリティを付与します

### OBI に必要なものは？

OBI Pod は、eBPF がカーネルレベルで動作するため、昇格された権限で実行されます

``` yaml
hostPID: true        # See all processes on the node, including other pods
hostNetwork: true    # Observe and inject trace context into network traffic
privileged: true     # Attach eBPF probes to the kernel
```

クラスターポリシーで権限の制限が必要な場合は、[OBI Security Documentation](https://opentelemetry.io/docs/zero-code/obi/security/) で詳細をご確認ください。

## OBI の動作を確認する

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl get pods  -n obi-workshop -l app.kubernetes.io/name=obi
kubectl logs  -n obi-workshop -l app.kubernetes.io/name=obi --tail=20
```

{{% /tab %}}
{{% tab title="確認すべき出力例" %}}

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

トラフィックを生成します

``` bash
curl -s http://localhost:30000/create-order | jq
```

## Splunk APM を確認する

トレースが流れるまで30〜60秒お待ちください。

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: `frontend` -> `order-processor` -> `payment-service` の3つのサービスが表示されるはずです。
2. **Traces**: 任意のトレースをクリックしてください。3つのサービスすべてにまたがる分散トレースが、各ホップのタイミングとともに表示されます。
3. **フェーズ 2 と同じストーリー**: コード変更はゼロです。1つのフラグを指定した `helm upgrade` 1回だけです。

{{% /notice %}}
