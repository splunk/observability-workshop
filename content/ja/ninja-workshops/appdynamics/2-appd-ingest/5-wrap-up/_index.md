---
title: まとめ
linkTitle: 5. まとめ
weight: 5
archetype: chapter
time: 5 minutes
description: サマリー、クリーンアップ、次のステップ。
---

## 達成したこと

このワークショップでは以下を行いました:

1. **通常のAppDynamics計装でJavaサービスをビルドして実行しました** — 単一のエージェントがAPMデータをAppDynamics Controllerのみに送信する構成です。

2. **ハイブリッドモードとデュアルシグナルモードの違いを学びました** — ハイブリッドはAppD自体の計装を再利用してOTel Spanを生成します（オーバーヘッドが低く、カバレッジは狭い）。一方、デュアルはAppDと並行して完全なOTel Java自動計装を実行します（カバレッジが広く、相関属性を追加）。

3. **デュアルシグナルモードを有効にしました** — 同じプロセスに4つのJVMフラグを追加するだけです。コード変更なし、2つ目のエージェントなし、再コンパイルなし。同じAppDynamicsエージェントがAppDynamicsとSplunk Observability Cloudの両方に同時にデータを送信するようになります。

4. **グローバルデータリンクを作成しました** — Splunk Observability Cloudで `appd.*` Span属性を使用して、対応するAppDynamicsのティアビューに直接移動できるようにしました。

## クリーンアップ

アプリケーションとロードジェネレーターを停止します:

```bash
kill %2 2>/dev/null   # load generator
kill %1 2>/dev/null   # java app
```

必要に応じてCollectorを停止します:

```bash
sudo systemctl stop splunk-otel-collector
```

## 重要なポイント

- **デュアルモードはコード変更ではなく、設定変更です。** すでに計装済みのアプリケーションにJVMフラグを追加することで有効にしました。これにより、アプリケーションコードに手を加えることなく、組織全体にロールアウトすることが実用的になります。

- **`appd.*` 相関属性が統合を価値あるものにしています。** これらがない場合（ハイブリッドモード）、Splunk O11yでOTelトレースは取得できますが、特定のAppDynamicsビジネストランザクション、ティア、またはアプリケーションに戻るリンクがありません。デュアルモードはそのリンクを提供します。

- **グローバルデータリンクは相関をワークフローに変えます。** 2つのツールを手動で相互参照する代わりに、エンジニアはSplunk O11yのトレースからAppDynamicsビューに直接クリックして移動できます。

- **このパターンは段階的な移行をサポートします。** 組織はSplunk Observability Cloudが同じシグナル品質をキャプチャしていることを検証するために一定期間デュアルモードを実行し、その後サービスごとにデュアルを継続するか、Splunkのみの計装に切り替えるか、AppDynamicsを継続するかを決定できます。

## 参考資料

- [Enable Dual Signal Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-dual-signal-mode)（AppDynamicsドキュメント）
- [Enable Hybrid Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-hybrid-mode)（AppDynamicsドキュメント）
- [Java Agent Frameworks for OpenTelemetry](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/support-for-appdynamics-for-opentelemetry/java-agent-frameworks-for-opentelemetry)（サポートされるフレームワークリスト）
- [Global Data Links](https://docs.splunk.com/observability/en/data-visualization/navigate-with-data-links.html)（Splunk Observabilityドキュメント）
