---
title: ワークショップの概要
linkTitle: 1. ワークショップの概要
weight: 1
archetype: chapter
time: 5 minutes
description: OBI ワークショップの目標、前提条件、アーキテクチャ。
---

## 学習内容

このワークショップを終えると、以下のことができるようになります:

- eBPFがLinuxカーネルレベルでゼロコード計装をどのように実現するかを理解する
- ベアホスト上でOBIバイナリを使用して実行中のアプリケーションを計装する
- Docker Composeでポリグロットマイクロサービススタックをデプロイし、1つのコンテナで分散トレーシングを追加する
- Splunk OTel Collector Helm chartを使用して同じスタックをKubernetesにデプロイし、1つのフラグでOBIを有効にする
- Splunk APMで分散トレース、サービスマップ、リクエストフローを確認する

## 前提条件

ワークショップインスタンスには必要なものがすべて事前設定されています:

| 要件 | ワークショップインスタンスでの状態 |
|---|---|
| Linux ホスト | 提供済み (Ubuntu) |
| Python 3.9+ | インストール済み |
| Docker & Docker Compose | インストール済み |
| K3s (Kubernetes) | インストール済み |
| kubectl | インストール済み |
| Helm 3 | インストール済み |
| ワークショップアセット | `~/workshop/obi/` にデプロイ済み |

以下も必要です:

| 要件 | 取得方法 |
|---|---|
| Splunk Observability Cloud アカウント | インストラクターから提供されます |
| **Splunk Access Token** (Ingest) | インスタンスで `env` と入力し、`ACCESS_TOKEN` を探してください |
| **Splunk Realm** (例: `us0`, `us1`, `eu0`) | インスタンスで `env` と入力し、`REALM` を探してください |
| **ユニークな名前** (例: `shw-2c74`) | `env` で `INSTANCE` を探してください。`host.name` として使用されます |

## アーキテクチャ

このワークショップでは、リクエストチェーンを形成する3つのシンプルなマイクロサービスを使用します:

```text
Frontend (Node.js :3000)  →  Order-Processor (Go :8080)  →  Payment-Service (Go :8081)
```

これらのサービスには**オブザーバビリティコードが一切ありません** -- OpenTelemetry SDKも、トレーシングヘッダーも、いかなる種類の計装もありません。OBIはeBPFプローブを使用してカーネルからこれらを計装し、OpenTelemetry互換のトレースを生成し、Splunk OTel Collectorに送信します。CollectorはそれをSplunk Observability Cloudに転送します。

## OBI とは?

[OBI (OpenTelemetry eBPF Instrumentation)](https://opentelemetry.io/docs/zero-code/obi/) は、LinuxカーネルのeBPFプローブを使用してアプリケーションを流れるHTTP/gRPCトラフィックを観測するスタンドアロンエージェントです。**カーネルから**プロセスにアタッチします -- SDKも、コード変更も、再コンパイルも不要です。リクエストを検知し、OpenTelemetry互換のトレーススパンを生成し、Collectorに送信します。

これはSDKでの計装が**できない**、または**しない**組織にとって価値があります:

- ソースアクセスのないレガシーシステム
- 再コンパイルがオプションにないコンパイル言語
- 開発者の抵抗（「計装を追加する時間がない」）
- コード変更がフル監査サイクルをトリガーする規制上の制約

## 価値提案

多くの組織には、OpenTelemetry SDKでの計装が**できない**、または**しない**アプリケーションがあります:

- **レガシーシステム**: COBOLからJavaへの移行、10年前の .NET Frameworkアプリ、ソースアクセスのないベンダー提供バイナリ
- **コンパイル言語**: 再コンパイルがオプションにない、またはチームが離れてしまったGo、Rust、C++ サービス
- **開発者の抵抗**:「時間がない」、「スプリントに含まれていない」、「動作しているコードは変更しない」
- **規制上の制約**: コード変更がフル監査/認証サイクルをトリガーする

OBIは**コード変更なしで完全な分散トレーシング**を提供します:

- **SDK 統合ゼロ** -- インポートなし、依存関係なし、コンパイル時の変更なし
- **アプリケーション再起動ゼロ** -- OBIはeBPF経由で既に実行中のプロセスにアタッチします
- **言語非依存** -- Go、Node.js、Python、Java、Rust、C++ -- HTTPまたはgRPCを話すものなら何でも動作します
- **1つのコンテナまたは1つの Helm フラグ** -- composeに追加するか、Helm chartで `obi.enabled=true` を有効にするだけで完了です
