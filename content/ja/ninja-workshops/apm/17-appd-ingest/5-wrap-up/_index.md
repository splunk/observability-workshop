---
title: Wrap Up
linkTitle: 5. Wrap Up
weight: 5
archetype: chapter
time: 5 minutes
description: まとめ、クリーンアップ、次のステップ。
---

## 達成したこと

このワークショップでは、以下を行いました。

1. **通常の AppDynamics インストルメンテーションで Java サービスをビルドして実行**: APM データを AppDynamics Controller のみに送信する単一エージェントを使用しました。

2. **hybrid モードと dual signal モードの違いを理解**: hybrid は AppD 自身のインストルメンテーションを再利用して OTel スパンを生成します（オーバーヘッドが低く、カバー範囲は狭い）。一方、dual は AppD と並行して OTel Java auto-instrumentation の全機能を実行します（カバー範囲が広く、相関属性が追加されます）。

3. **dual signal モードを有効化**: 同一プロセスに 4 つの JVM フラグを追加するだけで実現しました。コード変更も、2 つ目のエージェントも、再コンパイルも不要です。同じ AppDynamics エージェントが、AppDynamics と Splunk Observability Cloud の両方に同時にデータを送信できるようになりました。

4. **Global data link を作成**: Splunk Observability Cloud で `appd.*` スパン属性を使用し、対応する AppDynamics tier ビューに直接遷移できるようにしました。

## クリーンアップ

アプリケーションと負荷生成ツールを停止します。

```bash
kill %2 2>/dev/null   # load generator
kill %1 2>/dev/null   # java app
```

必要に応じて collector を停止します。

```bash
sudo systemctl stop splunk-otel-collector
```

## 重要なポイント

- **dual モードはコード変更ではなく、設定変更です。** すでにインストルメント済みのアプリケーションに JVM フラグを追加するだけで有効化できました。これにより、アプリケーションコードに手を加えることなく、組織全体への展開が現実的になります。

- **`appd.*` 相関属性こそが、この統合に価値をもたらします。** これらが無い場合（hybrid モード）、Splunk O11y で OTel トレースは取得できますが、特定の AppDynamics ビジネストランザクション、tier、アプリケーションに紐付ける手段がありません。dual モードはその紐付けを提供します。

- **Global data link は相関をワークフローへと変換します。** 2 つのツールを手作業で相互参照する代わりに、エンジニアは Splunk O11y のトレースから AppDynamics のビューに直接クリックで移動できます。

- **このパターンは段階的な移行を可能にします。** 組織は一定期間 dual モードを実行することで、Splunk Observability Cloud が同等のシグナル品質を捕捉していることを検証できます。その後、サービスごとに dual を継続するか、Splunk のみのインストルメンテーションに切り替えるか、AppDynamics に留まるかを判断できます。

## 参考情報

- [Enable Dual Signal Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-dual-signal-mode) (AppDynamics ドキュメント)
- [Enable Hybrid Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-hybrid-mode) (AppDynamics ドキュメント)
- [Java Agent Frameworks for OpenTelemetry](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/support-for-appdynamics-for-opentelemetry/java-agent-frameworks-for-opentelemetry) (サポート対象フレームワーク一覧)
- [Global Data Links](https://docs.splunk.com/observability/en/data-visualization/navigate-with-data-links.html) (Splunk Observability ドキュメント)
