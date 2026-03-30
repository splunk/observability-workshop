---
title: 4. スケーリングの仕組み
weight: 4
---

## 環境間で共通するパターン

フェーズ0ではバイナリを実行しました。フェーズ2（Docker）では1つのコンテナを追加しました。フェーズ3（K8s）では `helm upgrade` を1回実行しました。パターンは同じです：

| 環境 | OBI のデプロイ方法 | 変更点 |
|---|---|---|
| ベアホスト | `sudo` でバイナリを実行 | なし -- OBI はカーネルからプロセスを監視します |
| Docker Compose | 1 つのコンテナ | `docker-compose.yaml` にサービスを追加 |
| Kubernetes | Helm chart フラグ | `--set="obi.enabled=true"` を指定して `helm upgrade` |

[Splunk OTel Collector Helm chart](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/docs/zero-code-ebpf-instrumentation.md) は、コレクターとOBIの両方を本番環境にデプロイするための方法です。さらに自動化を進めるには、[OpenTelemetry Operator](https://opentelemetry.io/docs/kubernetes/operator/) を使用して、アノテーションによりOBIをサイドカーとして自動的に注入できます。

## 価値提案（まとめ）

多くの組織には、OpenTelemetry SDKで計装**できない**、または**しない**アプリケーションがあります：

- **レガシーシステム**: COBOLからJavaへの移行、10年以上前の .NET Frameworkアプリ、ソースコードにアクセスできないベンダー提供のバイナリ
- **コンパイル言語**: Go、Rust、C++ サービスで、再コンパイルができない場合やチームがすでに異動している場合
- **開発者の抵抗**:「時間がない」「スプリントに入っていない」「動いているコードは変えたくない」
- **規制上の制約**: コード変更があると完全な監査/認証サイクルが必要になる

OBIは**コード変更なしで完全な分散トレーシング**を提供します：

- **SDK 統合ゼロ** -- インポートなし、依存関係なし、コンパイル時の変更なし
- **アプリケーション再起動ゼロ** -- OBIはeBPFを介して実行中のプロセスにアタッチします
- **言語に依存しない** -- Go、Node.js、Python、Java、Rust、C++ などHTTPまたはgRPCを使用するあらゆる言語で動作します
- **1 つのコンテナまたは 1 つの Helm フラグ** -- composeに追加するか、Helm chartで `obi.enabled=true` を有効にするだけで完了です
