---
title: ワークショップ概要
linkTitle: 1. Overview
weight: 1
archetype: chapter
time: 5 minutes
description: ユースケース、アーキテクチャ、前提条件、およびhybridモードとdual signalモードの違い。
---

## ユースケース

あなたの組織は現在、APMとしてAppDynamicsを運用しています。データの可視性とガバナンスの取り組みの一環として、経営陣はアプリケーションパフォーマンスデータを **Splunk Observability Cloud** にも送信し、Splunkにすでに取り込まれているインフラストラクチャメトリクス、ログ、その他のシグナルと合わせて統一的なビューをチームに提供したいと考えています。

すべてのサービスを別のOpenTelemetry SDKで再計装する代わりに、AppDynamics Java Agentは **dual signalモード** をサポートしています。単一のエージェントがAppDynamics APMデータとOpenTelemetryトレースの両方を同時に生成します。これにより、AppDynamicsの全機能を維持しながら、同じテレメトリをOpenTelemetry Collectorを通じてSplunk Observability Cloudにストリーミングできます。

これは、現在AppDynamicsを使い慣れているL1およびL2チームにとって特に有用です。Dual ingestにより、担当するアプリケーションやサービスがクラウドのSaaSプラットフォームでホストされる新しいサービスと接続されるようになっても、コンテキストを維持できます。

## 学習内容

このワークショップを完了すると、以下ができるようになります。

- AppDynamics Java Agentを使用してシンプルなJavaサービスをビルドおよび実行する
- **hybrid mode** と **dual signal mode** の違いを理解する
- Dual signalモードを有効にして、APMデータをAppDynamicsとSplunk Observability Cloudの両方に送信する
- 両方のプラットフォームでトレースとメトリクスを検証する
- Splunk Observability Cloudで **global data link** を作成し、AppDynamicsへのワンクリックナビゲーションを実現する

## アーキテクチャ

このワークショップでは、EC2インスタンス上でSpring Boot Javaアプリケーションを直接実行します。AppDynamics Java AgentはJVMプロセスにアタッチされます。

**フェーズ1: 通常のAppD計装**

```text
Java App + AppD Agent  ──▶  AppD Controller
```

**フェーズ2: Dual signalモード有効化**

```text
Java App + AppD Agent  ──▶  AppD Controller        (AppD protocol, unchanged)
                       ──▶  OTel Collector          (OTLP on localhost:4317)
                                 │
                                 ▼
                           Splunk Observability Cloud
```

OpenTelemetry Collectorは同じEC2インスタンス上で動作し、エージェントからOTLPを受信して、トレースとメトリクスをSplunk Observability Cloudにエクスポートします。

**注意:** Collectorを使用せずにエージェントから直接[OTLPインジェストエンドポイント](https://dev.splunk.com/observability/docs/datamodel/ingest/#Send-data-points)にデータを送信することも可能ですが、OTel設定で使用される一部の属性や関連付けが失われる場合があります。

## Hybrid ModeとDual Signal Modeの比較

AppDynamics Java Agentは、OpenTelemetryデータを出力するための2つのモードをサポートしています。

この違いを理解することが重要です。

### Hybrid Mode - 旧方式（GA、Java Agent 22.3以降）

- AppDynamicsの **独自の計装ルール** がOTel形式のSpanを生成する
- エージェントは既存の計装を再利用してOTelデータを生成する（古いセマンティックバージョン）
- フレームワークのカバレッジはAppDynamicsが計装するものに限定される
- 有効化: `-Dagent.deployment.mode=hybrid`

### Dual Signal Mode - 新方式（Beta、Java Agent 25.6以降）

- 完全な[OpenTelemetry Java自動計装](https://github.com/open-telemetry/opentelemetry-java-instrumentation/)がAppDエージェントと **並行して** 動作する
- 2つの独立した計装エンジンが並列で動作する
- **より広いフレームワークカバレッジ** — OTel Javaエージェントがサポートするすべてに対応
- CPUとメモリの消費量が増加する
- 有効化: `-Dagent.deployment.mode=dual` または環境変数 `AGENT_DEPLOYMENT_MODE=dual`

### このワークショップでDualモードを使用する理由

Dual signalモードは、hybrid modeにはない **相関属性** をルートSpanに追加します。

| 属性 | 説明 |
|---|---|
| `appd.app.name` | AppDynamicsアプリケーション名 |
| `appd.tier.name` | AppDynamicsティア名（トレース中にティアが変わる場合にも表示される） |
| `appd.bt.name` | AppDynamicsビジネストランザクション名 |
| `appd.request.guid` | AppDynamicsリクエストGUID |

これらの属性により **global data links** が有効になります。これはSplunk Observability Cloudのトレース上のクリック可能なリンクで、対応するAppDynamicsのビューに直接ナビゲートできます。さらに、dualモードでキャプチャされたAppDynamicsスナップショットには、Data CollectorsタブにOTelの `TraceId` が含まれるため、双方向のナビゲーションが可能になります。

## 前提条件

ワークショップインスタンスには必要なツールが事前設定されています（または、この[Splunk Showインスタンス](https://show.splunk.com/template/428/)で独自に起動することもできます）。

| 要件 | ワークショップインスタンスでの状態 |
|---|---|
| Linuxホスト（Ubuntu） | 提供済み |
| OpenJDK 17 | インストール済み |
| Maven | インストール済み |
| ワークショップアセット | `~/workshop/appd/` にデプロイ済み |

以下も必要です。

| 要件 | 取得方法 |
|---|---|
| Splunk Observability Cloudアカウント | インストラクターから提供されます |
| **Splunk Access Token**（Ingest） | インスタンスで `echo $ACCESS_TOKEN` を実行 |
| **Splunk Realm**（例: `us0`, `us1`, `eu0`） | インスタンスで `echo $REALM` を実行 |
| **インスタンス名** | インスタンスで `echo $INSTANCE` を実行 |
| AppDynamics Controllerアクセス | [SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/)にCisco資格情報でログイン |
