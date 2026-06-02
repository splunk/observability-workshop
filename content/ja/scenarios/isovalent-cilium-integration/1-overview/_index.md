---
title: 概要
weight: 1
---

## Isovalent Enterprise Platform とは？

Isovalent Enterprise Platform は、eBPF (Extended Berkeley Packet Filter) 技術に基づいて構築された3つのコアコンポーネントで構成されています

### Cilium

#### クラウドネイティブ CNI とネットワークセキュリティ

- Kubernetes 向けの eBPF ベースのネットワーキングとセキュリティ
- kube-proxy を高性能な eBPF データパスに置き換え
- AWS ENI モードのネイティブサポート（Pod が VPC IP アドレスを取得）
- L3-L7 でのネットワークポリシーの適用
- 透過的な暗号化とロードバランシング

### Hubble

#### ネットワークオブザーバビリティ

- Cilium の eBPF 可視性の上に構築
- リアルタイムのネットワークフロー監視
- L7 プロトコルの可視性（HTTP、DNS、gRPC、Kafka）
- フローのエクスポートと履歴データストレージ（Timescape）
- ポート 9965 でメトリクスを公開

### Tetragon

#### ランタイムセキュリティとオブザーバビリティ

- eBPF ベースのランタイムセキュリティ
- プロセス実行の監視
- システムコールのトレース
- ファイルアクセスの追跡
- ポート 2112 でのセキュリティイベントメトリクス

## アーキテクチャ

{{< mermaid >}}
graph TB
    subgraph AWS["Amazon Web Services"]
        subgraph EKS["EKS Cluster"]
            subgraph Node["Worker Node"]
                CA["Cilium Agent:9962"]
                CE["Cilium Envoy:9964"]
                HA["Hubble:9965"]
                TE["Tetragon:2112"]
                OC["OTel Collector"]
            end
            CO["Cilium Operator:9963"]
            HR["Hubble Relay"]
        end
    end
    subgraph Splunk["Splunk Observability Cloud"]
        IM["Infrastructure Monitoring"]
        DB["Dashboards"]
    end
    CA -.->|"Scrape"| OC
    CE -.->|"Scrape"| OC
    HA -.->|"Scrape"| OC
    TE -.->|"Scrape"| OC
    CO -.->|"Scrape"| OC
    OC ==>|"OTLP/HTTP"| IM
    IM --> DB
{{< /mermaid >}}

## 主要コンポーネント

| コンポーネント | サービス名 | ポート | 用途 |
| --------- | ------------ | ---- | ------- |
| Cilium Agent | cilium-agent | `9962` | CNI、ネットワークポリシー、eBPF プログラム |
| Cilium Envoy | cilium-envoy | `9964` | HTTP、gRPC 用の L7 プロキシ |
| Cilium Operator | cilium-operator | `9963` | クラスタ全体のオペレーション |
| Hubble | hubble-metrics | `9965` | ネットワークフローメトリクス |
| Tetragon | tetragon | `2112` | ランタイムセキュリティメトリクス |

## eBPF のメリット

- **高性能**: 最小限のオーバーヘッドで Linux カーネル内で実行されます
- **安全性**: ベリファイアがプログラムの安全な実行を保証します
- **柔軟性**: カーネルモジュールなしで動的なインストルメンテーションが可能です
- **可視性**: ネットワークとシステムの動作に対する深い洞察を提供します

{{% notice title="注意" style="info" %}}
この統合により、従来の CNI プラグインでは不可能なレベルで Kubernetes ネットワーキングの可視性が提供されます。
{{% /notice %}}
