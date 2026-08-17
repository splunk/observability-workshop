---
title: OpenTelemetry Collectorの問題をトラブルシュート
linkTitle: 10. OpenTelemetry Collectorの問題をトラブルシュート
weight: 10
time: 20 minutes
---

前のセクションでは、コレクター設定にdebug exporterを追加し、
traceとlogのパイプラインの一部として設定しました。期待通り、debug出力が
agent collectorのlogに書き込まれていることが確認できます。

しかし、traceがo11y cloudに送信されなくなりました。原因を特定して修正しましょう。

## コレクター設定の確認

`values.yaml` ファイルを使用してコレクター設定を変更した場合は、
config mapを確認して、コレクターに適用された実際の設定を確認すると便利です

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

agent collectorの設定にあるlogとtraceのパイプラインを確認しましょう。以下のように
なっているはずです

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

問題がわかりますか？traceとlogのパイプラインにはdebug exporterしか含まれていません。
以前traceパイプラインの設定に存在していた `otlp_http` と `signalfx` のexporterがなくなっています。
これが、o11y cloudでtraceが表示されなくなった原因です。また、logパイプラインからは
`splunk_hec/platform_logs` exporterが削除されています。

> 以前どの特定のexporterが含まれていたかをどうやって知ったのでしょうか？確認するには、
> 以前のカスタマイズを元に戻してからconfig mapを確認し、traceパイプラインに
> 元々何が含まれていたかを確認する方法があります。あるいは、
> [GitHub repo for splunk-otel-collector-chart](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/default/rendered_manifests/configmap-agent.yaml)
> の例を参照して、Helmチャートで使用されるデフォルトのagent設定を確認することもできます。

## これらのexporterはなぜ削除されたのか？

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

`helm upgrade` を使用して `values.yaml` ファイルをコレクターに適用すると、
カスタム設定が以前のコレクター設定とマージされます。
この際、パイプラインセクションのexporterリストのように、リストを含む `yaml` 設定の
セクションは、`values.yaml` ファイルに含めた内容（この場合はdebug exporterのみ）で
置き換えられます。

## 問題を修正しましょう

そのため、既存のパイプラインをカスタマイズする場合は、設定のその部分を完全に再定義する必要があります。
`values.yaml` ファイルを以下のように更新する必要があります

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

次に、agent config mapを確認します

``` bash
kubectl describe cm splunk-otel-collector-otel-agent
```

今回は、logとtraceの両方で完全に定義されたexporterパイプラインが表示されるはずです

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

**Splunk Distribution of OpenTelemetry .NET** は、`Microsoft.Extensions.Logging` を使用してログを記録する
アプリケーション（サンプルアプリもこれを使用しています）から、トレーシングコンテキストが付与されたログを
自動的にエクスポートします。

アプリケーションログにはトレーシングメタデータが付与され、OTLP形式でローカルの
OpenTelemetry Collectorインスタンスにエクスポートされます。

debug exporterでキャプチャされたログを詳しく確認して、これが実際に行われているか見てみましょう。
コレクターのログをtailするには、以下のコマンドを使用します

``` bash
kubectl logs -l component=otel-collector-agent -f
```

ログをtailしている状態で、curlを使用してトラフィックを生成します。すると、以下のような
出力が表示されるはずです

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

この例では、OpenTelemetry .NETの計装によって、Trace IDとSpan IDがログ出力に
自動的に書き込まれていることがわかります。これにより、Splunk Observability Cloudで
ログとトレースを関連付けることができます。

ただし、Helmを使用してK8sクラスターにOpenTelemetry Collectorをデプロイし、
ログ収集オプションを含めた場合、OpenTelemetry CollectorはFile Log receiverを使用して
コンテナログを自動的にキャプチャすることを覚えているかもしれません。

これにより、アプリケーションのログが重複してキャプチャされることになります。例えば、以下のスクリーンショットでは、
サービスへの各リクエストに対して2つのログエントリが表示されています

![Duplicate Log Entries](../images/duplicate_logs.png)

これをどのように回避すればよいでしょうか？

## K8sでのログの重複を回避する

ログの重複キャプチャを回避するには、`OTEL_LOGS_EXPORTER` 環境変数を `none` に設定して、
Splunk Distribution of OpenTelemetry .NETがOTLPを使用してコレクターにログをエクスポートしないように
指定します。これは、`deployment.yaml` ファイルに `OTEL_LOGS_EXPORTER` 環境変数を追加することで
実現できます

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

そして以下を実行します

``` bash
# update the deployment
kubectl apply -f deployment.yaml
```

`OTEL_LOGS_EXPORTER` 環境変数を `none` に設定するのは簡単です。しかし、Trace IDと
Span IDはアプリケーションが生成するstdoutログには書き込まれないため、
ログとトレースを関連付けることができなくなります。

これを解決するには、カスタムロガーを定義する必要があります。例えば、
`/home/splunk/workshop/docker-k8s-otel/helloworld/SplunkTelemetryConfigurator.cs` に
定義されている例を使用できます。

`Program.cs` ファイルを以下のように更新することで、アプリケーションに組み込むことができます

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

次に、カスタムログ設定を含む新しいDockerイメージをビルドします

``` bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld 

docker build -t helloworld:1.3 .
```

そして、更新されたイメージをローカルコンテナリポジトリにインポートします

``` bash
cd /home/splunk

# Tag the image 
docker tag helloworld:1.3 localhost:9999/helloworld:1.3

# Import the image into our local container repo
docker push localhost:9999/helloworld:1.3
```

最後に、コンテナイメージのバージョン1.3を使用するように `deployment.yaml` ファイルを
更新する必要があります

``` yaml
    spec:
      containers:
        - name: helloworld
          image: localhost:9999/helloworld:1.3
```

そして変更を適用します

``` bash
# update the deployment
kubectl apply -f deployment.yaml
```

これで、重複したログエントリが解消されたことが確認できます。残りのログエントリは
JSON形式でフォーマットされ、spanとtrace IDが含まれています

![JSON Format Logs](../images/logs_json_format.png)
