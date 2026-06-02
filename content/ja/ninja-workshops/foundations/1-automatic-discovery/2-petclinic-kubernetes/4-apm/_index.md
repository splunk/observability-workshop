---
title: APM 向け自動検出と自動構成のセットアップ
linkTitle: 4. 自動検出と自動構成
weight: 5
time: 10 minutes
---

このセクションでは、Kubernetes 上で実行されている Java サービスに対して **自動検出と自動構成** を有効にします。これにより、OpenTelemetry Collector は Pod のアノテーションを参照して、Java アプリケーションを Splunk OpenTelemetry Java エージェントでインストルメントすべきかどうかを判断します。これによって、クラスター上で実行されている Java サービスからトレース、スパン、プロファイリングデータを取得できるようになります。

{{% notice title="自動検出と自動構成" style="note" %}}

自動検出と自動構成は、**コードの変更や再コンパイルを必要とせずに**、アプリケーションから **トレース、スパン、プロファイリング** データを取得することを目的に設計されている点を理解しておくことが重要です。

これは APM を始めるうえで非常に便利な方法ですが、手動インストルメンテーションの代替には **なりません**。手動インストルメンテーションでは、カスタムスパン、タグ、ログをアプリケーションに追加でき、トレースに対してより多くのコンテキストと詳細情報を付与できます。

{{% /notice %}}

Java アプリケーションの場合、OpenTelemetry Collector はアノテーション `instrumentation.opentelemetry.io/inject-java` を参照します。

このアノテーションには、値として `true` を指定するか、OpenTelemetry Collector の `namespace/daemonset`（例：`default/splunk-otel-collector`）を指定できます。後者の方式を使うと名前空間をまたいで動作させることができ、本ワークショップではこちらを使用します。

{{% notice title="deployment.yaml の使用" style="info" %}}

Pod が自動的にトレースを送信するようにしたい場合は、以下のように `deployment.yaml` にアノテーションを追加できます。これによって、初回のデプロイ時にインストルメンテーションライブラリが追加されます。作業を効率化するため、以下の Pod についてはすでにこの設定を行っています:

- **admin-server**
- **config-server**
- **discovery-server**

``` yaml
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
