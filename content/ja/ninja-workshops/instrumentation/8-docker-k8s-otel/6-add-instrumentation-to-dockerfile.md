---
title: Dockerfile に計装を追加する
linkTitle: 6. Dockerfile に計装を追加する
weight: 6
time: 10 minutes
---

アプリケーションの Docker 化が成功したので、次に OpenTelemetry の計装を追加しましょう。

これは Linux 上で実行されているアプリケーションを計装したときの手順と似ていますが、いくつかの重要な違いがあります。

## Dockerfile の更新

`/home/splunk/workshop/docker-k8s-otel/helloworld` ディレクトリにある `Dockerfile` を更新しましょう。

Dockerfile で .NET アプリケーションがビルドされた後、以下を行います

* `splunk-otel-dotnet-install.sh` のダウンロードと実行に必要な依存関係を追加する
* Splunk OTel .NET インストーラーをダウンロードする
* ディストリビューションをインストールする

Dockerfile のビルドステージに以下を追加します。vi で Dockerfile を開きましょう

``` bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile
```

> i キーを押して vi の編集モードに入ります

> 'NEW CODE' と記載された行を Dockerfile のビルドステージセクションに貼り付けてください

``` dockerfile
# CODE ALREADY IN YOUR DOCKERFILE:
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["helloworld.csproj", "helloworld/"]
RUN dotnet restore "./helloworld/./helloworld.csproj"
WORKDIR "/src/helloworld"
COPY . .
RUN dotnet build "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/build

# NEW CODE: add dependencies for splunk-otel-dotnet-install.sh
RUN apt-get update && \
 apt-get install -y unzip

# NEW CODE: download Splunk OTel .NET installer
RUN curl -sSfL https://github.com/signalfx/splunk-otel-dotnet/releases/latest/download/splunk-otel-dotnet-install.sh -O

# NEW CODE: install the distribution
RUN sh ./splunk-otel-dotnet-install.sh
```

次に、Dockerfile の最終ステージを以下の変更で更新します

* ビルドイメージから最終イメージに /root/.splunk-otel-dotnet/ をコピーする
* entrypoint.sh ファイルもコピーする
* `OTEL_SERVICE_NAME` と `OTEL_RESOURCE_ATTRIBUTES` 環境変数を設定する
* `ENTRYPOINT` を `entrypoint.sh` に設定する

最終ステージ全体を以下の内容に置き換えるのが最も簡単です

> **重要** Dockerfile 内の `$INSTANCE` をご自身のインスタンス名に置き換えてください。
> インスタンス名は `echo $INSTANCE` を実行して確認できます。

``` dockerfile
# CODE ALREADY IN YOUR DOCKERFILE
FROM base AS final

# NEW CODE: Copy instrumentation file tree
WORKDIR "//home/app/.splunk-otel-dotnet"
COPY --from=build /root/.splunk-otel-dotnet/ .

# CODE ALREADY IN YOUR DOCKERFILE
WORKDIR /app
COPY --from=publish /app/publish .

# NEW CODE: copy the entrypoint.sh script
COPY entrypoint.sh .

# NEW CODE: set OpenTelemetry environment variables
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_RESOURCE_ATTRIBUTES='deployment.environment=otel-$INSTANCE'

# NEW CODE: replace the prior ENTRYPOINT command with the following two lines 
ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["dotnet", "helloworld.dll"]
```

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力して `enter/return` キーを押してください。

すべての変更を適用した後、Dockerfile は以下のようになります

> **重要** この内容をご自身の Dockerfile にコピー＆ペーストする場合は、
> Dockerfile 内の `$INSTANCE` をご自身のインスタンス名に置き換えてください。
> インスタンス名は `echo $INSTANCE` を実行して確認できます。

``` dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER app
WORKDIR /app
EXPOSE 8080

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["helloworld.csproj", "helloworld/"]
RUN dotnet restore "./helloworld/./helloworld.csproj"
WORKDIR "/src/helloworld"
COPY . .
RUN dotnet build "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/build

# NEW CODE: add dependencies for splunk-otel-dotnet-install.sh
RUN apt-get update && \
 apt-get install -y unzip

# NEW CODE: download Splunk OTel .NET installer
RUN curl -sSfL https://github.com/signalfx/splunk-otel-dotnet/releases/latest/download/splunk-otel-dotnet-install.sh -O

# NEW CODE: install the distribution
RUN sh ./splunk-otel-dotnet-install.sh

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final

# NEW CODE: Copy instrumentation file tree
WORKDIR "//home/app/.splunk-otel-dotnet"
COPY --from=build /root/.splunk-otel-dotnet/ .

WORKDIR /app
COPY --from=publish /app/publish .

# NEW CODE: copy the entrypoint.sh script
COPY entrypoint.sh .

# NEW CODE: set OpenTelemetry environment variables
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_RESOURCE_ATTRIBUTES='deployment.environment=otel-$INSTANCE'

# NEW CODE: replace the prior ENTRYPOINT command with the following two lines 
ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["dotnet", "helloworld.dll"]
```

## entrypoint.sh ファイルの作成

`/home/splunk/workshop/docker-k8s-otel/helloworld` フォルダに `entrypoint.sh` という名前のファイルを作成し、以下の内容を記述する必要があります

``` bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/entrypoint.sh
```

新しく作成したファイルに以下のコードを貼り付けてください

``` bash
#!/bin/sh
# Read in the file of environment settings
. /$HOME/.splunk-otel-dotnet/instrument.sh

# Then run the CMD
exec "$@"
```

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力して `enter/return` キーを押してください。

`entrypoint.sh` スクリプトは、計装に含まれる instrument.sh スクリプトから環境変数を読み込むために必要です。これにより、各プラットフォームに対して環境変数が正しく設定されます。

> Linux ホストで OpenTelemetry .NET 計装を有効化したときのように、Dockerfile に以下のコマンドを含めるだけではなぜダメなのか、疑問に思うかもしれません
>
> ``` dockerfile
> RUN . $HOME/.splunk-otel-dotnet/instrument.sh
> ```
>
> この方法の問題は、Dockerfile の各 RUN ステップが新しいコンテナと新しいシェルで実行されることです。
> あるシェルで環境変数を設定しても、その後のステップでは参照できません。
> この問題は、ここで行ったようにエントリーポイントスクリプトを使用することで解決できます。
> この問題の詳細については、こちらの [Stack Overflow の投稿](https://stackoverflow.com/questions/55921914/how-to-source-a-script-with-environment-variables-in-a-docker-build-process)を参照してください。

## Docker イメージのビルド

OpenTelemetry .NET 計装を含む新しい Docker イメージをビルドしましょう

``` bash
docker build -t helloworld:1.1 .
```

> 注意：以前のバージョンと区別するために、異なるバージョン（1.1）を使用しています。
> 古いバージョンをクリーンアップするには、まず以下のコマンドでコンテナ ID を取得します
>
> ``` bash
> docker ps -a | grep helloworld
> ```
>
> 次に以下のコマンドでコンテナを削除します
>
> ``` bash
> docker rm <old container id> --force
> ```
>
> 次にコンテナイメージ ID を取得します
>
> ``` bash
> docker images | grep 1.0
> ```
>
> 最後に、以下のコマンドで古いイメージを削除します
>
> ``` bash
> docker image rm <old image id>
> ```

## アプリケーションの実行

新しい Docker イメージを実行しましょう

``` bash
docker run --name helloworld \
--detach \
--expose 8080 \
--network=host \
helloworld:1.1
```

以下のコマンドでアプリケーションにアクセスできます

``` bash
curl http://localhost:8080/hello
```

上記のコマンドを数回実行してトラフィックを生成してください。

1分ほど経ったら、Splunk Observability Cloud に新しいトレースが表示されていることを確認してください。

> ご自身の Environment でトレースを探すことを忘れないでください。

## トラブルシューティング

Splunk Observability Cloud にトレースが表示されない場合、以下の方法でトラブルシューティングできます。

まず、コレクターの設定ファイルを編集用に開きます

``` bash
sudo vi /etc/otel/collector/agent_config.yaml
```

次に、トレースパイプラインに debug エクスポーターを追加します。これにより、トレースがコレクターのログに書き込まれるようになります

``` yaml
service:
  telemetry:
    logs:
      level: ${env:SPLUNK_COLLECTOR_LOG_LEVEL:-info}
    metrics:
      readers:
        - pull:
            exporter:
              prometheus:
                host: '127.0.0.1'
                port: 8888
  extensions: [headers_setter, health_check, http_forwarder, zpages, smartagent]
  pipelines:
    traces:
      receivers: [jaeger, otlp, zipkin]
      processors:
      - memory_limiter
      - batch
      - resourcedetection
      #- resource/add_environment
      # NEW CODE: add the debug exporter here
      exporters: [otlp_http, signalfx, debug]
```

次に、設定変更を適用するためにコレクターを再起動します

``` bash
sudo systemctl restart splunk-otel-collector
```

`journalctl` を使用してコレクターのログを確認できます

> Ctrl + C を押してログのテーリングを終了します。

``` bash
sudo journalctl -u splunk-otel-collector -f -n 100
```
