---
title: 4. スケーリングの仕組み
weight: 4
---

## 環境全体に共通するパターン

フェーズ0ではバイナリを実行しました。フェーズ2（Docker）ではコンテナを1つ追加しました。フェーズ3（K8s）では `helm upgrade` を1回実行しました。パターンは同じです

| 環境 | OBI のデプロイ | 変更内容 |
|---|---|---|
| ベアホスト | `sudo` 経由のバイナリ | 変更なし：OBI はカーネルからプロセスを監視します |
| Docker Compose | コンテナ1つ | `docker-compose.yaml` にサービスを追加 |
| Kubernetes | Helm chart フラグ | `helm upgrade` で `--set="obi.enabled=true"` を指定 |

[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/zero-code-ebpf-instrumentation.md) は、コレクターと OBI の両方を本番環境にデプロイするための方法です。さらなる自動化のために、[OpenTelemetry Operator](https://opentelemetry.io/docs/kubernetes/operator/) はアノテーションを使用して OBI をサイドカーとして自動的にインジェクトすることができます。

## 価値提案（まとめ）

多くの組織には、OpenTelemetry SDK で計装**できない**、または**しない**アプリケーションがあります

- **レガシーシステム**: COBOL から Java への移行、10年以上前の .NET Framework アプリ、ソースアクセスのないベンダー提供のバイナリ
- **コンパイル言語**: Go、Rust、C++ のサービスで、再コンパイルができない、またはチームがすでに離れている場合
- **開発者の抵抗**: 「時間がない」「スプリントに入っていない」「動いているコードは変えたくない」
- **規制上の制約**: コード変更により完全な監査/認証サイクルが発生する場合

OBI は**コード変更なしで完全な分散トレーシング**を提供します

- **SDK 統合不要**: インポート不要、依存関係不要、コンパイル時の変更不要
- **アプリケーションの再起動不要**: OBI は eBPF を介して実行中のプロセスにアタッチします
- **言語に依存しない**: Go、Node.js、Python、Java、Rust、C++ など、HTTP または gRPC を使用するあらゆる言語で動作します
- **コンテナ1つまたは Helm フラグ1つ**: compose に追加するか、Helm chart で `obi.enabled=true` を有効にするだけで完了です

## 環境によっては obi/eBPF 設定のカスタマイズが必要な場合があります

OpenShift などの場合、obi の設定に追加情報が必要になることがあります。
この例を提供してくれた Leandro de Oliveira e Ferreira に感謝します！

```
# obi-scc.yaml
apiVersion: security.openshift.io/v1
kind: SecurityContextConstraints
metadata:
  name: splunk-otel-obi-scc
allowPrivilegedContainer: true
allowHostPID: true
allowHostDirVolumePlugin: true
allowHostNetwork: true
allowHostPorts: true
allowPrivilegeEscalation: true
readOnlyRootFilesystem: false
runAsUser:
  type: RunAsAny
seLinuxContext:
  type: RunAsAny
fsGroup:
  type: RunAsAny
supplementalGroups:
  type: RunAsAny
volumes:
  - configMap
  - emptyDir
  - hostPath
  - secret
  - projected
allowedCapabilities:
  - BPF
  - PERFMON
  - SYS_PTRACE
  - DAC_READ_SEARCH
  - NET_ADMIN
  - NET_RAW
  - CHECKPOINT_RESTORE
  - SYS_ADMIN
users: []
```
