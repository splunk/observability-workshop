---
title: ワークショップ概要
linkTitle: 1. ワークショップ概要
weight: 1
archetype: chapter
time: 5 minutes
description: OBI ワークショップの目標、前提条件、およびアーキテクチャ。
---

## 学習内容

このワークショップを終了すると、以下のことができるようになります

- eBPF が Linux カーネルレベルでゼロコード計装を可能にする仕組みを理解する
- ベアホスト上で OBI バイナリを使用して実行中のアプリケーションを計装する
- Docker Compose でポリグロット（複数言語）マイクロサービススタックをデプロイし、1つのコンテナで分散トレーシングを追加する
- Splunk OTel Collector Helm chart を使用して同じスタックを Kubernetes にデプロイし、1つのフラグで OBI を有効にする
- Splunk APM で分散トレース、サービスマップ、リクエストフローを表示する

## 前提条件

ワークショップインスタンスには必要なものがすべて事前設定されています

| 要件 | ワークショップインスタンスでの状態 |
|---|---|
| Linux ホスト | 提供済み（Ubuntu） |
| Python 3.9+ | インストール済み |
| Docker & Docker Compose | インストール済み |
| K3s (Kubernetes) | インストール済み |
| kubectl | インストール済み |
| Helm 3 | インストール済み |
| ワークショップアセット | `~/workshop/obi/` にデプロイ済み |

以下も必要です

| 要件 | 取得方法 |
|---|---|
| Splunk Observability Cloud アカウント | インストラクターから提供されます |
| **Splunk Access Token**（Ingest） | インスタンスで `env` と入力し、`ACCESS_TOKEN` を探してください |
| **Splunk Realm**（例`us0`、`us1`、`eu0`） | インスタンスで `env` と入力し、`REALM` を探してください |
| **ユニークな名前**（例`shw-2c74`） | `env` で `INSTANCE` を探してください。`host.name` として使用されます |

## アーキテクチャ

このワークショップでは、リクエストチェーンを形成する3つのシンプルなマイクロサービスを使用します

```text
Frontend (Node.js :3000)  →  Order-Processor (Go :8080)  →  Payment-Service (Go :8081)
```

これらのサービスには**オブザーバビリティコードがまったくありません** - OpenTelemetry SDK なし、トレーシングヘッダーなし、いかなる種類の計装もありません。OBI は eBPF プローブを使用してカーネルからこれらを計装し、OpenTelemetry 互換のトレースを生成して Splunk OTel Collector に送信し、そこから Splunk Observability Cloud に転送されます。

## OBI とは？

[OBI (OpenTelemetry eBPF Instrumentation)](https://opentelemetry.io/docs/zero-code/obi/) は、Linux カーネルの eBPF プローブを使用してアプリケーションを流れる HTTP/gRPC トラフィックを監視するスタンドアロンエージェントです。**カーネルから**プロセスにアタッチします - SDK なし、コード変更なし、再コンパイルなし。リクエストを監視し、OpenTelemetry 互換のトレーススパンを生成して、コレクターに送信します。

これは、SDK で計装**できない**または計装**したくない**組織にとって価値があります

- ソースアクセスのないレガシーシステム
- 再コンパイルができないコンパイル言語
- 開発者の抵抗（「計装を追加する時間がない」）
- コード変更がフル監査サイクルをトリガーする規制上の制約

## 価値提案

多くの組織には、OpenTelemetry SDK で計装**できない**または計装**したくない**アプリケーションがあります

- **レガシーシステム**：COBOL から Java への移行、10年以上前の .NET Framework アプリ、ソースアクセスのないベンダー提供バイナリ
- **コンパイル言語**：再コンパイルができない、またはチームが離れてしまった Go、Rust、C++ サービス
- **開発者の抵抗**：「時間がない」、「スプリントに入っていない」、「動いているコードは変更しない」
- **規制上の制約**：コード変更がフル監査/認証サイクルをトリガーする

OBI は**コード変更なしで完全な分散トレーシング**を提供します

- **SDK 統合ゼロ**：インポートなし、依存関係なし、コンパイル時の変更なし
- **アプリケーション再起動ゼロ**：OBI は eBPF 経由で既に実行中のプロセスにアタッチします
- **言語に依存しない**：Go、Node.js、Python、Java、Rust、C++、または HTTP や gRPC を使用するあらゆるものに対応
- **1つのコンテナまたは1つの Helm フラグ**：compose に追加するか、Helm chart で `obi.enabled=true` を有効にするだけで完了
