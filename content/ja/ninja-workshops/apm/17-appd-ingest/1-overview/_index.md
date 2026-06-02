---
title: ワークショップ概要
linkTitle: 1. 概要
weight: 1
archetype: chapter
time: 5 minutes
description: ユースケース、アーキテクチャ、前提条件、およびハイブリッドモードとデュアルシグナルモードの違いについて解説します。
---

## ユースケース

あなたの組織では現在、APM として AppDynamics を運用しています。データの可視性とガバナンスに関する取り組みの一環として、経営陣はアプリケーションパフォーマンスデータを **Splunk Observability Cloud** にも流し込み、すでに Splunk に存在するインフラストラクチャメトリクス、ログ、その他のシグナルと並べて、チームに統一されたビューを提供したいと考えています。

すべてのサービスを別個の OpenTelemetry SDK で再計装する代わりに、AppDynamics Java Agent は **デュアルシグナルモード** をサポートしています。これは、単一のエージェントが AppDynamics APM データと OpenTelemetry トレースの両方を同時に生成する仕組みです。これにより、AppDynamics の機能をフルに維持しながら、同じテレメトリーを OpenTelemetry Collector 経由で Splunk Observability Cloud にストリーミングできます。

これは、現在 AppDynamics を熟知し、依存している L1 および L2 チームにとって特に有用です。デュアルインジェストは、彼らが担当するアプリケーションとサービスがクラウド上の SaaS プラットフォームでホストされる新しいサービスとますます連携していく中で、コンテキストを維持するのに役立ちます。

## このワークショップで学ぶこと

このワークショップを終える頃には、次のことができるようになります。

- AppDynamics Java Agent を使ったシンプルな Java サービスのビルドと実行
- **ハイブリッドモード** と **デュアルシグナルモード** の違いの理解
- デュアルシグナルモードを有効化して、APM データを AppDynamics と Splunk Observability Cloud の両方に送信
- 両プラットフォームでのトレースとメトリクスの確認
- ワンクリックで AppDynamics に遷移できる **global data link** を Splunk Observability Cloud で作成

## アーキテクチャ

このワークショップでは、Spring Boot Java アプリケーションを EC2 インスタンス上で直接実行します。AppDynamics Java Agent は JVM プロセスにアタッチされます。

**フェーズ 1: 通常の AppD 計装:**

```text
Java App + AppD Agent  ──▶  AppD Controller
```

**フェーズ 2: デュアルシグナルモード有効化:**

```text
Java App + AppD Agent  ──▶  AppD Controller        (AppD protocol, unchanged)
                       ──▶  OTel Collector          (OTLP on localhost:4317)
                                 │
                                 ▼
                           Splunk Observability Cloud
```

OpenTelemetry Collector は同じ EC2 インスタンス上で実行され、エージェントから OTLP を受信し、トレースとメトリクスを Splunk Observability Cloud にエクスポートします。

**Note:** Collector を介さずにエージェントから直接当社の [OTLP ingest endpoint](https://dev.splunk.com/observability/docs/datamodel/ingest/#Send-data-points) にデータを送信することも可能ですが、OTel 設定で関与する一部の属性や関連付けが失われる可能性があります。

## ハイブリッドモード vs デュアルシグナルモード

AppDynamics Java Agent は、OpenTelemetry データを送出するための 2 つのモードをサポートしています。

両者の違いを理解することは重要です。

### ハイブリッドモード - 古くて埃をかぶった方式 (GA, Java Agent 22.3+)

- AppDynamics 独自の **計装ルール** が OTel フォーマットのスパンを生成
- エージェントは既存の計装を再利用して OTel データを生成 (古いセマンティックバージョン)
- フレームワークのカバレッジは AppDynamics が計装するものに限定
- 有効化方法: `-Dagent.deployment.mode=hybrid`

### デュアルシグナルモード - 新しく注目の方式 (Beta, Java Agent 25.6+)

- 完全な [OpenTelemetry Java auto-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/) が AppD エージェントと **並行して** 実行
- 2 つの独立した計装エンジンが並列で動作
- **より広範なフレームワークカバレッジ** OTel Java エージェントがサポートするすべて
- CPU とメモリの消費量が増加
- 有効化方法: `-Dagent.deployment.mode=dual` または環境変数 `AGENT_DEPLOYMENT_MODE=dual`

### このワークショップでデュアルモードを使う理由

デュアルシグナルモードでは、ハイブリッドモードにはない **相関属性** がルートスパンに追加されます。

| 属性 | 説明 |
|---|---|
| `appd.app.name` | AppDynamics アプリケーション名 |
| `appd.tier.name` | AppDynamics ティア名 (ティアが変化する際にはトレースの途中にも現れます) |
| `appd.bt.name` | AppDynamics ビジネストランザクション名 |
| `appd.request.guid` | AppDynamics リクエスト GUID |

これらの属性により、**global data links** が利用可能になります。これは Splunk Observability Cloud のトレース上のクリック可能なリンクで、対応する AppDynamics ビューに直接遷移できます。さらに、デュアルモードでキャプチャされた AppDynamics スナップショットには、Data Collectors タブに OTel `TraceId` が含まれるため、双方向のナビゲーションが可能です。

## 前提条件

ワークショップインスタンスには、必要なツールがあらかじめ設定されています。

| 要件 | ワークショップインスタンスでの状態 |
|---|---|
| Linux ホスト (Ubuntu) | 提供済み |
| OpenJDK 17 | プリインストール済み |
| Maven | プリインストール済み |
| ワークショップ資材 | `~/workshop/appd/` にデプロイ済み |

また、以下も必要です。

| 要件 | 取得方法 |
|---|---|
| Splunk Observability Cloud アカウント | インストラクターから提供 |
| **Splunk Access Token** (Ingest) | インスタンス上で `echo $ACCESS_TOKEN` を実行 |
| **Splunk Realm** (例 `us0`, `us1`, `eu0`) | インスタンス上で `echo $REALM` を実行 |
| **Instance name** | インスタンス上で `echo $INSTANCE` を実行 |
| AppDynamics Controller アクセス | [SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) に Cisco の認証情報でログイン |
