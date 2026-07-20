---
title: アプリケーションのDocker化
linkTitle: 5. アプリケーションのDocker化
weight: 5
time: 15 minutes
---

このワークショップの後半では、.NETアプリケーションをKubernetesクラスターにデプロイします。

では、どのようにすればよいのでしょうか？

最初のステップは、アプリケーションのDockerイメージを作成することです。これはアプリケーションの「Docker化」と呼ばれ、`Dockerfile` の作成から始まります。

まず、いくつかの重要な用語を定義しましょう。

## 重要な用語

### Dockerとは？

_「Dockerは、コンテナと呼ばれる緩やかに分離された環境でアプリケーションをパッケージ化して実行する機能を提供します。分離とセキュリティにより、特定のホスト上で多数のコンテナを同時に実行できます。コンテナは軽量で、アプリケーションの実行に必要なすべてを含んでいるため、ホストにインストールされているものに依存する必要がありません。」_

出典:  <https://docs.docker.com/get-started/docker-overview/>

### コンテナとは？

_「コンテナは、アプリケーションの各コンポーネントの分離されたプロセスです。各コンポーネントは独自の分離された環境で実行され、マシン上の他のすべてから完全に分離されています。」_

出典:  <https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/>

### コンテナイメージとは？

_「コンテナイメージは、コンテナを実行するために必要なすべてのファイル、バイナリ、ライブラリ、および設定を含む標準化されたパッケージです。」_

### Dockerfile

_「Dockerfileは、コンテナイメージを作成するために使用されるテキストベースのドキュメントです。実行するコマンド、コピーするファイル、起動コマンドなどについて、イメージビルダーに指示を提供します。」_

## Dockerfileの作成

`/home/splunk/workshop/docker-k8s-otel/helloworld` ディレクトリに `Dockerfile` という名前のファイルを作成しましょう。

``` bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld
```

viまたはnanoを使用してファイルを作成できます。ここではviを使用した例を示します。

``` bash
vi Dockerfile
```

新しく開いたファイルに以下の内容をコピーして貼り付けます。

> 以下のテキストを貼り付ける前に、viで「i」を押してインサートモードに入ります。

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

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

ENTRYPOINT ["dotnet", "helloworld.dll"]
```

> viで変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

これはどういう意味でしょうか？詳しく見ていきましょう。

## Dockerfileの解説

この例ではマルチステージDockerfileを使用しており、Dockerイメージの作成プロセスを以下のステージに分けています。

* Base
* Build
* Publish
* Final

マルチステージのアプローチはより複雑ですが、デプロイ用の軽量なランタイムイメージを作成できます。以下で各ステージの目的を説明します。

### Baseステージ

Baseステージでは、アプリケーションを実行するユーザー、作業ディレクトリを定義し、アプリケーションへのアクセスに使用されるポートを公開します。Microsoftの `mcr.microsoft.com/dotnet/aspnet:8.0` イメージをベースにしています。

``` dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER app
WORKDIR /app
EXPOSE 8080
```

`mcr.microsoft.com/dotnet/aspnet:8.0` イメージにはSDKではなく.NETランタイムのみが含まれているため、比較的軽量です。Debian 12 Linuxディストリビューションをベースにしています。ASP.NET Core Runtime Dockerイメージの詳細については [GitHub](https://github.com/dotnet/dotnet-docker/blob/main/README.aspnet.md) を参照してください。

### Buildステージ

Dockerfileの次のステージはBuildステージです。このステージでは `mcr.microsoft.com/dotnet/sdk:8.0` イメージを使用します。このイメージもDebian 12をベースにしていますが、ランタイムだけでなく完全な [.NET SDK](https://github.com/dotnet/dotnet-docker/blob/main/README.sdk.md) が含まれています。

このステージでは `.csproj` ファイルをビルドイメージにコピーし、`dotnet restore` を使用してアプリケーションが使用する依存関係をダウンロードします。

次に、アプリケーションコードをビルドイメージにコピーし、`dotnet build` を使用してプロジェクトとその依存関係を `.dll` バイナリのセットにビルドします。

``` dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["helloworld.csproj", "helloworld/"]
RUN dotnet restore "./helloworld/./helloworld.csproj"
WORKDIR "/src/helloworld"
COPY . .
RUN dotnet build "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/build
```

### Publishステージ

3番目のステージはPublishです。MicrosoftイメージではなくBuildステージのイメージをベースにしています。このステージでは `dotnet publish` を使用して、アプリケーションとその依存関係をデプロイ用にパッケージ化します。

``` dockerfile
FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false
```

### Finalステージ

4番目のステージは最終ステージで、Baseステージのイメージをベースにしています（BuildおよびPublishステージよりも軽量です）。Publishステージのイメージからの出力をコピーし、アプリケーションのエントリポイントを定義します。

``` dockerfile
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

ENTRYPOINT ["dotnet", "helloworld.dll"]
```

## Dockerイメージのビルド

`Dockerfile` ができたので、これを使用してアプリケーションを含むDockerイメージをビルドできます。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
docker build -t helloworld:1.0 .
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Sending build context to Docker daemon  281.1kB
Step 1/19 : FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
8.0: Pulling from dotnet/aspnet
af302e5c37e9: Pull complete 
91ab5e0aabf0: Pull complete 
1c1e4530721e: Pull complete 
1f39ca6dcc3a: Pull complete 
ea20083aa801: Pull complete 
64c242a4f561: Pull complete 
Digest: sha256:587c1dd115e4d6707ff656d30ace5da9f49cec48e627a40bbe5d5b249adc3549
Status: Downloaded newer image for mcr.microsoft.com/dotnet/aspnet:8.0
 ---> 0ee5d7ddbc3b
Step 2/19 : USER app
etc,
```

{{% /tab %}}
{{< /tabs >}}

これはDockerに対して、カレントディレクトリの `Dockerfile` を使用して `helloworld:1.0` というタグのイメージをビルドするよう指示しています。

以下のコマンドで正常に作成されたことを確認できます。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
docker images
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
helloworld   1.0       db19077b9445   20 seconds ago   217MB
```

{{% /tab %}}
{{< /tabs >}}

## Dockerイメージのテスト

> 続行する前に、先ほど起動したアプリケーションがインスタンス上で実行されていないことを確認してください。

Dockerイメージを使用して以下のようにアプリケーションを実行できます。

``` bash
docker run --name helloworld \
--detach \
--expose 8080 \
--network=host \
helloworld:1.0
```

> 注意: Dockerコンテナがインスタンス上のリソースにアクセスできるように `--network=host` パラメータを含めています。これは後でアプリケーションがlocalhostで実行されているCollectorにデータを送信する必要がある場合に重要です。

Dockerコンテナが実行されていることを確認しましょう。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
docker ps | grep helloworld
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
$ docker ps | grep helloworld
CONTAINER ID   IMAGE            COMMAND                  CREATED       STATUS       PORTS     NAMES
5f5b9cd56ac5   helloworld:1.0   "dotnet helloworld.d…"   2 mins ago    Up 2 mins              helloworld
```

{{% /tab %}}
{{< /tabs >}}

以前と同様にアプリケーションにアクセスできます。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
curl http://localhost:8080/hello/Docker
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
Hello, Docker! 
```

{{% /tab %}}
{{< /tabs >}}

ここまで完了できていれば、.NETアプリケーションのDocker化に成功しています。
