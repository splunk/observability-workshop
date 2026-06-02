---
title: 4. スケーリングの仕組み
weight: 4
---

## 環境を横断するパターン

Phase 0 ではバイナリを実行しました。Phase 2 (Docker) ではコンテナを 1 つ追加しました。Phase 3 (K8s) では `helm upgrade` を 1 回実行しました。パターンは同じです。

| 環境 | OBI のデプロイ | 変更内容 |
|---|---|---|
| ベアホスト | `sudo` 経由のバイナリ | 何も変えない: OBI がカーネルからプロセスを監視 |
| Docker Compose | コンテナ 1 つ | `docker-compose.yaml` にサービスを追加 |
| Kubernetes | Helm chart のフラグ | `helm upgrade` を `--set="obi.enabled=true"` で実行 |

[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/zero-code-ebpf-instrumentation.md) は、collector と OBI の両方をデプロイする本番向けの方法です。さらなる自動化のために、[OpenTelemetry Operator](https://opentelemetry.io/docs/kubernetes/operator/) はアノテーションを使って OBI をサイドカーとして自動的にインジェクトできます。

## 価値の整理

多くの組織には、OpenTelemetry SDK で計装**できない**、または計装**したくない**アプリケーションがあります。

- **レガシーシステム**: COBOL から Java への移行、10 年前の .NET Framework アプリ、ソースコードにアクセスできないベンダー提供のバイナリ
- **コンパイル言語**: Go、Rust、C++ のサービスで、再コンパイルが選択肢にない、もしくはチームが既に他へ移っている
- **開発者の抵抗**: 「時間がない」「スプリントに入っていない」「動いているコードは変えない」
- **規制上の制約**: コードを変更すると監査・認証サイクル全体が再走する

OBI は**コード変更なしで完全な分散トレーシング**を提供します。

- **SDK 統合不要**: import なし、依存関係なし、コンパイル時の変更なし
- **アプリケーションの再起動不要**: OBI は eBPF を介して既に動作中のプロセスにアタッチ
- **言語非依存**: HTTP または gRPC を話すものなら Go、Node.js、Python、Java、Rust、C++ で動作
- **コンテナ 1 つ、または Helm のフラグ 1 つ**: compose に追加するか Helm chart で `obi.enabled=true` を有効化すれば完了

## 環境によっては obi/eBPF の設定にカスタマイズが必要な場合があります

OpenShift などのケースでは、obi の設定に追加情報が必要になることがあります。
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
