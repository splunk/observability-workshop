---
title: 4. How This Scales
weight: 4
---

## 環境全体を通じたパターン

Phase 0 ではバイナリを実行しました。Phase 2（Docker）ではコンテナを1つ追加しました。Phase 3（K8s）では `helm upgrade` を1回実行しました。パターンは同じです

| 環境 | OBI のデプロイ方法 | 変更点 |
|---|---|---|
| ベアホスト | `sudo` でバイナリを実行 | なし：OBI はカーネルからプロセスを監視 |
| Docker Compose | コンテナを1つ追加 | `docker-compose.yaml` にサービスを追加 |
| Kubernetes | Helm chart フラグ | `--set="obi.enabled=true"` で `helm upgrade` |

[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/zero-code-ebpf-instrumentation.md) は、コレクターと OBI の両方をデプロイする本番環境向けの方法です。さらに自動化するには、[OpenTelemetry Operator](https://opentelemetry.io/docs/kubernetes/operator/) を使用してアノテーションで OBI をサイドカーとして自動的に注入できます。

## 価値提案（まとめ）

多くの組織には、OpenTelemetry SDK で計装**できない**、または**しない**アプリケーションがあります

- **レガシーシステム**: COBOL から Java への移行、10年前の .NET Framework アプリ、ソースにアクセスできないベンダー提供のバイナリ
- **コンパイル言語**: 再コンパイルがオプションではない、またはチームが離れた Go、Rust、C++ サービス
- **開発者の抵抗**: 「時間がない」「スプリントにない」「動いているコードは変えない」
- **規制上の制約**: コード変更があると完全な監査/認証サイクルが発生する

OBI は**コード変更なしで完全な分散トレーシング**を提供します

- **SDK 統合ゼロ**: インポートなし、依存関係なし、コンパイル時の変更なし
- **アプリケーション再起動ゼロ**: OBI は eBPF を介して既に実行中のプロセスにアタッチ
- **言語非依存**: HTTP または gRPC を使用する Go、Node.js、Python、Java、Rust、C++ など何でも動作
- **コンテナ1つまたは Helm フラグ1つ**: compose に追加するか、Helm chart で `obi.enabled=true` を有効にするだけで完了
