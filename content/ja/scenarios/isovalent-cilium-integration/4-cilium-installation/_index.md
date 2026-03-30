---
title: Cilium のインストール
weight: 4
---

## ステップ 1: Cilium Enterprise の設定

`cilium-enterprise-values.yaml` という名前のファイルを作成します。`<YOUR-EKS-API-SERVER-ENDPOINT>` を前のステップで取得したエンドポイントに置き換えてください（`https://` プレフィックスは除きます）。

```yaml
# Enable/disable debug logging
debug:
  enabled: false
  verbose: ~

# Configure unique cluster name & ID
cluster:
  name: isovalent-demo
  id: 0

# Configure ENI specifics
eni:
  enabled: true
  updateEC2AdapterLimitViaAPI: true   # Dynamically fetch ENI limits from EC2 API
  awsEnablePrefixDelegation: true     # Assign /28 CIDR blocks per ENI (16 IPs) instead of individual IPs

enableIPv4Masquerade: false           # Pods use their real VPC IPs — no SNAT needed in ENI mode
loadBalancer:
  serviceTopology: true               # Prefer backends in the same AZ to reduce cross-AZ traffic costs

ipam:
  mode: eni

routingMode: native                   # No overlay tunnels — traffic routes natively through VPC

# BPF / KubeProxyReplacement
# Cilium replaces kube-proxy entirely with eBPF programs in the kernel.
# This requires a direct path to the API server, hence k8sServiceHost.
kubeProxyReplacement: "true"
k8sServiceHost: <YOUR-EKS-API-SERVER-ENDPOINT>
k8sServicePort: 443

# TLS for internal Cilium communication
tls:
  ca:
    certValidityDuration: 3650        # 10 years for the CA cert

# Hubble: network observability built on top of Cilium's eBPF datapath
hubble:
  enabled: true
  metrics:
    enableOpenMetrics: true           # Use OpenMetrics format for better Prometheus compatibility
    enabled:
      # DNS: query/response tracking with namespace-level label context
      - dns:labelsContext=source_namespace,destination_namespace
      # Drop: packet drop reasons (policy deny, invalid, etc.) per namespace
      - drop:labelsContext=source_namespace,destination_namespace
      # TCP: connection state tracking (SYN, FIN, RST) per namespace
      - tcp:labelsContext=source_namespace,destination_namespace
      # Port distribution: which destination ports are being used
      - port-distribution:labelsContext=source_namespace,destination_namespace
      # ICMP: ping/traceroute visibility with workload identity context
      - icmp:labelsContext=source_namespace,destination_namespace;sourceContext=workload-name|reserved-identity;destinationContext=workload-name|reserved-identity
      # Flow: per-workload flow counters (forwarded, dropped, redirected)
      - flow:sourceContext=workload-name|reserved-identity;destinationContext=workload-name|reserved-identity
      # HTTP L7: request/response metrics with full workload context and exemplars for trace correlation
      - "httpV2:exemplars=true;labelsContext=source_ip,source_namespace,source_workload,destination_namespace,destination_workload,traffic_direction;sourceContext=workload-name|reserved-identity;destinationContext=workload-name|reserved-identity"
      # Policy: network policy verdict tracking (allowed/denied) per workload
      - "policy:sourceContext=app|workload-name|pod|reserved-identity;destinationContext=app|workload-name|pod|dns|reserved-identity;labelsContext=source_namespace,destination_namespace"
      # Flow export: enables Hubble to export flow records to Timescape for historical storage
      - flow_export
    serviceMonitor:
      enabled: true                   # Creates a Prometheus ServiceMonitor for auto-discovery
  tls:
    enabled: true
    auto:
      enabled: true
      method: cronJob                 # Automatically rotate Hubble TLS certs on a schedule
      certValidityDuration: 1095      # 3 years per cert rotation
  relay:
    enabled: true                     # Hubble Relay aggregates flows from all nodes cluster-wide
    tls:
      server:
        enabled: true
    prometheus:
      enabled: true
      serviceMonitor:
        enabled: true
  timescape:
    enabled: true                     # Stores historical flow data for time-travel debugging

# Cilium Operator: cluster-wide identity and endpoint management
operator:
  prometheus:
    enabled: true
    serviceMonitor:
      enabled: true

# Cilium Agent: per-node eBPF datapath metrics
prometheus:
  enabled: true
  serviceMonitor:
    enabled: true

# Cilium Envoy: L7 proxy metrics (HTTP, gRPC)
envoy:
  prometheus:
    enabled: true
    serviceMonitor:
      enabled: true

# Enable the Cilium agent to hand off DNS proxy responsibilities to the
# external DNS Proxy HA deployment, so policies keep working during upgrades
extraConfig:
  external-dns-proxy: "true"

# Enterprise feature gates — these must be explicitly approved
enterprise:
  featureGate:
    approved:
      - DNSProxyHA          # High-availability DNS proxy (installed separately)
      - HubbleTimescape     # Historical flow storage via Timescape
```

{{% notice title="ラベルコンテキストが重要な理由" style="info" %}}
各Hubbleメトリクスの `labelsContext` および `sourceContext`/`destinationContext` パラメータは、メトリクスをどのディメンションで分割するかを制御します。`labelsContext=source_namespace,destination_namespace` を設定すると、すべてのメトリクスにこれら2つのラベルが付与され、カーディナリティの爆発を起こすことなくSplunkでnamespaceによるフィルタリングが可能になります。`workload-name|reserved-identity` のフォールバックチェーンは、利用可能な場合はワークロード名を使用し、利用できない場合はセキュリティIDにフォールバックすることを意味します。
{{% /notice %}}

## ステップ 2: Cilium Enterprise のインストール

新しいノードがEKSクラスターに参加すると、そのノードのkubeletはすぐにCNIプラグインを探してネットワーキングをセットアップします。`/etc/cni/net.d/` に存在するCNI設定を読み取り、それを使用してノードを初期化します。**ノードグループを先に作成すると、AWS VPC CNI が最初に到達します** — そして一度ノードが特定のCNIで初期化されると、別のCNIに切り替えるにはノードをドレインして再初期化する必要があります。

ノードが存在する前にCiliumをインストールすることで、CiliumのCNI設定が `kube-system` に既に存在し、ノードが起動した瞬間にピックアップされる準備ができていることを保証します。EC2インスタンスが起動すると、CiliumのDaemonSet Podがすぐにスケジュールされ、eBPFプログラムがロードされ、ノードは最初の瞬間からCiliumの制御下で `Ready` 状態になります。

これは、EKSセットアップのステップ3でクラスターが `disableDefaultAddons: true` で作成された理由でもあります — これがないと、AWS VPC CNIが自動的にインストールされ、Ciliumと競合することになります。

Helmを使用してCiliumをインストールします：

```bash
helm install cilium isovalent/cilium --version 1.18.4 \
  --namespace kube-system -f cilium-enterprise-values.yaml
```

{{% notice title="Pending状態のジョブは正常です" style="warning" %}}
インストール後、いくつかのジョブがPending状態になっているのが見えます — これは正常です。CiliumのHelmチャートにはHubble用のTLS証明書を生成するジョブが含まれており、そのジョブを実行するにはノードが必要です。次のステップでノードが利用可能になると、自動的に完了します。
{{% /notice %}}

## ステップ 3: ノードグループの作成

`nodegroup.yaml` という名前のファイルを作成します：

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: isovalent-demo
  region: us-east-1
managedNodeGroups:
- name: standard
  instanceType: m5.xlarge
  desiredCapacity: 2
  privateNetworking: true
```

ノードグループを作成します（5〜10分かかります）：

```bash
eksctl create nodegroup -f nodegroup.yaml
```

## ステップ 4: Cilium インストールの確認

ノードの準備ができたら、すべてのコンポーネントを確認します：

```bash
# Check nodes
kubectl get nodes

# Check Cilium pods
kubectl get pods -n kube-system -l k8s-app=cilium

# Check all Cilium components
kubectl get pods -n kube-system | grep -E "(cilium|hubble)"
```

**期待される出力：**

- 2つのノードが `Ready` 状態
- Cilium Podが実行中（ノードごとに1つ）
- Hubble relayとtimescapeが実行中
- Cilium operatorが実行中

## ステップ 5: 拡張ネットワークオブザーバビリティを備えた Tetragon のインストール

Tetragonはそのままでもランタイムセキュリティとプロセスレベルの可視性を提供します。Splunkとの統合 — 特にNetwork Explorerダッシュボード — には、TCP/UDPソケット統計、RTT、接続イベント、DNSをカーネルレベルで追跡する拡張ネットワークオブザーバビリティモードも有効にする必要があります。

`tetragon-network-values.yaml` という名前のファイルを作成します：

```yaml
# Tetragon configuration with Enhanced Network Observability enabled
# Required for Splunk Observability Cloud Network Explorer integration

tetragon:
  # Enable network events — this activates eBPF-based socket tracking
  enableEvents:
    network: true

  # Layer3 settings: track TCP, UDP, and ICMP with RTT and latency
  # These enable the socket stats metrics (srtt, retransmits, bytes, etc.)
  layer3:
    tcp:
      enabled: true
      rtt:
        enabled: true     # Round-trip time per TCP flow
    udp:
      enabled: true
    icmp:
      enabled: true
    latency:
      enabled: true       # Per-connection latency tracking

  # DNS tracking at the kernel level (complements Hubble DNS metrics)
  dns:
    enabled: true

  # Expose Tetragon metrics via Prometheus
  prometheus:
    enabled: true
    serviceMonitor:
      enabled: true

  # Filter out noise from internal system namespaces — we only care about
  # application workloads, not the observability stack itself
  exportDenyList: |-
    {"health_check":true}
    {"namespace":["", "cilium", "tetragon", "kube-system", "otel-splunk"]}

  # Only include labels that are meaningful for the Network Explorer
  metricsLabelFilter: "namespace,workload,binary"

  resources:
    limits:
      cpu: 500m
      memory: 1Gi
    requests:
      cpu: 100m
      memory: 256Mi

# Enable the Tetragon Operator and TracingPolicy support.
# With tracingPolicy.enabled: true, the operator manages and deploys
# TracingPolicies (TCP connection tracking, HTTP visibility, etc.) automatically.
tetragonOperator:
  enabled: true
  tracingPolicy:
    enabled: true
```

これらの値でTetragonをインストールします：

```bash
helm install tetragon isovalent/tetragon --version 1.18.0 \
  --namespace tetragon --create-namespace \
  -f tetragon-network-values.yaml
```

インストールを確認します：

```bash
kubectl get pods -n tetragon
```

**表示される内容：** TetragonはDaemonSet（ノードごとに1つのPod）とオペレーターとして実行されます。

{{% notice title="拡張ネットワークオブザーバビリティが追加するもの" style="info" %}}
`layer3.tcp.rtt.enabled: true` を設定すると、TetragonはカーネルのTCPソケット状態にフックし、ラウンドトリップタイム、再送回数、送受信バイト数、セグメント数を含む接続ごとのメトリクスを記録します。これらはSplunkのNetwork Explorerのレイテンシとスループットビューを動かす `tetragon_socket_stats_*` メトリクスに供給されます。これがないとイベントカウントのみが取得されますが、これがあると接続品質データが取得できます。

TracingPolicies（TCP接続追跡、HTTP可視性など）は、上記のHelm valuesで `tetragonOperator.tracingPolicy.enabled: true` が設定されている場合、Tetragon Operatorによって自動的に管理されます。
{{% /notice %}}

## ステップ 6: Cilium DNS Proxy HA のインストール

`cilium-dns-proxy-ha-values.yaml` という名前のファイルを作成します：

```yaml
enableCriticalPriorityClass: true
metrics:
  serviceMonitor:
    enabled: true
```

DNS Proxy HAをインストールします：

```bash
helm upgrade -i cilium-dnsproxy isovalent/cilium-dnsproxy --version 1.16.7 \
  -n kube-system -f cilium-dns-proxy-ha-values.yaml
```

確認します：

```bash
kubectl rollout status -n kube-system ds/cilium-dnsproxy --watch
```

{{% notice title="成功" style="success" %}}
これでCilium CNI、Hubbleオブザーバビリティ、Tetragonセキュリティを備えた完全に機能するEKSクラスターが完成しました！
{{% /notice %}}
