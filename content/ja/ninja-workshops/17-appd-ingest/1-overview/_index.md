---
title: ワークショップの概要
linkTitle: 1. Overview
weight: 1
archetype: chapter
time: 5 minutes
description: ユースケース、アーキテクチャ、前提条件、ハイブリッドモードとデュアルシグナルモードの違いを学びます。
---

## ユースケース

あなたの組織では現在、APM として AppDynamics を運用しています。データの可視性とガバナンスを高める取り組みの一環として、経営陣はアプリケーションパフォーマンスのデータも **Splunk Observability Cloud** に流し込みたいと考えています。これにより、すでに Splunk に存在するインフラメトリクス、ログ、その他のシグナルと並べて、各チームが統一されたビューを得られるようにします。

すべてのサービスを別の OpenTelemetry SDK で再計装するのではなく、AppDynamics Java Agent は **デュアルシグナルモード**をサポートしています。つまり、1つのエージェントが AppDynamics APM データと OpenTelemetry トレースを同時に生成します。これにより、AppDynamics の機能を完全に維持しながら、同じテレメトリを OpenTelemetry Collector を経由して Splunk Observability Cloud にストリーミングできます。

これは、現在 AppDynamics を熟知し依存している L1 および L2 チームにとって特に有用です。デュアル ingest は、彼らが担当するアプリケーションやサービスが、クラウド上の SaaS プラットフォームでホストされる新しいサービスとますます接続されていく中で、コンテキストを維持するのに役立ちます。

## 学べる内容

このワークショップを終えると、次のことができるようになります。

- AppDynamics Java Agent を使用して、シンプルな Java サービスをビルドし、実行する
- **ハイブリッドモード**と**デュアルシグナルモード**の違いを理解する
- デュアルシグナルモードを有効にして、AppDynamics と Splunk Observability Cloud の両方に APM データを送信する
- 両方のプラットフォームでトレースとメトリクスを確認する
- Splunk Observability Cloud で **global data link** を作成し、ワンクリックで AppDynamics に移動する

## アーキテクチャ

このワークショップでは、Spring Boot Java アプリケーションを EC2 インスタンス上で直接実行します。AppDynamics Java Agent は JVM プロセスにアタッチされます。

**フェーズ 1: 通常の AppD インストルメンテーション**

```text
Java App + AppD Agent  ──▶  AppD Controller
```

**フェーズ 2: デュアルシグナルモード有効化後**

```text
Java App + AppD Agent  ──▶  AppD Controller        (AppD protocol, unchanged)
                       ──▶  OTel Collector          (OTLP on localhost:4317)
                                 │
                                 ▼
                           Splunk Observability Cloud
```

OpenTelemetry Collector は同じ EC2 インスタンス上で実行され、エージェントから OTLP を受信し、トレースとメトリクスを Splunk Observability Cloud にエクスポートします。

**注意:** Collector を介さずにエージェントから直接 [OTLP ingest endpoint](https://dev.splunk.com/observability/docs/datamodel/ingest/#Send-data-points) にデータを送信することも可能ですが、OTel 設定で行う一部の属性や関連付けが失われる可能性があります。

## ハイブリッドモード vs デュアルシグナルモード

AppDynamics Java Agent は、OpenTelemetry データを出力するための2つのモードをサポートしています。

その違いを理解することは重要です。

### ハイブリッドモード - 古くて時代遅れ（GA、Java Agent 22.3+）

- AppDynamics の**独自のインストルメンテーションルール**が OTel 形式のスパンを生成します
- エージェントは既存のインストルメンテーションを再利用して OTel データを生成します（古いセマンティックバージョン）
- フレームワークのカバレッジは AppDynamics が計装する範囲に限定されます
- 有効化方法 `-Dagent.deployment.mode=hybrid`

### デュアルシグナルモード - 新しくホットな機能（Beta、Java Agent 25.6+）

- 完全な [OpenTelemetry Java auto-instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/) が AppD エージェントと**並行して**実行されます
- 2つの独立したインストルメンテーションエンジンが並列で動作します
- **より広範なフレームワークカバレッジ** OTel Java エージェントがサポートするものすべて
- CPU とメモリの消費量はより高くなります
- 有効化方法 `-Dagent.deployment.mode=dual` または環境変数 `AGENT_DEPLOYMENT_MODE=dual`

### このワークショップでデュアルモードを使用する理由

デュアルシグナルモードは、ハイブリッドモードでは付与されない**相関属性**をルートスパンに追加します。

| 属性 | 説明 |
|---|---|
| `appd.app.name` | AppDynamics のアプリケーション名 |
| `appd.tier.name` | AppDynamics の tier 名（tier が変化した場合はトレース中盤にも表示されます） |
| `appd.bt.name` | AppDynamics のビジネストランザクション名 |
| `appd.request.guid` | AppDynamics のリクエスト GUID |

これらの属性により、**global data links** が利用可能になります。これは、Splunk Observability Cloud のトレース上に表示されるクリック可能なリンクで、対応する AppDynamics ビューに直接移動できます。さらに、デュアルモードでキャプチャされた AppDynamics スナップショットには、Data Collectors タブに OTel `TraceId` が含まれており、双方向のナビゲーションが可能になります。

## OBI vs 従来のゼロコードインストルメンテーション

OBI と既存の言語固有のゼロコードインストルメンテーション（Java、JS、.NET、Python、Go、PHP）は、オブザーバビリティ戦略において補完的な役割を担っています。違いを理解することで、それぞれのアプローチをいつ使用するかを判断できます。

### 1. インストルメンテーションモデル

| 観点 | OBI | 従来のゼロコードインストルメンテーション |
|---|---|---|
| 実行モデル | プロセス外 | プロセス内 |
| インストルメンテーション層 | Linux カーネル / ネットワーク | アプリケーションランタイム |
| コード変更が必要か | 不要 | 不要または最小限 |
| アプリケーションの再起動が必要か | 不要 | 必要 |
| セキュリティプロファイル | 隔離 | アプリケーションと同じ権限プロファイル |

### 2. 可視化レベル

| 機能 | OBI | 従来のゼロコードインストルメンテーション |
|---|---|---|
| 分散トレーシング | プロトコルレベル | フルフィデリティ |
| RED メトリクス | 対応 | 対応 |
| アプリケーションログの収集 | 非対応 | 対応 |
| アプリケーションログとトレースの相関 | 対応 | 対応 |
| アプリケーション内部（フレームワーク、関数） | 非対応（部分的、主に Go） | 対応 |
| カスタムスパン / ビジネス属性 | 非対応 | 対応 |
| ランタイムメトリクス（JVM、メモリ、スレッド） | 現時点では非対応 | 対応 |

### 3. カバレッジと互換性

| シナリオ | OBI | 従来のゼロコードインストルメンテーション |
|---|---|---|
| マルチ言語環境 | 強力（プロトコルベース） | 言語固有 |
| サードパーティアプリケーション | サポート | 限定的、contrib リポジトリ |
| レガシーシステム | サポート | 限定的 |
| コンパイル言語（C/C++/Rust） | サポート（async に一部制限あり） | 限定的 |
| Async / 複雑なフレームワーク | 一部のケースで限定的 | 強力 |

### 4. 運用特性

| 観点 | OBI | 従来のゼロコードインストルメンテーション |
|---|---|---|
| デプロイの労力 | 低（ドロップイン） | 中（エージェントのアタッチ） |
| 最初の可視化までの時間 | 数分 | 「より長い」数分 |
| アプリケーションライフサイクルの変更 | 不要 | 必要 |
| パフォーマンスオーバーヘッド | 最小限かつ隔離 | 言語/ランタイムにより異なる |

### 5. Splunk Distro 機能

| 機能 | OBI | 従来のゼロコードインストルメンテーション |
|---|---|---|
| Always-on Profiling | 非対応（将来 eBPF profiler とバンドルされる可能性あり） | ほとんどで CPU、一部で Memory |
| コールグラフ | 非対応 | ほとんどで CPU、一部で Memory |
| ファイルベースの設定 | 提供予定 | Java、Node.js、.NET、Python（提供予定） |
| ノーコードインストルメンテーション | 該当なし | 対応 |

## 前提条件

ワークショップインスタンスには、必要なツールがあらかじめ設定されています。

| 要件 | ワークショップインスタンス上のステータス |
|---|---|
| Linux ホスト（Ubuntu） | 提供済み |
| OpenJDK 17 | プリインストール済み |
| Maven | プリインストール済み |
| ワークショップアセット | `~/workshop/appd/` にデプロイ済み |

加えて、次のものも必要です。

| 要件 | 入手方法 |
|---|---|
| Splunk Observability Cloud アカウント | インストラクターから提供 |
| **Splunk Access Token**（Ingest） | インスタンスで `echo $ACCESS_TOKEN` |
| **Splunk Realm**（例 `us0`、`us1`、`eu0`） | インスタンスで `echo $REALM` |
| **インスタンス名** | インスタンスで `echo $INSTANCE` |
| AppDynamics Controller アクセス | [SE Lab Controller](https://se-lab.saas.appdynamics.com/controller/) に Cisco の認証情報でログイン |
