---
title: ワークショップ概要
linkTitle: 1. Overview
weight: 1
archetype: chapter
time: 5 minutes
description: ユースケース、アーキテクチャ、前提条件、およびハイブリッドモードとデュアルシグナルモードの違いについて説明します。
---

## ユースケース

あなたの組織では現在、APMとしてAppDynamicsを使用しています。データの可視性とガバナンスの取り組みの一環として、経営陣はアプリケーションパフォーマンスデータを **Splunk Observability Cloud** にも送信することを望んでいます。これにより、チームはすでにSplunkにあるインフラストラクチャメトリクス、ログ、その他のシグナルと合わせて統一されたビューを得ることができます。

すべてのサービスを別のOpenTelemetry SDKで再計装する代わりに、AppDynamics Java Agentは **デュアルシグナルモード** をサポートしています。単一のエージェントがAppDynamics APMデータとOpenTelemetryトレースの両方を同時に生成します。これにより、OpenTelemetry Collectorを通じて同じテレメトリをSplunk Observability Cloudにストリーミングしながら、AppDynamicsの完全な機能を維持できます。

これは、現在AppDynamicsを熟知し依存しているL1およびL2チームにとって特に有用です。デュアルインジェストは、担当するアプリケーションやサービスがクラウドのSaaSプラットフォームでホストされる新しいサービスとより密接に接続されるようになっても、コンテキストを維持するのに役立ちます。

## 学習内容

このワークショップを完了すると、以下のことができるようになります：

- AppDynamics Java Agentを使用してシンプルなJavaサービスをビルドおよび実行する
- **ハイブリッドモード** と **デュアルシグナルモード** の違いを理解する
- デュアルシグナルモードを有効にしてAPMデータをAppDynamicsとSplunk Observability Cloudの両方に送信する
- 両方のプラットフォームでトレースとメトリクスを確認する
- Splunk Observability Cloudで **グローバルデータリンク** を作成し、ワンクリックでAppDynamicsに移動できるようにする

## アーキテクチャ

このワークショップでは、Spring Boot JavaアプリケーションをEC2インスタンス上で直接実行します。AppDynamics Java AgentはJVMプロセスにアタッチされます。

**フェーズ1 -- 通常のAppD計装：**

```text
Java App + AppD Agent  ──▶  AppD Controller
```

**フェーズ2 -- デュアルシグナルモード有効化：**

```text
Java App + AppD Agent  ──▶  AppD Controller        (AppD protocol, unchanged)
                       ──▶  OTel Collector          (OTLP on localhost:4317)
                                 │
                                 ▼
                           Splunk Observability Cloud
```

OpenTelemetry Collectorは同じEC2インスタンス上で実行され、エージェントからOTLPを受信し、トレースとメトリクスをSplunk Observability Cloudにエクスポートします。

**注意：** コレクターなしでエージェントから直接[OTLPインジェストエンドポイント](https://dev.splunk.com/observability/docs/datamodel/ingest/#Send-data-points)にデータを送信することも可能ですが、OTel設定で設定した一部の属性や関連付けが失われる可能性があります。

## ハイブリッドモード vs デュアルシグナルモード

AppDynamics Java AgentはOpenTelemetryデータを出力するための2つのモードをサポートしています。

この違いを理解することは重要です！

### ハイブリッドモード（GA、Java Agent 22.3以降）

- AppDynamicsの **独自の計装ルール** がOTel形式のスパンを生成します
- エージェントは既存の計装を再利用してOTelデータを生成します（古いセマンティックバージョン）
- **オーバーヘッドが低い**（CPUとメモリ）
- フレームワークのカバレッジはAppDynamicsが計装するものに限定されます
- 有効化方法: `-Dagent.deployment.mode=hybrid`

### デュアルシグナルモード（ベータ、Java Agent 25.6以降）

- 完全な[OpenTelemetry Java自動計装](https://github.com/open-telemetry/opentelemetry-java-instrumentation/)がAppDエージェントと **並行して** 実行されます
- 2つの独立した計装エンジンが並列で動作します
- **フレームワークカバレッジが広い** -- OTel Javaエージェントがサポートするすべてのフレームワークに対応
- CPUとメモリの消費量が高くなります
- 有効化方法: `-Dagent.deployment.mode=dual` または環境変数 `AGENT_DEPLOYMENT_MODE=dual`

### このワークショップでデュアルモードを使用する理由

デュアルシグナルモードは、ハイブリッドモードにはない **相関属性** をルートスパンに追加します：

| 属性 | 説明 |
|---|---|
| `appd.app.name` | AppDynamicsアプリケーション名 |
| `appd.tier.name` | AppDynamicsティア名（ティアが変更されるとトレースの途中にも表示されます） |
| `appd.bt.name` | AppDynamicsビジネストランザクション名 |
| `appd.request.guid` | AppDynamicsリクエストGUID |

これらの属性により、**グローバルデータリンク**（Splunk Observability Cloudのトレース上のクリック可能なリンクで、対応するAppDynamicsビューに直接移動できます）が有効になります。さらに、デュアルモードでキャプチャされたAppDynamicsスナップショットには、Data CollectorsタブにOTelの `TraceId` が含まれるため、双方向のナビゲーションが可能になります。

## 前提条件

ワークショップインスタンスには必要なツールが事前に設定されています：

| 要件 | ワークショップインスタンスでの状態 |
|---|---|
| Linuxホスト（Ubuntu） | 提供済み |
| OpenJDK 17 | インストール済み |
| Maven | インストール済み |
| ワークショップアセット | `~/workshop/appd/` に事前デプロイ済み |

以下も必要です：

| 要件 | 取得方法 |
|---|---|
| Splunk Observability Cloud アカウント | インストラクターから提供されます |
| **Splunk Access Token**（Ingest） | インスタンスで `echo $ACCESS_TOKEN` を実行 |
| **Splunk Realm**（例：`us0`、`us1`、`eu0`） | インスタンスで `echo $REALM` を実行 |
| **インスタンス名** | インスタンスで `echo $INSTANCE` を実行 |
| AppDynamics Controllerアクセス | [SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) -- Ciscoの認証情報でログイン |
