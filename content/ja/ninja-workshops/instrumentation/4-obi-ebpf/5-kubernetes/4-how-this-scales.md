---
title: 4. スケーリングの仕組み
weight: 4
---

## 環境間で共通するパターン

Phase 0ではバイナリを実行しました。Phase 2（Docker）ではコンテナを1つ追加しました。Phase 3（K8s）では `helm upgrade` を1回実行しました。パターンは同じです。

| 環境 | OBIのデプロイ | 変更点 |
|---|---|---|
| ベアホスト | `sudo` 経由のバイナリ | なし: OBIはカーネルからプロセスを監視 |
| Docker Compose | コンテナ1つ | `docker-compose.yaml` にサービスを追加 |
| Kubernetes | Helmチャートフラグ | `helm upgrade` で `--set="obi.enabled=true"` を指定 |

[Splunk OTel Collector Helmチャート](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/zero-code-ebpf-instrumentation.md)は、CollectorとOBIの両方をデプロイする本番環境向けの方法です。さらに自動化するには、[OpenTelemetry Operator](https://opentelemetry.io/docs/kubernetes/operator/)がアノテーションを使用してOBIをサイドカーとして自動的に挿入できます。

## 価値提案（まとめ）

多くの組織には、OpenTelemetry SDKで計装 **できない** または **しない** アプリケーションがあります。

- **レガシーシステム**: COBOLからJavaへの移行、10年以上前の.NET Frameworkアプリ、ソースアクセスのないベンダー提供バイナリ
- **コンパイル言語**: Go、Rust、C++サービスで再コンパイルが選択肢にない、またはチームが離れている場合
- **開発者の抵抗**: 「時間がない」「スプリントに入っていない」「動いているコードは変えない」
- **規制上の制約**: コード変更が完全な監査/認証サイクルをトリガーする

OBIは **コード変更なしで完全な分散トレーシング** を提供します。

- **SDKの統合不要**: インポートなし、依存関係なし、コンパイル時の変更なし
- **アプリケーションの再起動不要**: OBIはeBPFを介して実行中のプロセスにアタッチ
- **言語非依存**: Go、Node.js、Python、Java、Rust、C++など、HTTPまたはgRPCを使用するすべてのものに対応
- **コンテナ1つまたはHelmフラグ1つ**: composeに追加するか、Helmチャートで `obi.enabled=true` を有効にするだけで完了

## 環境によってはobi/eBPF設定のカスタマイズが必要な場合があります

OpenShiftなどの場合、obi設定に追加情報が必要になることがあります。
この例を提供してくれたLeandro de Oliveira e Ferreiraに感謝します！

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
