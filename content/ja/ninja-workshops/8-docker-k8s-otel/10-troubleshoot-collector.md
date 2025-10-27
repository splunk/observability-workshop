---
title: Troubleshoot OpenTelemetry Collector Issues
linkTitle: 10. Troubleshoot OpenTelemetry Collector Issues
weight: 10
time: 20 minutes
---

前のセクションでは、debug エクスポーターをコレクターの設定に追加し、
トレースとログのパイプラインの一部にしました。期待通りに、debug 出力が
エージェントコレクターのログに書き込まれているのが確認できます。

しかし、トレースが o11y cloud に送信されなくなっています。なぜなのかを把握して修正しましょう。

## コレクター設定を確認する

`values.yaml`ファイルを通じてコレクター設定が変更された場合は、
config map を確認してコレクターに実際に適用された設定を確認することが役立ちます：

```bash
kubectl describe cm splunk-otel-collector-otel-agent
```

エージェントコレクター設定のログとトレースのパイプラインを確認しましょう。次のようになっているはずです：

```yaml
  pipelines:
    logs:
      exporters:
      - debug
      processors:
      - memory_limiter
      - k8sattributes
      - filter/logs
      - batch
      - resourcedetection
      - resource
      - resource/logs
      - resource/add_environment
      receivers:
      - filelog
      - fluentforward
      - otlp
    ...
    traces:
      exporters:
      - debug
      processors:
      - memory_limiter
      - k8sattributes
      - batch
      - resourcedetection
      - resource
      - resource/add_environment
      receivers:
      - otlp
      - jaeger
      - smartagent/signalfx-forwarder
      - zipkin
```

問題がわかりますか？debug エクスポーターのみがトレースとログのパイプラインに含まれています。
以前のトレースパイプライン設定にあった`otlphttp`と`signalfx`エクスポーターがなくなっています。
これが、もう o11y cloud でトレースが見えなくなった理由です。ログパイプラインについても、`splunk_hec/platform_logs`
エクスポーターが削除されています。

> どのような特定のエクスポーターが以前含まれていたかをどのように知ったか？それを見つけるには、
> 以前のカスタマイズを元に戻してから、config map を確認して
> トレースパイプラインに元々何が含まれていたかを見ることもできました。あるいは、
> [splunk-otel-collector-chart の GitHub リポジトリ](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/default/rendered_manifests/configmap-agent.yaml)
> の例を参照することもでき、これにより Helm チャートで使用されるデフォルトのエージェント設定が分かります。

## これらのエクスポーターはどのように削除されたのか？

`values.yaml`ファイルに追加したカスタマイズを確認しましょう：

```yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
  config:
    receivers: ...
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

`helm upgrade`を使ってコレクターに`values.yaml`ファイルを適用したとき、
カスタム設定は以前のコレクター設定とマージされました。
これが発生すると、リストを含む`yaml`設定のセクション、
例えばパイプラインセクションのエクスポーターのリストは、`values.yaml`ファイルに
含めたもの（debug エクスポーターのみ）で置き換えられます。

## 問題を修正しましょう

既存のパイプラインをカスタマイズする場合、設定のその部分を完全に再定義する必要があります。
したがって、`values.yaml`ファイルを次のように更新する必要があります：

```yaml
logsEngine: otel
splunkObservability:
  infrastructureMonitoringEventsEnabled: true
agent:
  config:
    receivers: ...
    exporters:
      debug:
        verbosity: detailed
    service:
      pipelines:
        traces:
          exporters:
            - otlphttp
            - signalfx
            - debug
        logs:
          exporters:
            - splunk_hec/platform_logs
            - debug
```

変更を適用しましょう：

```bash
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

それからエージェント config map を確認します：

```bash
kubectl describe cm splunk-otel-collector-otel-agent
```

今度は、ログとトレースの両方について完全に定義されたエクスポーターパイプラインが表示されるはずです：

```bash
  pipelines:
    logs:
      exporters:
      - splunk_hec/platform_logs
      - debug
      processors:
      ...
    traces:
      exporters:
      - otlphttp
      - signalfx
      - debug
      processors:
      ...
```

## ログ出力の確認

**Splunk Distribution of OpenTelemetry .NET**は、ログに使用するアプリケーション
（サンプルアプリでも使用している）から、トレースコンテキストで強化されたログを自動的にエクスポートします。

アプリケーションログはトレースメタデータで強化され、その後
OpenTelemetry Collector のローカルインスタンスに OTLP 形式でエクスポートされます。

debug エクスポーターによってキャプチャされたログを詳しく見て、それが発生しているかを確認しましょう。
コレクターログを tail するには、次のコマンドを使用できます：

```bash
kubectl logs -l component=otel-collector-agent -f
```

ログを tail したら、curl を使ってさらにトラフィックを生成できます。そうすると
次のようなものが表示されるはずです：

```
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
```

この例では、Trace ID と Span ID が
OpenTelemetry .NET 計装によってログ出力に自動的に書き込まれていることがわかります。これにより、
Splunk Observability Cloud でログとトレースを関連付けることができます。

ただし、Helm を使って K8s クラスターに OpenTelemetry collector をデプロイし、
ログ収集オプションを含める場合、OpenTelemetry collector は File Log receiver を使用して
コンテナーログを自動的にキャプチャすることを覚えておいてください。

これにより、アプリケーションの重複ログがキャプチャされることになります。例えば、次のスクリーンショットでは
サービスへの各リクエストに対して 2 つのログエントリーが表示されています：

![Duplicate Log Entries](../images/duplicate_logs.png)

これをどのように回避しますか？

## K8s での重複ログの回避

重複ログをキャプチャしないようにするには、`OTEL_LOGS_EXPORTER`環境変数を`none`に設定して、
Splunk Distribution of OpenTelemetry .NET が OTLP を使用してコレクターにログをエクスポートしないようにできます。
これは、`deployment.yaml`ファイルに`OTEL_LOGS_EXPORTER`環境変数を追加することで実行できます：

```yaml
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

それから次を実行します：

```bash
# update the deployment
kubectl apply -f deployment.yaml
```

`OTEL_LOGS_EXPORTER`環境変数を`none`に設定するのは簡単です。しかし、Trace ID と
Span ID はアプリケーションによって生成された stdout ログに書き込まれないため、
ログとトレースを関連付けることができなくなります。

これを解決するには、
`/home/splunk/workshop/docker-k8s-otel/helloworld/SplunkTelemetryConfigurator.cs`で定義されている例のような、カスタムロガーを定義する必要があります。

次のように`Program.cs`ファイルを更新することで、これをアプリケーションに含めることができます：

```cs
using SplunkTelemetry;
using Microsoft.Extensions.Logging.Console;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

SplunkTelemetryConfigurator.ConfigureLogger(builder.Logging);

var app = builder.Build();

app.MapControllers();

app.Run();
```

その後、カスタムログ設定を含む新しい Docker イメージをビルドします：

```bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld

docker build -t helloworld:1.3 .
```

それから更新されたイメージを Kubernetes にインポートします：

```bash
cd /home/splunk

# Import the image into k3d
sudo k3d image import helloworld:1.3 --cluster $INSTANCE-cluster
```

最後に、`deployment.yaml`ファイルを更新してコンテナーイメージの 1.3 バージョンを使用する必要があります：

```yaml
spec:
  containers:
    - name: helloworld
      image: docker.io/library/helloworld:1.3
```

それから変更を適用します：

```bash
# update the deployment
kubectl apply -f deployment.yaml
```

これで重複したログエントリーが排除されたことがわかります。そして
残りのログエントリーは JSON としてフォーマットされ、span と trace ID が含まれています：

![JSON Format Logs](../images/logs_json_format.png)
