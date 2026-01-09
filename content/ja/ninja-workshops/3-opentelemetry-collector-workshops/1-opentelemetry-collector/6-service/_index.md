---
title: OpenTelemetry Collector Service
linkTitle: 6. Service
weight: 6
---

**Service** セクションは、receivers、processors、exporters、extensions セクションで定義された設定に基づいて、Collector でどのコンポーネントを有効にするかを設定するために使用します。

{{% notice style="info" %}}
コンポーネントが設定されていても、**Service** セクション内で定義されていない場合、そのコンポーネントは**有効になりません**。
{{% /notice %}}

service セクションは3つのサブセクションで構成されています：

- extensions
- pipelines
- telemetry

デフォルト設定では、extension セクションは `health_check`、`pprof`、`zpages` を有効にするよう設定されています。これらは先ほど Extensions モジュールで設定しました。

``` yaml
service:
  extensions: [health_check, pprof, zpages]
```

それでは、Metric Pipeline を設定しましょう！
