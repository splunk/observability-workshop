---
title: 3. Helm を使って OBI を有効化する
weight: 3
---

これで、アプリケーションコードを一切変更することなく、たった 1 回の Helm アップグレードでクラスター全体にトレーシングを追加できます。

## OBI を有効にして Collector をアップグレードする

{{% notice title="演習" style="green" icon="running" %}}

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

変更点はこの `--set="obi.enabled=true"` ただ 1 つだけです。残りはすべて Helm チャートが処理してくれます。

- **OBI DaemonSet** をデプロイする（ノードごとに 1 つの Pod）
- RBAC（ServiceAccount、ClusterRole、ClusterRoleBinding）を構成する
- OBI を自動的に Collector に向ける
- eBPF に必要な Linux capabilities を付与する

### OBI に必要なものは？

eBPF はカーネルレベルで動作するため、OBI Pod は昇格された権限で実行されます。

``` yaml
hostPID: true        # See all processes on the node, including other pods
hostNetwork: true    # Observe and inject trace context into network traffic
privileged: true     # Attach eBPF probes to the kernel
```

クラスターのポリシー上、権限を縮小する必要がある場合は、[OBI Security Documentation](https://opentelemetry.io/docs/zero-code/obi/security/) を参照してください。

## OBI が稼働していることを確認する

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

トラフィックを生成します。

``` bash
curl -s http://localhost:30000/create-order | jq
```

## Splunk APM を確認する

トレースが流れてくるまで 30〜60 秒待ちます。

{{% notice title="演習" style="green" icon="running" %}}

1. **Service Map**: `frontend` -> `order-processor` -> `payment-service` の 3 つのサービスが表示されているはずです。
2. **Traces**: 任意のトレースをクリックします。3 つのサービスすべてにまたがる分散トレース全体と、各ホップの所要時間を確認できます。
3. **Phase 2 と同じ流れ**: コード変更はゼロ。フラグを 1 つ付けた `helm upgrade` を 1 回実行するだけです。

{{% /notice %}}
