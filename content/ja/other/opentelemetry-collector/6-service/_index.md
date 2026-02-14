---
title: OpenTelemetry Collector サービス
linkTitle: 6. サービス
weight: 6
---

**Service** セクションでは、レシーバー、プロセッサー、エクスポーター、およびエクステンションにある設定に基づいて、コレクターで有効にするコンポーネントを設定していきます。


{{% notice style="info" %}}
コンポーネントが設定されていても、**Service** セクション内で定義されていない場合、そのコンポーネントは**有効化されません**。
{{% /notice %}}

サービスのセクションは、以下の3つのサブセクションで構成されています

- extensions（拡張機能）
- pipelines（パイプライン）
- telemetry（テレメトリー）

デフォルトの設定では、拡張機能セクションが `health_check`、`pprof`、`zpages` を有効にするように設定されており、これらは以前のエクステンションのモジュールで設定しました。

``` yaml
service:
  extensions: [health_check, pprof, zpages]
```

それでは、メトリックパイプラインを設定していきましょう！
