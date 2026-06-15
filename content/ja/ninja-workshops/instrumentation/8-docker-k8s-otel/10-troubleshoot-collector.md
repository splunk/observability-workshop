---
title: OpenTelemetry Collector の問題をトラブルシュートする
linkTitle: 10. OpenTelemetry Collector の問題をトラブルシュートする
weight: 10
time: 20 minutes
---

前のセクションでは、Collector の設定に debug エクスポーターを追加し、トレースとログのパイプラインの一部にしました。期待どおり、エージェント Collector のログに debug 出力が書き込まれることを確認しました。

しかし、トレースが o11y cloud に送信されなくなりました。原因を特定して修正しましょう。

## Collector 設定の確認

`values.yaml` ファイルを通じて Collector の設定を変更した場合、config map を確認して、Collector に実際に適用された設定を確認することが有効です

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

エージェント Collector 設定のログとトレースのパイプラインを確認しましょう。以下のようになっているはずです

``` yaml
  pipelines:
    logs:
      exporters:
      - debug
      processors:
      - memory_limiter
      - k8s_attributes
      - filter/logs
      - batch
      - resourcedetection
      - resource
      - resource/logs
      - resource/add_environment
      receivers:
      - filelog
      - otlp
    ...
    traces:
      exporters:
      - debug
      processors:
      - memory_limiter
      - k8s_attributes
      - batch
      - resourcedetection
      - resource
      - resource/add_environment
      receivers:
      - otlp
      - jaeger
      - zipkin
```

問題がわかりますか？トレースとログのパイプラインに debug エクスポーターしか含まれていません。以前トレースパイプラインの設定に存在していた `otlp_http` と `signalfx` エクスポーターがなくなっています。これが o11y cloud でトレースが表示されなくなった原因です。また、ログパイプラインでは `splunk_hec/platform_logs` エクスポーターが削除されています。

> 以前どのエクスポーターが含まれていたかをどうやって知ることができるのでしょうか？確認するには、以前のカスタマイズを元に戻してから config map を確認し、トレースパイプラインに元々何が含まれていたかを見る方法があります。あるいは、[GitHub repo for splunk-otel-collector-chart](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/default/rendered_manifests/configmap-agent.yaml) のサンプルを参照することで、Helm chart が使用するデフォルトのエージェント設定を確認できます。

## なぜこれらのエクスポーターが削除されたのか？

`values.yaml` ファイルに追加したカスタマイズを確認しましょう

``` yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
  config:
    receivers:
     ...
    exporters:
      debug:
        verbosity: detailed
    service:
      pipelines:
        traces:
          exporters:
            - debug
        logs:
          exporters:
            - debug
```

`helm upgrade` を使用して `values.yaml` ファイルを Collector に適用すると、カスタム設定が以前の Collector 設定とマージされます。この際、パイプラインセクションのエクスポーターリストのようなリストを含む `yaml` 設定のセクションは、`values.yaml` ファイルに含まれている内容（この場合は debug エクスポーターのみ）で置き換えられます。

## 問題を修正する

既存のパイプラインをカスタマイズする場合、設定のその部分を完全に再定義する必要があります。`values.yaml` ファイルを以下のように更新する必要があります

``` yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
  config:
    receivers:
     ...
    exporters:
      debug:
        verbosity: detailed
    service:
      pipelines:
        traces:
          exporters:
            - otlp_http
            - signalfx
            - debug
        logs:
          exporters:
            - splunk_hec/platform_logs
            - debug
```

変更を適用しましょう

``` bash
helm upgrade splunk-otel-collector \
  --set="splunkObservability.realm=$REALM" \
  --set="splunkObservability.accessToken=$ACCESS_TOKEN" \
  --set="clusterName=$INSTANCE-cluster" \
  --set="environment=otel-$INSTANCE" \
  --set="splunkPlatform.token=$HEC_TOKEN" \
  --set="splunkPlatform.endpoint=$HEC_URL" \
  --set="splunkPlatform.index=splunk4rookies-workshop" \
  -f values.yaml \
splunk-otel-collector-chart/splunk-otel-collector
```

次に、エージェントの config map を確認します

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

今回は、ログとトレースの両方で完全に定義されたエクスポーターパイプラインが表示されるはずです

``` bash
  pipelines:
    logs:
      exporters:
      - splunk_hec/platform_logs
      - debug
      processors:
      ...
    traces:
      exporters:
      - otlp_http
      - signalfx
      - debug
      processors:
      ...
```

## ログ出力の確認

**Splunk Distribution of OpenTelemetry .NET** は、ログに `Microsoft.Extensions.Logging` を使用するアプリケーション（サンプルアプリがこれに該当します）から、トレーシングコンテキストで強化されたログを自動的にエクスポートします。

アプリケーションログはトレーシングメタデータで強化され、OTLP 形式でローカルの OpenTelemetry Collector インスタンスにエクスポートされます。

debug エクスポーターでキャプチャされたログを詳しく確認して、これが実際に行われているか見てみましょう。Collector のログをテールするには、以下のコマンドを使用します

``` bash
kubectl logs -l component=otel-collector-agent -f
```

ログをテールしている状態で、curl を使用してトラフィックを生成します。すると、以下のような出力が表示されるはずです

````
2024-12-20T21:56:30.858Z info Logs {"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 1}
2024-12-20T21:56:30.858Z info ResourceLog #0
Resource SchemaURL: https://opentelemetry.io/schemas/1.6.1
Resource attributes:
     -> splunk.distro.version: Str(1.8.0)
     -> telemetry.distro.name: Str(splunk-otel-dotnet)
     -> telemetry.distro.version: Str(1.8.0)
     -> os.type: Str(linux)
     -> os.description: Str(Debian GNU/Linux 12 (bookworm))
     -> os.build_id: Str(6.8.0-1021-aws)
     -> os.name: Str(Debian GNU/Linux)
     -> os.version: Str(12)
     -> host.name: Str(derek-1)
     -> process.owner: Str(app)
     -> process.pid: Int(1)
     -> process.runtime.description: Str(.NET 8.0.11)
     -> process.runtime.name: Str(.NET)
     -> process.runtime.version: Str(8.0.11)
     -> container.id: Str(5bee5b8f56f4b29f230ffdd183d0367c050872fefd9049822c1ab2aa662ba242)
     -> telemetry.sdk.name: Str(opentelemetry)
     -> telemetry.sdk.language: Str(dotnet)
     -> telemetry.sdk.version: Str(1.9.0)
     -> service.name: Str(helloworld)
     -> deployment.environment: Str(otel-derek-1)
     -> k8s.node.name: Str(derek-1)
     -> k8s.cluster.name: Str(derek-1-cluster)
ScopeLogs #0
ScopeLogs SchemaURL: 
InstrumentationScope HelloWorldController 
LogRecord #0
ObservedTimestamp: 2024-12-20 21:56:28.486804 +0000 UTC
Timestamp: 2024-12-20 21:56:28.486804 +0000 UTC
SeverityText: Information
SeverityNumber: Info(9)
Body: Str(/hello endpoint invoked by {name})
Attributes:
     -> name: Str(Kubernetes)
Trace ID: 78db97a12b942c0252d7438d6b045447
Span ID: 5e9158aa42f96db3
Flags: 1
 {"kind": "exporter", "data_type": "logs", "name": "debug"}
````

この例では、OpenTelemetry .NET インストルメンテーションによって Trace ID と Span ID が自動的にログ出力に書き込まれていることがわかります。これにより、Splunk Observability Cloud でログとトレースを相関付けることができます。

ただし、Helm を使用して K8s クラスターに OpenTelemetry Collector をデプロイし、ログ収集オプションを含めた場合、OpenTelemetry Collector は File Log receiver を使用してコンテナログを自動的にキャプチャすることを思い出してください。

これにより、アプリケーションのログが重複してキャプチャされます。例えば、以下のスクリーンショットでは、サービスへの各リクエストに対して 2 つのログエントリが表示されています

![Duplicate Log Entries](../images/duplicate_logs.png)

これを回避するにはどうすればよいでしょうか？

## K8s でのログ重複の回避

ログの重複キャプチャを回避するには、`OTEL_LOGS_EXPORTER` 環境変数を `none` に設定して、Splunk Distribution of OpenTelemetry .NET が OTLP を使用して Collector にログをエクスポートしないようにします。これは `deployment.yaml` ファイルに `OTEL_LOGS_EXPORTER` 環境変数を追加することで実現できます

``` yaml
          env:
            - name: PORT
              value: "8080"
            - name: NODE_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.hostIP
            - name: OTEL_EXPORTER_OTLP_ENDPOINT
              value: "http://$(NODE_IP):4318"
            - name: OTEL_SERVICE_NAME
              value: "helloworld"
            - name: OTEL_RESOURCE_ATTRIBUTES 
              value: "deployment.environment=otel-$INSTANCE" 
            - name: OTEL_LOGS_EXPORTER 
              value: "none" 
```

その後、以下を実行します

``` bash
# update the deployment
kubectl apply -f deployment.yaml
```

`OTEL_LOGS_EXPORTER` 環境変数を `none` に設定するのは簡単です。しかし、アプリケーションが生成する stdout ログには Trace ID と Span ID が書き込まれないため、ログとトレースの相関付けができなくなります。

この問題を解決するには、カスタムロガーを定義する必要があります。例えば、`/home/splunk/workshop/docker-k8s-otel/helloworld/SplunkTelemetryConfigurator.cs` に定義されているサンプルを使用できます。

`Program.cs` ファイルを以下のように更新することで、アプリケーションにこれを含めることができます

``` cs
using SplunkTelemetry;
using Microsoft.Extensions.Logging.Console;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

SplunkTelemetryConfigurator.ConfigureLogger(builder.Logging);

var app = builder.Build();

app.MapControllers();

app.Run();
```

次に、カスタムログ設定を含む新しい Docker イメージをビルドします

``` bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld 

docker build -t helloworld:1.3 .
```

更新したイメージをローカルのコンテナリポジトリにインポートします

``` bash
cd /home/splunk

# Tag the image 
docker tag helloworld:1.3 localhost:9999/helloworld:1.3

# Import the image into our local container repo
docker push localhost:9999/helloworld:1.3
```

最後に、コンテナイメージのバージョン 1.3 を使用するように `deployment.yaml` ファイルを更新する必要があります

``` yaml
    spec:
      containers:
        - name: helloworld
          image: localhost:9999/helloworld:1.3
```

変更を適用します

``` bash
# update the deployment
kubectl apply -f deployment.yaml
```

これで、重複したログエントリが解消されたことが確認できます。残りのログエントリは JSON 形式でフォーマットされ、span ID と trace ID が含まれています

![JSON Format Logs](../images/logs_json_format.png)
