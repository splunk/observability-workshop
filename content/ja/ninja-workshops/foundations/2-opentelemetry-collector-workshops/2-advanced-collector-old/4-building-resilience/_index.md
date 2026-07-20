---
title: 4. レジリエンスの構築
linkTitle: 4. レジリエンスの構築
time: 10 minutes
weight: 6
---

OpenTelemetry Collectorの [**FileStorage Extension**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/19bc7d6ee854c0c1b5c97d8d348e5b9d1199e8aa/extension/storage/filestorage/README.md) は、信頼性の高いチェックポイント機能、リトライ管理、一時的な障害の効果的な処理を提供することで、テレメトリパイプラインのレジリエンスを強化します。

この拡張機能を有効にすると、OpenTelemetry Collectorは中間状態をディスクに保存できるため、ネットワーク障害時のデータ損失を防ぎ、シームレスに操作を再開できます。

{{% notice note %}}

このソリューションは、接続のダウンタイムが短い場合（最大15分）にMetricに対して機能します。ダウンタイムがこれを超えると、データポイントの順序が乱れるため、Splunk Observability Cloudはデータを破棄します。

ログについては、今後のSplunk OpenTelemetry Collectorリリースで、よりエンタープライズ対応のソリューションを実装する計画があります。

{{% /notice %}}

{{% notice title="演習" style="green" icon="running" %}}

- `[WORKSHOP]`ディレクトリ内に、`4-resilience`という名前の新しいサブディレクトリを作成します。
- 次に、`3-filelog`ディレクトリから`*.yaml`を`4-resilience`にコピーします。

> [!IMPORTANT]
> **すべてのターミナルウィンドウを `[WORKSHOP]/4-resilience` ディレクトリに変更してください。**

更新後のディレクトリ構造は次のようになります

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
