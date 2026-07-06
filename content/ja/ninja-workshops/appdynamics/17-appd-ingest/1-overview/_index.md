---
title: ワークショップ概要
linkTitle: 1. 概要
weight: 1
archetype: chapter
time: 5 minutes
description: ユースケース、アーキテクチャ、前提条件、およびハイブリッドモードとデュアルシグナルモードの違いについて説明します。
---

## ユースケース

あなたの組織では現在、APM として AppDynamics を使用しています。データの可視性とガバナンスの取り組みの一環として、経営層はアプリケーションパフォーマンスデータを **Splunk Observability Cloud** にも送信し、Splunk に既に存在するインフラストラクチャメトリクス、ログ、その他のシグナルと合わせてチームに統合ビューを提供することを求めています。

すべてのサービスを別の OpenTelemetry SDK で再計装する代わりに、AppDynamics Java Agent は**デュアルシグナルモード**をサポートしています。単一のエージェントが AppDynamics APM データと OpenTelemetry トレースの両方を同時に生成します。これにより、AppDynamics の完全な機能を維持しながら、OpenTelemetry Collector を通じて同じテレメトリを Splunk Observability Cloud にストリーミングできます。

これは、現在 AppDynamics を熟知し依存している L1 および L2 チームにとって特に有用です。デュアルインジェストは、担当するアプリケーションやサービスがクラウドの SaaS プラットフォームでホストされる新しいサービスとより密接に接続されるようになる際に、コンテキストを維持するのに役立ちます。

## 学習内容

このワークショップを終了すると、以下のことができるようになります

- AppDynamics Java Agent を使用してシンプルな Java サービスをビルドおよび実行する
- **ハイブリッドモード**と**デュアルシグナルモード**の違いを理解する
- デュアルシグナルモードを有効にして、APM データを AppDynamics と Splunk Observability Cloud の両方に送信する
- 両方のプラットフォームでトレースとメトリクスを検証する
- Splunk Observability Cloud で**グローバルデータリンク**を作成し、AppDynamics へのワンクリックナビゲーションを実現する

## アーキテクチャ

このワークショップでは、EC2 インスタンス上で直接 Spring Boot Java アプリケーションを実行します。AppDynamics Java Agent は JVM プロセスにアタッチされます。

**フェーズ 1: 通常の AppD 計装**

```text
Java App + AppD Agent  ──▶  AppD Controller
```

**フェーズ 2: デュアルシグナルモード有効化**

```text
Java App + AppD Agent  ──▶  AppD Controller        (AppD protocol, unchanged)
                       ──▶  OTel Collector          (OTLP on localhost:4317)
                                 │
                                 ▼
                           Splunk Observability Cloud
```

OpenTelemetry Collector は同じ EC2 インスタンス上で実行され、エージェントから OTLP を受信し、トレースとメトリクスを Splunk Observability Cloud にエクスポートします。  

**注意:** Collector を使用せずにエージェントから直接 [OTLP インジェストエンドポイント](https://dev.splunk.com/observability/docs/datamodel/ingest/#Send-data-points) にデータを送信することも可能ですが、OTel 設定で使用される一部の属性やアソシエーションが失われる可能性があります。

## ハイブリッドモード vs デュアルシグナルモード

AppDynamics Java Agent は、OpenTelemetry データを出力するための2つのモードをサポートしています。  

この違いを理解することが重要です！

### ハイブリッドモード - 旧式 (GA, Java Agent 22.3+)

- AppDynamics の**独自の計装ルール**が OTel 形式のスパンを生成します
- エージェントは既存の計装を再利用して OTel データを生成します（古いセマンティックバージョン）
- フレームワークカバレッジは AppDynamics が計装するものに限定されます
- 有効化方法: `-Dagent.deployment.mode=hybrid`

### デュアルシグナルモード - 最新版 (Beta, Java Agent 25.6+)

- 完全な [OpenTelemetry Java auto-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/) が AppD エージェントと**並行して**実行されます
- 2つの独立した計装エンジンが並列で動作します
- **より広範なフレームワークカバレッジ** - OTel Java エージェントがサポートするすべてのものに対応
- CPU とメモリの消費量が増加します
- 有効化方法: `-Dagent.deployment.mode=dual` または環境変数 `AGENT_DEPLOYMENT_MODE=dual`

### このワークショップでデュアルモードを使用する理由

デュアルシグナルモードは、ハイブリッドモードにはない**相関属性**をルートスパンに追加します

| 属性 | 説明 |
|---|---|
| `appd.app.name` | AppDynamics アプリケーション名 |
| `appd.tier.name` | AppDynamics ティア名（トレース中にティアが変わる場合はミッドトレースにも表示されます） |
| `appd.bt.name` | AppDynamics ビジネストランザクション名 |
| `appd.request.guid` | AppDynamics リクエスト GUID |

これらの属性により、**グローバルデータリンク**が有効になります。Splunk Observability Cloud のトレース上のクリック可能なリンクから、対応する AppDynamics ビューに直接ナビゲートできます。さらに、デュアルモードでキャプチャされた AppDynamics スナップショットには、Data Collectors タブに OTel の `TraceId` が含まれるため、双方向のナビゲーションが可能になります。

## 前提条件

ワークショップインスタンスには必要なツールが事前設定されています（または [Splunk Show インスタンス](https://show.splunk.com/template/428/) で独自に起動することもできます）

| 要件 | ワークショップインスタンスでの状態 |
|---|---|
| Linux ホスト (Ubuntu) | 提供済み |
| OpenJDK 17 | インストール済み |
| Maven | インストール済み |
| ワークショップアセット | `~/workshop/appd/` にデプロイ済み |

以下も必要です

| 要件 | 取得方法 |
|---|---|
| Splunk Observability Cloud アカウント | インストラクターから提供されます |
| **Splunk Access Token** (Ingest) | インスタンスで `echo $ACCESS_TOKEN` を実行 |
| **Splunk Realm** (例: `us0`, `us1`, `eu0`) | インスタンスで `echo $REALM` を実行 |
| **インスタンス名** | インスタンスで `echo $INSTANCE` を実行 |
| AppDynamics Controller アクセス | [SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) に Cisco 資格情報でログイン |
