---
title: 4. スケーリングの仕組み
weight: 4
---

## 環境間のパターン

Phase 0 ではバイナリを実行しました。Phase 2（Docker）ではコンテナを1つ追加しました。Phase 3（K8s）では `helm upgrade` を1回実行しました。パターンは同じです

| 環境 | OBI デプロイメント | 変更点 |
|---|---|---|
| ベアホスト | `sudo` によるバイナリ | なし：OBI はカーネルからプロセスを監視します |
| Docker Compose | コンテナ1つ | `docker-compose.yaml` にサービスを追加 |
| Kubernetes | Helm chart フラグ | `--set="obi.enabled=true"` で `helm upgrade` |

[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/zero-code-ebpf-instrumentation.md) は、コレクターと OBI の両方をデプロイするための本番環境向けの方法です。さらなる自動化のために、[OpenTelemetry Operator](https://opentelemetry.io/docs/kubernetes/operator/) はアノテーションを使用して OBI をサイドカーとして自動的に注入できます。

## 価値提案（まとめ）

多くの組織には、OpenTelemetry SDK での計装が**できない**、または**しない**アプリケーションがあります

- **レガシーシステム**: COBOL から Java への移行、10年前の .NET Framework アプリ、ソースアクセスのないベンダー提供のバイナリ
- **コンパイル言語**: Go、Rust、C++ サービスで、再コンパイルが選択肢にないか、チームが離れてしまった場合
- **開発者の抵抗**: 「時間がない」、「スプリントに入っていない」、「動いているコードは変えない」
- **規制上の制約**: コードの変更が完全な監査/認証サイクルをトリガーする

OBI は**コード変更なしで完全な分散トレーシング**を提供します

- **SDK 統合ゼロ**: インポートなし、依存関係なし、コンパイル時の変更なし
- **アプリケーション再起動ゼロ**: OBI は eBPF を介して実行中のプロセスにアタッチします
- **言語非依存**: Go、Node.js、Python、Java、Rust、C++ など、HTTP または gRPC を使用するすべてのものに対応
- **コンテナ1つまたは Helm フラグ1つ**: compose に追加するか、Helm chart で `obi.enabled=true` を有効にすれば完了です

## 環境によっては obi/eBPF 設定のカスタマイズが必要な場合があります

OpenShift などの場合、obi 設定に追加情報が必要になることがあります。
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
