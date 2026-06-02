---
title: OpenTelemetry Collector Service
linkTitle: 6. Service
weight: 6
---

**Service** セクションは、receivers、processors、exporters、extensions の各セクションに定義された設定をもとに、Collector で有効化するコンポーネントを指定するために使用します。

{{% notice style="info" %}}
コンポーネントが設定されていても、**Service** セクション内で定義されていなければ、そのコンポーネントは有効化**されません**。
{{% /notice %}}

service セクションは、次の3つのサブセクションで構成されています。

- extensions
- pipelines
- telemetry

デフォルトの設定では、extension セクションに `health_check`、`pprof`、`zpages` を有効化する設定が記述されており、これらは先ほど Extensions モジュールで設定した内容です。

``` yaml
service:
  extensions: [health_check, pprof, zpages]
```

それでは、Metric Pipeline を設定していきましょう！
