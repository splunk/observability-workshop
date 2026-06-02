---
title: OpenTelemetry Collector の問題をトラブルシューティングする
linkTitle: 10. OpenTelemetry Collector の問題をトラブルシューティングする
weight: 10
time: 20 minutes
---

前のセクションでは、Collector の構成に debug exporter を追加し、トレースとログのパイプラインに組み込みました。期待どおり、debug 出力がエージェント Collector のログに書き込まれていることを確認できました。

しかし、トレースは o11y cloud に送信されなくなっています。原因を調べて修正していきましょう。

## Collector の構成を確認する

`values.yaml` ファイル経由で Collector の構成を変更した場合は、config map を確認して、Collector に実際に適用されている構成を確認すると役立ちます。

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

エージェント Collector の構成内のログとトレースのパイプラインを確認してみましょう。次のような内容になっているはずです。

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

問題が分かりますか？traces と logs パイプラインに含まれているのは debug exporter のみです。以前 traces パイプラインの構成に存在していた `otlp_http` と `signalfx` の exporter がなくなっています。これが、トレースが o11y cloud に表示されなくなった理由です。また、logs パイプラインからは `splunk_hec/platform_logs` exporter が削除されています。

> 以前にどの exporter が含まれていたかをどうやって把握したのでしょうか？それを知るには、先ほど追加したカスタマイズを元に戻し、config map を確認して traces パイプラインに元々何が含まれていたかを確認する方法があります。あるいは、[splunk-otel-collector-chart の GitHub リポジトリ](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/default/rendered_manifests/configmap-agent.yaml)にある例を参照することもできます。Helm chart で使用されているデフォルトのエージェント構成を確認できます。

## なぜこれらの exporter が削除されたのか？

`values.yaml` ファイルに追加したカスタマイズを確認してみましょう。

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

`helm upgrade` を使って `values.yaml` ファイルを Collector に適用したとき、カスタム構成は以前の Collector 構成とマージされました。このとき、パイプラインセクションの exporter リストのように、リストを含む `yaml` 構成のセクションは、`values.yaml` ファイルに記述された内容（debug exporter のみ）で置き換えられます。

## 問題を修正する

したがって、既存のパイプラインをカスタマイズする際は、その構成部分を完全に再定義する必要があります。`values.yaml` ファイルは次のように更新する必要があります。

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

変更を適用しましょう。

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

その後、エージェントの config map を確認します。

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

今回は、ログとトレースの両方で完全に定義された exporters パイプラインが表示されるはずです。

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

## ログ出力を確認する

**Splunk Distribution of OpenTelemetry .NET** は、ログ記録に `Microsoft.Extensions.Logging` を使用するアプリケーション（このサンプルアプリも含まれます）から、トレースコンテキストでエンリッチされたログを自動的にエクスポートします。

アプリケーションログはトレース メタデータでエンリッチされたうえで、OTLP 形式でローカルの OpenTelemetry Collector インスタンスにエクスポートされます。

debug exporter で取得したログを詳しく確認して、これが実際に行われているかどうかを見てみましょう。Collector のログをテイルするには、次のコマンドを使用します。

``` bash
kubectl logs -l component=otel-collector-agent -f
```

ログをテイルしている状態で、curl を使ってさらにトラフィックを生成します。すると、次のような内容が表示されるはずです。

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

この例では、Trace ID と Span ID が OpenTelemetry .NET インストゥルメンテーションによって自動的にログ出力に書き込まれていることが確認できます。これにより、Splunk Observability Cloud でログとトレースを関連付けることができます。

ただし、Helm を使って K8s クラスターに OpenTelemetry Collector をデプロイし、ログ収集オプションを有効にした場合、OpenTelemetry Collector は File Log receiver を使ってあらゆるコンテナーのログを自動的に取り込むという点も思い出してください。

これにより、アプリケーションのログが重複して取得されてしまいます。たとえば、次のスクリーンショットでは、サービスへの各リクエストに対して 2 つのログエントリが表示されています。

![Duplicate Log Entries](../images/duplicate_logs.png)

これを回避するにはどうすればよいでしょうか？

## K8s での重複ログを回避する

ログの重複を回避するには、`OTEL_LOGS_EXPORTER` 環境変数を `none` に設定して、Splunk Distribution of OpenTelemetry .NET に対して OTLP を使用したログのエクスポートを行わないように指示します。これは、`deployment.yaml` ファイルに `OTEL_LOGS_EXPORTER` 環境変数を追加することで実現できます。

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

そして次のコマンドを実行します。

``` bash
# update the deployment
kubectl apply -f deployment.yaml
```

`OTEL_LOGS_EXPORTER` 環境変数を `none` に設定するのは簡単です。しかし、Trace ID と Span ID がアプリケーションが生成する stdout のログに書き込まれなくなり、ログとトレースを関連付けることができなくなります。

これを解決するには、`/home/splunk/workshop/docker-k8s-otel/helloworld/SplunkTelemetryConfigurator.cs` で定義されている例のように、カスタムロガーを定義する必要があります。

これをアプリケーションに組み込むには、`Program.cs` ファイルを次のように更新します。

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

次に、カスタムロギング構成を含む新しい Docker イメージをビルドします。

``` bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld 

docker build -t helloworld:1.3 .
```

そして、更新したイメージをローカルのコンテナーリポジトリにインポートします。

``` bash
cd /home/splunk

# Tag the image 
docker tag helloworld:1.3 localhost:9999/helloworld:1.3

# Import the image into our local container repo
docker push localhost:9999/helloworld:1.3
```

最後に、コンテナーイメージの 1.3 バージョンを使うように `deployment.yaml` ファイルを更新する必要があります。

``` yaml
    spec:
      containers:
        - name: helloworld
          image: localhost:9999/helloworld:1.3
```

そして変更を適用します。

``` bash
# update the deployment
kubectl apply -f deployment.yaml
```

これで、重複したログエントリがなくなったことが確認できます。残ったログエントリは JSON 形式でフォーマットされており、span ID と trace ID が含まれています。

![JSON Format Logs](../images/logs_json_format.png)
