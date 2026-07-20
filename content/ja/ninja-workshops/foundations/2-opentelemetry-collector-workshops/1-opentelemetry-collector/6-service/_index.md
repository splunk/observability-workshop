---
title: OpenTelemetry Collector Service
linkTitle: 6. Service
weight: 6
---

**Service** セクションは、Receiver、Processor、Exporter、Extension セクションの設定に基づいて、Collectorでどのコンポーネントを有効にするかを構成するために使用します。

{{% notice style="info" %}}
コンポーネントが構成されていても、**Service** セクション内で定義されていない場合、そのコンポーネントは有効に **なりません**。
{{% /notice %}}

Serviceセクションは3つのサブセクションで構成されています

- extensions
- pipelines
- telemetry

デフォルトの構成では、extensionセクションで `health_check`、`pprof`、`zpages` が有効になるよう設定されています。これらは先ほどExtensionsモジュールで構成したものです。

``` yaml
service:
  extensions: [health_check, pprof, zpages]
```

それでは、Metric Pipelineを構成しましょう！
