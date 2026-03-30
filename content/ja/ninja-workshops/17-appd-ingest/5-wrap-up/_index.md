---
title: まとめ
linkTitle: 5. まとめ
weight: 5
archetype: chapter
time: 5 minutes
description: まとめ、クリーンアップ、次のステップ
---

## 達成したこと

このワークショップでは、以下のことを行いました：

1. **通常の AppDynamics 計装で Java サービスをビルドして実行しました**：APMデータをAppDynamics Controllerのみに送信する単一のエージェントを使用しました。

2. **ハイブリッドモードとデュアルシグナルモードの違いを学びました**：ハイブリッドモードはAppD独自の計装を再利用してOTelスパンを生成し（低オーバーヘッド、狭いカバレッジ）、デュアルモードはAppDと並行して完全なOTel Java自動計装を実行します（広いカバレッジ、相関属性を追加）。

3. **デュアルシグナルモードを有効にしました**：同じプロセスに4つのJVMフラグを追加することで有効にしました。コード変更なし、2つ目のエージェントなし、再コンパイルなし。同じAppDynamicsエージェントがAppDynamicsとSplunk Observability Cloudの両方に同時にデータを送信するようになりました。

4. **グローバルデータリンクを作成しました**：Splunk Observability Cloudで `appd.*` スパン属性を使用して、対応するAppDynamicsティアビューに直接ナビゲートできるようにしました。

## クリーンアップ

アプリケーションと負荷生成ツールを停止します：

```bash
kill %2 2>/dev/null   # load generator
kill %1 2>/dev/null   # java app
```

オプションでCollectorを停止します：

```bash
sudo systemctl stop splunk-otel-collector
```

## 重要なポイント

- **デュアルモードはコード変更ではなく、設定変更です。** すでに計装されているアプリケーションにJVMフラグを追加することで有効にしました。これにより、アプリケーションコードに触れることなく、組織全体に展開することが実用的になります。

- **`appd.*` 相関属性がこの統合を価値あるものにしています。** これらがない場合（ハイブリッドモード）、Splunk O11yでOTelトレースを取得できますが、特定のAppDynamicsビジネストランザクション、ティア、またはアプリケーションにリンクバックする方法がありません。デュアルモードはそのリンケージを提供します。

- **グローバルデータリンクは相関をワークフローに変えます。** 2つのツールを手動でクロスリファレンスする代わりに、エンジニアはSplunk O11yトレースからAppDynamicsビューに直接クリックで移動できます。

- **このパターンは段階的な移行をサポートします。** 組織はデュアルモードを一定期間実行して、Splunk Observability Cloudが同じシグナル品質をキャプチャすることを検証し、その後サービスごとにデュアルを継続するか、Splunkのみの計装に切り替えるか、AppDynamicsを維持するかを決定できます。

## 参考資料

- [Enable Dual Signal Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-dual-signal-mode) -- AppDynamicsドキュメント
- [Enable Hybrid Mode](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/instrument-applications-with-splunk-appdynamics-for-opentelemetry/enable-opentelemetry-in-the-java-agent/enable-hybrid-mode) -- AppDynamicsドキュメント
- [Java Agent Frameworks for OpenTelemetry](https://help.splunk.com/en/appdynamics-on-premises/virtual-appliance-self-hosted/25.7.0/splunk-appdynamics-for-opentelemetry/support-for-appdynamics-for-opentelemetry/java-agent-frameworks-for-opentelemetry) -- サポートされているフレームワーク一覧
- [Global Data Links](https://docs.splunk.com/observability/en/data-visualization/navigate-with-data-links.html) -- Splunk Observabilityドキュメント
