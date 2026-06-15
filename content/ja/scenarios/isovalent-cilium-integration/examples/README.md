# 設定例

このディレクトリには、Isovalent Enterprise Platform と Splunk Observability Cloud の統合をデプロイする際に使用する設定ファイルが含まれています。

## ファイル概要

### EKS クラスター設定

- **cluster.yaml** - 初期 EKS クラスター設定
- **nodegroup.yaml** - ノードグループ設定

### Cilium Enterprise 設定

- **cilium-enterprise-values.yaml** - Cilium Enterprise のメイン Helm values
- **cilium-dns-proxy-ha-values.yaml** - DNS Proxy HA の Helm values

### Splunk OpenTelemetry 設定

- **splunk-otel-isovalent.yaml** - Isovalent メトリクスレシーバーとメトリクスフィルタリングを含む Splunk OpenTelemetry Collector の Helm values

### Splunk Observability Cloud ダッシュボード

- **Cilium by Isovalent.json** - Cilium メトリクス用の事前構築済みダッシュボード（エージェントステータス、ENI 割り当て、BPF マップ圧力）
- **Hubble by Isovalent.json** - Hubble メトリクス用の事前構築済みダッシュボード（ネットワークフロー、DNS クエリ、ドロップされたパケット）

## 必須プレースホルダー

これらの設定ファイルを使用する前に、以下のプレースホルダーを実際の値に置き換える**必要があります**

### 1. EKS API Server Endpoint

**ファイル:** `cilium-enterprise-values.yaml`  
**プレースホルダー:** `<YOUR-EKS-API-SERVER-ENDPOINT>`  
**場所:** 28行目 (`k8sServiceHost`)

**取得方法:**

```bash
kubectl cluster-info | grep 'Kubernetes control plane' | awk '{print $NF}' | sed 's|https://||'
```

**値の例:**

```
79F5FA6349FF9D1DC9052A3140032E7A.gr7.us-east-1.eks.amazonaws.com
```

### 2. Splunk Access Token

**ファイル:** `splunk-otel-isovalent.yaml`  
**プレースホルダー:** `<YOUR-SPLUNK-ACCESS-TOKEN>`  
**フィールド:** `splunkObservability.accessToken`

**取得方法:**

1. Splunk Observability Cloud にログインします
2. **Settings** > **Access Tokens** に移動します
3. **INGEST** 権限を持つ新しいトークンを作成するか、既存のトークンを使用します

**セキュリティに関する注意:** このトークンは安全に保管してください。バージョン管理にコミットしないでください。

### 3. Splunk Realm

**ファイル:** `splunk-otel-isovalent.yaml`  
**プレースホルダー:** `<YOUR-SPLUNK-REALM>`  
**フィールド:** `splunkObservability.realm`

**確認方法:**

1. Splunk Observability Cloud にログインします
2. **Settings** > **Account** に移動します
3. Realm が表示されます（例: `us0`、`us1`、`eu0`、`ap0`）

**一般的な Realm:**

- `us0` - US East (N. Virginia)
- `us1` - US East (Ohio)
- `eu0` - Europe (Frankfurt)
- `ap0` - Asia Pacific (Tokyo)

## 使用方法

プレースホルダーを置き換えた後、メインの [README.md](../README.md) に記載されているコマンドでこれらのファイルを使用します

```bash
# Create EKS cluster
eksctl create cluster -f examples/cluster.yaml

# Add node group
eksctl create nodegroup -f examples/nodegroup.yaml

# Install Cilium Enterprise
helm upgrade --install cilium isovalent/cilium \
  --version 1.18.4 \
  --namespace kube-system \
  -f examples/cilium-enterprise-values.yaml

# Install DNS Proxy HA
helm upgrade --install cilium-dns-proxy-ha isovalent/cilium-dns-proxy-ha \
  --version 1.18.0 \
  --namespace kube-system \
  -f examples/cilium-dns-proxy-ha-values.yaml

# Install Splunk OpenTelemetry Collector
helm upgrade --install splunk-otel-collector splunk-otel-collector-chart/splunk-otel-collector \
  --namespace otel-splunk \
  --create-namespace \
  -f examples/splunk-otel-isovalent.yaml
```

## メトリクスフィルタリング

`splunk-otel-isovalent.yaml` ファイルには、Splunk Observability Cloud に送信されるメトリクスを制限する `filter/includemetrics` プロセッサーが含まれています。このプロセッサーは**厳格なインクルードセマンティクス**を使用します`metric_names` に明示的にリストされたメトリクスのみが転送され、その他のメトリクスはすべてドロップされます。これは以下の理由で不可欠です

- **メトリクスの爆発的増加を防止**: Cilium、Hubble、Tetragon は数百のメトリクスを生成する可能性があります
- **コストの制御**: Splunk はメトリクスのボリューム（MTS - Metric Time Series）に基づいて課金されます
- **主要な指標に集中**: アクション可能なインサイトを提供するメトリクスのみを送信します

**デフォルトでフィルタリングされるメトリクス:**

- コンテナおよび Pod のリソースメトリクス（CPU、メモリ、再起動）
- Cilium ネットワーキングメトリクス（エンドポイント、BPF マップ、ポリシー、API リミッター）
- Hubble オブザーバビリティメトリクス（フロー、DNS、HTTP、ドロップ）
- Tetragon セキュリティメトリクス（プロセス、HTTP、DNS、ソケット）

**フィルターのカスタマイズ:**
監視要件に基づいてメトリクスを追加または削除するには、`processors.filter/includemetrics` 配下の `metric_names` リストを編集します。利用可能なメトリクスを確認するには `kubectl exec` を使用します

```bash
# View all Cilium metrics
kubectl exec -n kube-system ds/cilium -- curl -s localhost:9962/metrics | grep "^cilium_"

# View all Hubble metrics
kubectl exec -n kube-system ds/cilium -- curl -s localhost:9965/metrics | grep "^hubble_"

# View all Tetragon metrics
kubectl exec -n tetragon ds/tetragon -- curl -s localhost:2112/metrics | grep "^tetragon_"
```

## カスタマイズ

お使いの環境に合わせて、これらのファイルを自由に変更してください

- `cluster.yaml` と `nodegroup.yaml` でクラスター名とリージョンを変更する
- `nodegroup.yaml` でインスタンスタイプとキャパシティを調整する
- `cilium-enterprise-values.yaml` で Hubble メトリクスを変更する
- `splunk-otel-isovalent.yaml` でクラスター名をデプロイメントに合わせて更新する
- `splunk-otel-isovalent.yaml` で監視ニーズに基づいてメトリクスフィルターリストをカスタマイズする

## セキュリティベストプラクティス

1. **機密情報をバージョン管理にコミットしない**でください
2. 認証情報には**環境変数**または**シークレット管理ツール**（例: AWS Secrets Manager、HashiCorp Vault）を使用してください
3. アクセストークンを定期的にローテーションしてください
4. IAM ロールとサービスアカウントには**最小権限の原則**を使用してください
5. EKS と Splunk Observability Cloud の両方で**監査ログ**を有効にしてください
