---
title: APMの自動検出と設定のセットアップ
linkTitle: 4. 自動検出と設定
weight: 5
time: 10分
---

このセクションでは、Kubernetes上で実行されているJavaサービスに対して**自動検出と設定**を有効化します。これにより、OpenTelemetry CollectorがPodアノテーションを検索し、JavaアプリケーションにSplunk OpenTelemetry Javaエージェントで計装を行う必要があることを示します。これにより、クラスター上で実行されているJavaサービスからトレース、スパン、およびプロファイリングデータを取得できるようになります。

{{% notice title="自動検出と設定" style="note" %}}

自動検出と設定は、**コード変更や再コンパイルを必要とせず**にアプリケーションから**トレース、スパン、およびプロファイリング**データを取得するように設計されていることを理解することが重要です。

これはAPMを始めるための優れた方法ですが、手動計装の**代替ではありません**。手動計装では、カスタムスパン、タグ、ログをアプリケーションに追加でき、トレースにより多くのコンテキストと詳細を提供できます。

{{% /notice %}}

Javaアプリケーションの場合、OpenTelemetry Collectorは `instrumentation.opentelemetry.io/inject-java` というアノテーションを検索します。

このアノテーションの値は `true` に設定するか、OpenTelemetry Collectorの `namespace/daemonset`（例：`default/splunk-otel-collector`）に設定できます。これにより、名前空間をまたいで動作することができ、このワークショップではこれを使用します。

{{% notice title="deployment.yamlの使用" style="info" %}}

Podが自動的にトレースを送信するようにしたい場合は、以下に示すように `deployment.yaml` にアノテーションを追加できます。これにより、初期デプロイメント時に計装ライブラリが追加されます。時間を節約するために、以下のPodに対してこれを実施済みです：

- **admin-server**
- **config-server**
- **discovery-server**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: admin-server
  labels:
    app.kubernetes.io/part-of: spring-petclinic
spec:
  selector:
    matchLabels:
      app: admin-server
  template:
    metadata:
      labels:
        app: admin-server
      annotations:
        instrumentation.opentelemetry.io/inject-java: "default/splunk-otel-collector"
```

{{% /notice %}}
