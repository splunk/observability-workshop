---
title: EKS セットアップ
weight: 3
---

## ステップ 1: Helm リポジトリの追加

必要な Helm リポジトリを追加します:

```bash
# Add Isovalent Helm repository
helm repo add isovalent https://helm.isovalent.com

# Add Splunk OpenTelemetry Collector Helm repository
helm repo add splunk-otel-collector-chart https://signalfx.github.io/splunk-otel-collector-chart

# Update Helm repositories
helm repo update
```

## ステップ 2: EKS クラスター構成の作成

`cluster.yaml` という名前のファイルを作成します:

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: isovalent-demo
  region: us-east-1
  version: "1.30"
iam:
  withOIDC: true
addonsConfig:
  disableDefaultAddons: true
addons:
- name: coredns
```

**主な構成の詳細:**

- `disableDefaultAddons: true` - AWS VPC CNI と kube-proxy を無効にします（Cilium が両方を置き換えます）
- `withOIDC: true` - サービスアカウント用の IAM ロールを有効にします（Cilium が ENI を管理するために必要です）
- `coredns` アドオンは DNS 解決に必要なため保持されます

{{% notice title="デフォルトアドオンを無効にする理由" style="info" %}}
Cilium は eBPF を使用した独自の CNI 実装を提供しており、デフォルトの AWS VPC CNI よりも高性能です。デフォルトを無効にすることで、競合を回避し、Cilium にすべてのネットワーキングを処理させることができます。
{{% /notice %}}

## ステップ 3: EKS クラスターの作成

クラスターを作成します（約 15〜20 分かかります）:

```bash
eksctl create cluster -f cluster.yaml
```

クラスターが作成されたことを確認します:

```bash
# Update kubeconfig
aws eks update-kubeconfig --name isovalent-demo --region us-east-1

# Check pods
kubectl get pods -n kube-system
```

**期待される出力:**

- CoreDNS Pod は `Pending` 状態になります（これは正常です - CNI を待機しています）
- ワーカーノードはまだありません

{{% notice title="注意" style="warning" %}}
CNI プラグインがない場合、Pod は IP アドレスやネットワーク接続を取得できません。CoreDNS は Cilium がインストールされるまで Pending のままになります。
{{% /notice %}}

## ステップ 4: Kubernetes API Server エンドポイントの取得

Cilium の構成に必要です:

```bash
aws eks describe-cluster --name isovalent-demo --region us-east-1 \
  --query 'cluster.endpoint' --output text
```

このエンドポイントを保存してください - Cilium のインストール手順で使用します。

## ステップ 5: Prometheus CRD のインストール

Cilium はメトリクスに Prometheus ServiceMonitor CRD を使用します:

```bash
kubectl apply -f https://github.com/prometheus-operator/prometheus-operator/releases/download/v0.68.0/stripped-down-crds.yaml
```

{{< checkpoint "EKS クラスターが作成されたので、Cilium、Hubble、Tetragon をインストールする準備が整いました！" >}}
