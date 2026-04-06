---
title: ワークショップ概要
linkTitle: 1. Overview
weight: 1
archetype: chapter
time: 5 minutes
description: ユースケース、アーキテクチャ、前提条件、および hybrid mode と dual signal mode の違いについて説明します。
---

## ユースケース

あなたの組織では現在、APM として AppDynamics を運用しています。データの可視化とガバナンスの取り組みの一環として、経営層はアプリケーションパフォーマンスデータを **Splunk Observability Cloud** にも送信し、すでに Splunk に取り込まれているインフラストラクチャメトリクス、ログ、その他のシグナルと統合されたビューをチームに提供したいと考えています。

すべてのサービスを個別の OpenTelemetry SDK で再計装するのではなく、AppDynamics Java Agent は **dual signal mode** をサポートしています。これにより、単一のエージェントが AppDynamics APM データと OpenTelemetry トレースの両方を同時に生成できます。これにより、AppDynamics の完全な機能を維持しながら、OpenTelemetry Collector を通じて同じテレメトリを Splunk Observability Cloud にストリーミングできます。

これは、現在 AppDynamics を熟知し依存している L1 および L2 チームにとって特に有用です。Dual ingest は、彼らが担当するアプリケーションやサービスがクラウドの SaaS プラットフォームでホストされる新しいサービスとより密接に接続されるようになっても、コンテキストを維持するのに役立ちます。

## 学習内容

このワークショップを完了すると、以下のことができるようになります

- AppDynamics Java Agent を使用してシンプルな Java サービスをビルドして実行する
- **hybrid mode** と **dual signal mode** の違いを理解する
- dual signal mode を有効にして、APM データを AppDynamics と Splunk Observability Cloud の両方に送信する
- 両方のプラットフォームでトレースとメトリクスを確認する
- Splunk Observability Cloud で AppDynamics へのワンクリックナビゲーションのための **global data link** を作成する

## アーキテクチャ

このワークショップでは、Spring Boot Java アプリケーションを EC2 インスタンス上で直接実行します。AppDynamics Java Agent は JVM プロセスにアタッチされます。

**Phase 1: 通常の AppD 計装:**

```text
Java App + AppD Agent  ──▶  AppD Controller
```

**Phase 2: Dual signal mode 有効化:**

```text
Java App + AppD Agent  ──▶  AppD Controller        (AppD protocol, unchanged)
                       ──▶  OTel Collector          (OTLP on localhost:4317)
                                 │
                                 ▼
                           Splunk Observability Cloud
```

OpenTelemetry Collector は同じ EC2 インスタンス上で実行され、エージェントから OTLP を受信し、トレースとメトリクスを Splunk Observability Cloud にエクスポートします。

**注意:** Collector を使用せずにエージェントから直接 [OTLP ingest endpoint](https://dev.splunk.com/observability/docs/datamodel/ingest/#Send-data-points) にデータを送信することも可能ですが、OTel 設定で一部の属性や関連付けが失われる可能性があります。

## Hybrid Mode vs Dual Signal Mode

AppDynamics Java Agent は、OpenTelemetry データを出力するための2つのモードをサポートしています。

この違いを理解することは重要です！

### Hybrid Mode - 旧式 (GA, Java Agent 22.3+)

- AppDynamics の**独自の計装ルール**が OTel 形式のスパンを生成します
- エージェントは既存の計装を再利用して OTel データを生成します（古いセマンティックバージョン）
- フレームワークのカバレッジは AppDynamics が計装するものに限定されます
- 有効化方法: `-Dagent.deployment.mode=hybrid`

### Dual Signal Mode - 最新式 (Beta, Java Agent 25.6+)

- 完全な [OpenTelemetry Java auto-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/) が AppD agent と**並行して**実行されます
- 2つの独立した計装エンジンが並列で動作します
- **より広範なフレームワークカバレッジ** - OTel Java agent がサポートするすべてのものに対応
- より高い CPU とメモリ消費
- 有効化方法: `-Dagent.deployment.mode=dual` または環境変数 `AGENT_DEPLOYMENT_MODE=dual`

### このワークショップで Dual Mode を使用する理由

Dual signal mode は、hybrid mode にはない**相関属性**をルートスパンに追加します

| 属性 | 説明 |
|---|---|
| `appd.app.name` | AppDynamics アプリケーション名 |
| `appd.tier.name` | AppDynamics tier 名（tier が変更されるとトレースの途中にも表示されます） |
| `appd.bt.name` | AppDynamics ビジネストランザクション名 |
| `appd.request.guid` | AppDynamics リクエスト GUID |

これらの属性により、**global data links** が有効になります。これは Splunk Observability Cloud のトレース上のクリック可能なリンクで、対応する AppDynamics ビューに直接ナビゲートできます。さらに、dual mode でキャプチャされた AppDynamics スナップショットには、Data Collectors タブに OTel `TraceId` が含まれ、双方向のナビゲーションが可能になります。

## 前提条件

ワークショップインスタンスには必要なツールが事前設定されています

| 要件 | ワークショップインスタンスでの状態 |
|---|---|
| Linux ホスト (Ubuntu) | 提供済み |
| OpenJDK 17 | インストール済み |
| Maven | インストール済み |
| ワークショップアセット | `~/workshop/appd/` にデプロイ済み |

以下も必要です

| 要件 | 入手方法 |
|---|---|
| Splunk Observability Cloud アカウント | インストラクターから提供されます |
| **Splunk Access Token** (Ingest) | インスタンスで `echo $ACCESS_TOKEN` を実行 |
| **Splunk Realm** (例: `us0`, `us1`, `eu0`) | インスタンスで `echo $REALM` を実行 |
| **Instance name** | インスタンスで `echo $INSTANCE` を実行 |
| AppDynamics Controller アクセス | [SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) に Cisco 認証情報でログイン |
