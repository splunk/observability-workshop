---
title: OpenTelemetry で .NET アプリケーションを計装する
linkTitle: 4. OpenTelemetry で .NET アプリケーションを計装する
weight: 4
time: 20 minutes
---

## Splunk Distribution of OpenTelemetry のダウンロード

このワークショップでは、NuGet パッケージを使用する代わりに、Splunk Distribution of OpenTelemetry を手動でインストールします。

まず、.NET アプリケーションの計装に使用する最新の `splunk-otel-dotnet-install.sh` ファイルをダウンロードします:

``` bash
cd ~/workshop/docker-k8s-otel/helloworld

curl -sSfL https://github.com/signalfx/splunk-otel-dotnet/releases/latest/download/splunk-otel-dotnet-install.sh -O
```

インストールプロセスの詳細については、[Install the Splunk Distribution of OpenTelemetry .NET manually](https://docs.splunk.com/observability/en/gdi/get-data-in/application/otel-dotnet/instrumentation/instrument-dotnet-application.html#install-the-splunk-distribution-of-opentelemetry-net-manually) を参照してください。

## ディストリビューションのインストール

ターミナルで、以下のようにディストリビューションをインストールします:

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
sh ./splunk-otel-dotnet-install.sh
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Downloading v1.8.0 for linux-glibc (/tmp/tmp.m3tSdtbmge/splunk-opentelemetry-dotnet-linux-glibc-x64.zip)...
```

{{% /tab %}}
{{< /tabs >}}

> 注意: 上記のコマンドを実行する際に、ARCHITECTURE 環境変数を指定する必要がある場合があります:
>
> ``` bash
> ARCHITECTURE=x64 sh ./splunk-otel-dotnet-install.sh
> ```

## 計装の有効化

次に、OpenTelemetry の計装を有効化します:

``` bash
. $HOME/.splunk-otel-dotnet/instrument.sh
```

## デプロイメント環境の設定

Splunk Observability Cloud 内でデータが専用の環境に流れるように、デプロイメント環境を設定しましょう:

``` bash
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=otel-$INSTANCE
```

## 計装付きでアプリケーションを実行する

以下のようにアプリケーションを実行できます:

```
dotnet run
```

## チャレンジ

Linux インスタンスから .NET アプリケーションがエクスポートしているトレースを確認するにはどうすればよいでしょうか？

{{< details summary="ここをクリックして回答を表示" >}}
2つの方法があります:

1. `dotnet run` コマンドの先頭に `OTEL_TRACES_EXPORTER=otlp,console` を追加することで、トレースが OTLP 経由で Collector に送信されると同時にコンソールにも出力されるようになります。

``` bash
OTEL_TRACES_EXPORTER=otlp,console dotnet run 
```

1. または、Collector の設定に debug エクスポーターを追加し、トレースパイプラインに追加することで、トレースが Collector のログに書き込まれるようになります。

``` yaml
exporters:
  debug:
    verbosity: detailed
service:
  pipelines:
    traces:
      receivers: [jaeger, otlp, zipkin]
      processors:
      - memory_limiter
      - batch
      - resourcedetection
      exporters: [otlphttp, signalfx, debug]
```

{{< /details >}}

## アプリケーションへのアクセス

アプリケーションが実行されたら、2つ目の SSH ターミナルを使用して curl でアクセスします:

``` bash
curl http://localhost:8080/hello
```

前回と同様に、`Hello, World!` が返されるはずです。

トレースログを有効にした場合、以下のようなトレースがコンソールまたは Collector のログに出力されるはずです:

````
info: Program[0]
      /hello endpoint invoked anonymously
Activity.TraceId:            c7bbf57314e4856447508cd8addd49b0
Activity.SpanId:             1c92ac653c3ece27
Activity.TraceFlags:         Recorded
Activity.ActivitySourceName: Microsoft.AspNetCore
Activity.DisplayName:        GET /hello/{name?}
Activity.Kind:               Server
Activity.StartTime:          2024-12-20T00:45:25.6551267Z
Activity.Duration:           00:00:00.0006464
Activity.Tags:
    server.address: localhost
    server.port: 8080
    http.request.method: GET
    url.scheme: http
    url.path: /hello
    network.protocol.version: 1.1
    user_agent.original: curl/7.81.0
    http.route: /hello/{name?}
    http.response.status_code: 200
Resource associated with Activity:
    splunk.distro.version: 1.8.0
    telemetry.distro.name: splunk-otel-dotnet
    telemetry.distro.version: 1.8.0
    service.name: helloworld
    os.type: linux
    os.description: Ubuntu 22.04.5 LTS
    os.build_id: 6.8.0-1021-aws
    os.name: Ubuntu
    os.version: 22.04
    host.name: derek-1
    host.id: 20cf15fcc7054b468647b73b8f87c556
    process.owner: splunk
    process.pid: 16997
    process.runtime.description: .NET 8.0.11
    process.runtime.name: .NET
    process.runtime.version: 8.0.11
    container.id: 2
    telemetry.sdk.name: opentelemetry
    telemetry.sdk.language: dotnet
    telemetry.sdk.version: 1.9.0
    deployment.environment: otel-derek-1
````

## Splunk Observability Cloud でアプリケーションを確認する

セットアップが完了したので、トレースが **Splunk Observability Cloud** に送信されていることを確認しましょう。アプリケーションを初めてデプロイした場合、データが表示されるまで数分かかることがあります。

APM に移動し、Environment ドロップダウンを使用して自分の環境（例: `otel-instancename`）を選択します。

すべてが正しくデプロイされていれば、サービス一覧に `helloworld` が表示されるはずです:

![APM Overview](../images/apm_overview.png)

右側の **Service Map** をクリックして、サービスマップを表示します。

![Service Map](../images/service_map.png)

次に、右側の **Traces** をクリックして、このアプリケーションでキャプチャされたトレースを確認します。

![Traces](../images/traces.png)

個々のトレースは以下のように表示されます:

![Traces](../images/trace.png)

> 次のステップに進む前に、Ctrl + C を押して Helloworld アプリを終了してください。
