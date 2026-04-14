---
title: まとめ
linkTitle: 5. まとめ
weight: 5
archetype: chapter
time: 5 minutes
description: まとめ、クリーンアップ、次のステップ。
---

## 達成したこと

このワークショップでは、以下のことを行いました

1. **通常の AppDynamics 計装で Java サービスをビルドして実行しました**：単一のエージェントが APM データを AppDynamics Controller にのみ送信します。

2. **ハイブリッドモードとデュアルシグナルモードの違いを学びました**：ハイブリッドは AppD 独自の計装を再利用して OTel スパンを生成します（オーバーヘッドが低く、カバレッジが狭い）。一方、デュアルは AppD と並行して完全な OTel Java 自動計装を実行します（カバレッジが広く、相関属性を追加）。

3. **デュアルシグナルモードを有効化しました**：同じプロセスに 4 つの JVM フラグを追加することで実現しました。コード変更なし、追加エージェントなし、再コンパイルなし。同じ AppDynamics エージェントが AppDynamics と Splunk Observability Cloud の両方に同時にデータを送信するようになりました。

4. **グローバルデータリンクを作成しました**：Splunk Observability Cloud で `appd.*` スパン属性を使用して、対応する AppDynamics tier ビューに直接ナビゲートします。

## クリーンアップ

アプリケーションとロードジェネレーターを停止します

```bash
kill %2 2>/dev/null   # load generator
kill %1 2>/dev/null   # java app
```

オプションで Collector を停止します

```bash
sudo systemctl stop splunk-otel-collector
```

## 重要なポイント

- **デュアルモードはコード変更ではなく、設定変更です。** すでに計装されたアプリケーションに JVM フラグを追加することで有効化しました。これにより、アプリケーションコードに触れることなく組織全体に展開することが現実的になります。

- **`appd.*` 相関属性が統合を価値あるものにしています。** これらがなければ（ハイブリッドモード）、Splunk O11y で OTel トレースを取得できますが、特定の AppDynamics ビジネストランザクション、tier、またはアプリケーションにリンクする方法がありません。デュアルモードはそのリンケージを提供します。

- **グローバルデータリンクは相関をワークフローに変えます。** 2 つのツールを手動でクロスリファレンスする代わりに、エンジニアは Splunk O11y トレースから AppDynamics ビューに直接クリックできます。

- **このパターンは段階的な移行をサポートします。** 組織はデュアルモードを一定期間実行して、Splunk Observability Cloud が同じシグナル品質をキャプチャすることを検証できます。その後、サービスごとにデュアルを継続するか、Splunk のみの計装に切り替えるか、AppDynamics を維持するかを決定します。

## 参考資料

- [Enable Dual Signal Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-dual-signal-mode) (AppDynamics ドキュメント)
- [Enable Hybrid Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-hybrid-mode) (AppDynamics ドキュメント)
- [Java Agent Frameworks for OpenTelemetry](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/support-for-appdynamics-for-opentelemetry/java-agent-frameworks-for-opentelemetry) (サポートされるフレームワーク一覧)
- [Global Data Links](https://docs.splunk.com/observability/en/data-visualization/navigate-with-data-links.html) (Splunk Observability ドキュメント)
