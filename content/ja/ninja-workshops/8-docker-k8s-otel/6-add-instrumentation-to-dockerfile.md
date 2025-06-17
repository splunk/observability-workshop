---
title: Dockerfileに計装を追加する
linkTitle: 6. Dockerfileに計装を追加する
weight: 6
time: 10 minutes
---

アプリケーションを正常に Docker 化したので、次に OpenTelemetry による計装 を追加しましょう。

これは、Linux で実行しているアプリケーションを計装した際の手順と似ていますが、
注意すべきいくつかの重要な違いがあります。

## Dockerfile の更新

`/home/splunk/workshop/docker-k8s-otel/helloworld`ディレクトリの`Dockerfile`を更新しましょう。

Dockerfile で.NET アプリケーションがビルドされた後、以下の操作を行いたいと思います：

- `splunk-otel-dotnet-install.sh`をダウンロードして実行するために必要な依存関係を追加する
- Splunk OTel .NET インストーラーをダウンロードする
- ディストリビューションをインストールする

Dockerfile のビルドステージに以下を追加できます。vi で Dockerfile を開きましょう：

```bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile
```

> vi では「i」キーを押して編集モードに入ります
> 'NEW CODE'とマークされている行を Dockerfile のビルドステージセクションに貼り付けてください：

```dockerfile
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

次に、以下の変更で Dockerfile の最終ステージを更新します：

- ビルドイメージから最終イメージに/root/.splunk-otel-dotnet/をコピーする
- entrypoint.sh ファイルもコピーする
- `OTEL_SERVICE_NAME`と`OTEL_RESOURCE_ATTRIBUTES`環境変数を設定する
- `ENTRYPOINT`を`entrypoint.sh`に設定する

最も簡単な方法は、最終ステージ全体を以下の内容で置き換えることです：

> **重要** Dockerfile の`$INSTANCE`をあなたのインスタンス名に置き換えてください。
> インスタンス名は`echo $INSTANCE`を実行することで確認できます。

```dockerfile
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

> vi での変更を保存するには、`esc`キーを押してコマンドモードに入り、`:wq!`と入力してから`enter/return`キーを押します。

これらすべての変更の後、Dockerfile は以下のようになるはずです：

> **重要** このコンテンツを自分の Dockerfile にコピー＆ペーストする場合は、
> Dockerfile の`$INSTANCE`をあなたのインスタンス名に置き換えてください。
> インスタンス名は`echo $INSTANCE`を実行することで確認できます。

```dockerfile
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

また、`/home/splunk/workshop/docker-k8s-otel/helloworld`フォルダに`entrypoint.sh`という名前のファイルを
以下の内容で作成する必要があります：

```bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/entrypoint.sh
```

次に、新しく作成したファイルに以下のコードを貼り付けます：

```bash
#!/bin/sh
# Read in the file of environment settings
. /$HOME/.splunk-otel-dotnet/instrument.sh

# Then run the CMD
exec "$@"
```

> vi での変更を保存するには、`esc`キーを押してコマンドモードに入り、`:wq!`と入力してから`enter/return`キーを押します。

`entrypoint.sh`スクリプトは、計装に含まれる instrument.sh スクリプトが環境変数を**コンテナ起動時に**取得するために必要です。これにより、各プラットフォームに対して環境変数が正しく設定されることが保証されます。

> 「なぜ Linux ホスト上で OpenTelemetry .NET instrumentation を有効化したときのように、
> Dockerfile に以下のコマンドを含めるだけではだめなのか？」と疑問に思うかもしれません。
>
> ```dockerfile
> RUN . $HOME/.splunk-otel-dotnet/instrument.sh
> ```
>
> この方法の問題点は、各 Dockerfile RUN ステップが新しいコンテナと新しいシェルで実行されることです。
> あるシェルで環境変数を設定しようとしても、後で見ることはできません。
> この問題は、ここで行ったようにエントリポイントスクリプトを使用することで解決されます。
> この問題についての詳細は、こちらの[Stack Overflow の投稿](https://stackoverflow.com/questions/55921914/how-to-source-a-script-with-environment-variables-in-a-docker-build-process)を参照してください。

## Docker イメージのビルド

OpenTelemetry .NET instrumentation を含む新しい Docker イメージをビルドしましょう：

```bash
docker build -t helloworld:1.1 .
```

> 注：以前のバージョンと区別するために、異なるバージョン（1.1）を使用しています。
> 古いバージョンをクリーンアップするには、以下のコマンドでコンテナ ID を取得します：
>
> ```bash
> docker ps -a
> ```
>
> 次に、以下のコマンドでコンテナを削除します：
>
> ```bash
> docker rm <old container id> --force
> ```
>
> 次にコンテナイメージ ID を取得します：
>
> ```bash
> docker images | grep 1.0
> ```
>
> 最後に、以下のコマンドで古いイメージを削除できます：
>
> ```bash
> docker image rm <old image id>
> ```

## アプリケーションの実行

新しい Docker イメージを実行しましょう：

```bash
docker run --name helloworld \
--detach \
--expose 8080 \
--network=host \
helloworld:1.1
```

以下を使用してアプリケーションにアクセスできます：

```bash
curl http://localhost:8080/hello
```

トラフィックを生成するために上記のコマンドを数回実行しましょう。

1 分ほど経過したら、Splunk Observability Cloud に新しいトレースが表示されることを確認します。

> あなたの特定の環境でトレースを探すことを忘れないでください。

## トラブルシューティング

Splunk Observability Cloud にトレースが表示されない場合は、以下のようにトラブルシューティングを行うことができます。

まず、コレクター設定ファイルを編集用に開きます：

```bash
sudo vi /etc/otel/collector/agent_config.yaml
```

次に、トレースパイプラインにデバッグエクスポーターを追加します。これにより、トレースがコレクターログに書き込まれるようになります：

```yaml
service:
  extensions: [health_check, http_forwarder, zpages, smartagent]
  pipelines:
    traces:
      receivers: [jaeger, otlp, zipkin]
      processors:
        - memory_limiter
        - batch
        - resourcedetection
      #- resource/add_environment
      # NEW CODE: デバッグエクスポーターをここに追加
      exporters: [otlphttp, signalfx, debug]
```

その後、コレクターを再起動して設定変更を適用します：

```bash
sudo systemctl restart splunk-otel-collector
```

`journalctl`を使用してコレクターログを表示できます：

> ログの追跡を終了するには、Ctrl + C を押します。

```bash
sudo journalctl -u splunk-otel-collector -f -n 100
```
