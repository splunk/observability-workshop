---
title: 3. Helm で OBI を有効化
weight: 3
---

アプリケーションコードを一切変更せずに、Helm のアップグレード1回だけでクラスター全体にトレーシングを追加します。

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

変更点は `--set="obi.enabled=true"` という1つのオプションだけです。Helm チャートが残りのすべてを処理します

- **OBI DaemonSet** をデプロイ（ノードごとに1つの Pod）
- RBAC を設定（ServiceAccount、ClusterRole、ClusterRoleBinding）
- OBI を自動的に Collector に接続
- eBPF に必要な Linux ケーパビリティを付与

### OBI に必要なものは？

OBI Pod は、eBPF がカーネルレベルで動作するため、昇格した権限で実行されます

``` yaml
hostPID: true        # See all processes on the node, including other pods
hostNetwork: true    # Observe and inject trace context into network traffic
privileged: true     # Attach eBPF probes to the kernel
```

クラスターポリシーで必要な場合に権限を削減する方法については、[OBI Security Documentation](https://opentelemetry.io/docs/zero-code/obi/security/) を参照してください。

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

トラフィックを生成します

``` bash
curl -s http://localhost:30000/create-order | python3 -m json.tool
```

## Splunk APM を確認

トレースが流れるまで30〜60秒待ちます。

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: `frontend` -> `order-processor` -> `payment-service` の3つのサービスが表示されるはずです。
2. **Traces**: 任意のトレースをクリックします。3つのサービスすべてにまたがる完全な分散トレースと、各ホップのタイミングが表示されます。
3. **フェーズ2と同じストーリー**: コード変更ゼロ。1つのフラグを付けた `helm upgrade` 1回だけです。

{{% /notice %}}
