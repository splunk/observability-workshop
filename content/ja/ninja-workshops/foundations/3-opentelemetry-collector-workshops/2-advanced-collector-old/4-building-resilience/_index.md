---
title: 4. レジリエンスの組み込み
linkTitle: 4. レジリエンスの構築
time: 10 minutes
weight: 6
---

OpenTelemetry Collector の [**FileStorage Extension**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/19bc7d6ee854c0c1b5c97d8d348e5b9d1199e8aa/extension/storage/filestorage/README.md) は、信頼性の高いチェックポイント機能、リトライ管理、および一時的な障害への効果的な対応を提供することで、テレメトリーパイプラインのレジリエンスを高めます。

この拡張機能を有効にすると、OpenTelemetry Collector は中間状態をディスクに保存できるようになり、ネットワーク障害時のデータ損失を防ぎ、シームレスに処理を再開できます。

{{% notice note %}}

このソリューションは、接続ダウンタイムが短時間（最大 15 分）であればメトリクスでも動作します。ダウンタイムがこれを超えると、データポイントの順序が崩れることにより Splunk Observability Cloud はデータをドロップします。

ログについては、今後の Splunk OpenTelemetry Collector のリリースで、よりエンタープライズ向けのソリューションを実装する計画があります。

{{% /notice %}}

{{% notice title="演習" style="green" icon="running" %}}

- `[WORKSHOP]` ディレクトリ内に、`4-resilience` という名前の新しいサブディレクトリを作成します。
- 次に、`3-filelog` ディレクトリから `*.yaml` を `4-resilience` にコピーします。

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `[WORKSHOP]/4-resilience` ディレクトリに変更してください。**

更新後のディレクトリ構造は次のようになります。

```text { title="Updated Directory Structure" }
.
├── agent.yaml
└── gateway.yaml
```

{{% /notice %}}
