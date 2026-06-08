---
title: まとめ
linkTitle: 5. まとめ
weight: 5
archetype: chapter
time: 5 minutes
description: サマリー、クリーンアップ、および次のステップです。
---

## 達成したこと

このワークショップでは、以下のことを行いました:

1. **通常の AppDynamics インストルメンテーションで Java サービスをビルドして実行しました**: 単一のエージェントが APM データを AppDynamics Controller のみに送信します。

2. **ハイブリッドモードとデュアルシグナルモードの違いを学びました**: ハイブリッドは AppD 自身のインストルメンテーションを再利用して OTel スパンを生成します（オーバーヘッドが低く、カバレッジは狭い）。一方、デュアルは完全な OTel Java 自動インストルメンテーションを AppD と並行して実行します（カバレッジが広く、相関属性が追加されます）。

3. **デュアルシグナルモードを有効にしました**: 同じプロセスに 4 つの JVM フラグを追加するだけです。コード変更なし、2 つ目のエージェントなし、再コンパイルなし。同じ AppDynamics エージェントが AppDynamics と Splunk Observability Cloud の両方に同時にデータを送信するようになります。

4. **グローバルデータリンクを作成しました**: Splunk Observability Cloud で `appd.*` スパン属性を使用して、対応する AppDynamics ティアビューに直接ナビゲートします。

## クリーンアップ

アプリケーションと負荷生成ツールを停止します:

```bash
kill %2 2>/dev/null   # load generator
kill %1 2>/dev/null   # java app
```

オプションで Collector を停止します:

```bash
sudo systemctl stop splunk-otel-collector
```

## 重要なポイント

- **デュアルモードはコード変更ではなく、設定変更です。** すでにインストルメンテーション済みのアプリケーションに JVM フラグを追加することで有効にしました。これにより、アプリケーションコードに触れることなく、組織全体にロールアウトすることが実用的になります。

- **`appd.*` 相関属性が統合を価値あるものにします。** これらがない場合（ハイブリッドモード）、Splunk O11y で OTel トレースを取得できますが、特定の AppDynamics ビジネストランザクション、ティア、またはアプリケーションにリンクする方法がありません。デュアルモードはそのリンクを提供します。

- **グローバルデータリンクは相関をワークフローに変えます。** 2 つのツールを手動でクロスリファレンスする代わりに、エンジニアは Splunk O11y のトレースから AppDynamics ビューに直接クリックできます。

- **このパターンは段階的な移行をサポートします。** 組織はデュアルモードを一定期間実行して、Splunk Observability Cloud が同じシグナル品質をキャプチャすることを検証し、その後サービスごとにデュアルを継続するか、Splunk のみのインストルメンテーションに切り替えるか、AppDynamics を継続するかを決定できます。

## 参考資料

- [Enable Dual Signal Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-dual-signal-mode) (AppDynamics ドキュメント)
- [Enable Hybrid Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-hybrid-mode) (AppDynamics ドキュメント)
- [Java Agent Frameworks for OpenTelemetry](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/support-for-appdynamics-for-opentelemetry/java-agent-frameworks-for-opentelemetry) (サポートされるフレームワーク一覧)
- [Global Data Links](https://docs.splunk.com/observability/en/data-visualization/navigate-with-data-links.html) (Splunk Observability ドキュメント)
