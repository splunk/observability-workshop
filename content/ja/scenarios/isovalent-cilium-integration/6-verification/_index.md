---
title: 検証
weight: 6
---

## すべてのコンポーネントの検証

すべてが正常に動作していることを確認するために、以下の包括的なチェックを実行します

```bash
echo "=== Cluster Nodes ==="
kubectl get nodes

echo -e "\n=== Cilium Components ==="
kubectl get pods -n kube-system -l k8s-app=cilium

echo -e "\n=== Hubble Components ==="
kubectl get pods -n kube-system | grep hubble

echo -e "\n=== Tetragon ==="
kubectl get pods -n tetragon

echo -e "\n=== Splunk OTel Collector ==="
kubectl get pods -n otel-splunk
```

**期待される出力**

- 2つのノードが `Ready` 状態であること
- Cilium Pod：2つが実行中（ノードごとに1つ）
- Hubble relay と timescape：実行中
- Tetragon Pod：2つが実行中 + operator
- Splunk collector Pod：実行中

## メトリクスエンドポイントの検証

各コンポーネントからメトリクスにアクセスできることをテストします

```bash
# Test Cilium metrics
kubectl exec -n kube-system ds/cilium -- curl -s localhost:9962/metrics | head -20

# Test Hubble metrics
kubectl exec -n kube-system ds/cilium -- curl -s localhost:9965/metrics | head -20

# Test Tetragon metrics
kubectl exec -n tetragon ds/tetragon -- curl -s localhost:2112/metrics | head -20
```

各コマンドは Prometheus 形式のメトリクスを返すはずです。

## Splunk Observability Cloud での検証

### Infrastructure Navigator の確認

1. Splunk Observability Cloud アカウントにログインします
2. **Infrastructure** → **Kubernetes** に移動します
3. クラスターを見つけます`isovalent-demo`
4. クラスターがメトリクスを報告していることを確認します

### Isovalent メトリクスの検索

**Metrics** に移動して以下を検索します

- `cilium_*` - Cilium ネットワーキングメトリクス
- `hubble_*` - ネットワークフローメトリクス
- `tetragon_*` - ランタイムセキュリティメトリクス

{{% notice title="ヒント" style="tip" %}}
インストール後、メトリクスが Splunk Observability Cloud に表示されるまで2〜3分かかる場合があります。
{{% /notice %}}

## ダッシュボードの表示

### カスタムダッシュボードの作成

1. **Dashboards** → **Create** に移動します
2. 主要なメトリクスのチャートを追加します

**Cilium Endpoint State**

```text
cilium_endpoint_state{cluster="isovalent-demo"}
```

**Hubble Flow Processing**

```text
hubble_flows_processed_total{cluster="isovalent-demo"}
```

**Tetragon Events**

```text
tetragon_dns_total{cluster="isovalent-demo"}
```

### クエリの例

**DNS Query Rate**

```text
rate(hubble_dns_queries_total{cluster="isovalent-demo"}[1m])
```

**Dropped Packets**

```text
sum by (reason) (hubble_drop_total{cluster="isovalent-demo"})
```

**Network Policy Enforcements**

```text
rate(cilium_policy_l7_total{cluster="isovalent-demo"}[5m])
```

## トラブルシューティング

### Splunk にメトリクスが表示されない場合

メトリクスが表示されない場合

1. **コレクターのログを確認します**

   ```bash
   kubectl logs -n otel-splunk -l app=splunk-otel-collector --tail=200
   ```

2. **スクレイプターゲットを確認します**

   ```bash
   kubectl describe configmap -n otel-splunk splunk-otel-collector-otel-agent
   ```

3. **ネットワーク接続を確認します**

   ```bash
   kubectl exec -n otel-splunk -it deployment/splunk-otel-collector -- \
     curl -v https://ingest.<YOUR-REALM>.signalfx.com
   ```

### Pod が実行されていない場合

Cilium または Tetragon の Pod が実行されていない場合

1. **Pod のステータスを確認します**

   ```bash
   kubectl describe pod -n kube-system <cilium-pod-name>
   ```

2. **ログを確認します**

   ```bash
   kubectl logs -n kube-system <cilium-pod-name>
   ```

3. **ノードの準備状態を確認します**

   ```bash
   kubectl get nodes -o wide
   ```

## クリーンアップ

すべてのリソースを削除して AWS の課金を回避するには

```bash
# Delete the OpenTelemetry Collector
helm uninstall splunk-otel-collector -n otel-splunk

# Delete the EKS cluster (this removes everything)
eksctl delete cluster --name isovalent-demo --region us-east-1
```

{{% notice title="警告" style="warning" %}}
クリーンアップ処理には10〜15分かかります。課金を回避するために、すべてのリソースが削除されたことを確認してください。
{{% /notice %}}

## 次のステップ

インテグレーションが正常に動作するようになったら

- サンプルアプリケーションをデプロイしてネットワークトラフィックを生成します
- ネットワークポリシーを作成し、適用状況を監視します
- Splunk でドロップされたパケットやセキュリティイベントのアラートを設定します
- Hubble の L7 可視性を使用して HTTP/gRPC トラフィックを調査します
- Tetragon を使用してプロセスの実行とファイルアクセスを監視します

{{< checkpoint "Isovalent Enterprise Platform と Splunk Observability Cloud のインテグレーションが正常に完了しました！" >}}
