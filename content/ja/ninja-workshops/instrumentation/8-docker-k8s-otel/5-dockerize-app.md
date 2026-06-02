---
title: アプリケーションのDocker化
linkTitle: 5. アプリケーションのDocker化
weight: 5
time: 15 minutes
---

このワークショップの後半では、.NETアプリケーションをKubernetesクラスターにデプロイします。

しかし、どのようにそれを実現するのでしょうか。

最初のステップは、アプリケーションのDockerイメージを作成することです。これは「dockerizing（Docker化）」と呼ばれ、`Dockerfile`の作成から始まります。

その前に、いくつかの重要な用語を定義しましょう。

## 重要な用語

### Dockerとは

_「Dockerは、コンテナと呼ばれる緩やかに分離された環境でアプリケーションをパッケージ化して実行する機能を提供します。この分離とセキュリティにより、特定のホスト上で多数のコンテナを同時に実行できます。コンテナは軽量で、アプリケーションの実行に必要なすべてが含まれているため、ホストにインストールされているものに依存する必要はありません。」_

出典: <https://docs.docker.com/get-started/docker-overview/>

### コンテナとは

_「コンテナは、アプリケーションの各コンポーネントに対して分離されたプロセスです。各コンポーネントは...独自の分離された環境で実行され、マシン上の他のすべてのものから完全に分離されています。」_

出典: <https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/>

### コンテナイメージとは

_「コンテナイメージは、コンテナを実行するためのすべてのファイル、バイナリ、ライブラリ、構成を含む標準化されたパッケージです。」_

### Dockerfile

_「Dockerfileは、コンテナイメージを作成するために使用されるテキストベースのドキュメントです。実行するコマンド、コピーするファイル、起動コマンドなどに関する指示をイメージビルダーに提供します。」_

## Dockerfileの作成

`/home/splunk/workshop/docker-k8s-otel/helloworld`ディレクトリに`Dockerfile`という名前のファイルを作成しましょう。

``` bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld
```

ファイルの作成にはviまたはnanoを使用できます。ここではviを使った例を示します。

``` bash
vi Dockerfile
```

新しく開いたファイルに以下の内容をコピー＆ペーストします。

> 以下のテキストを貼り付ける前に、viで`i`キーを押して挿入モードに入ってください。

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

> viで変更を保存するには、`esc`キーを押してコマンドモードに入り、`:wq!`と入力してから`enter/return`キーを押します。

これらは何を意味するのでしょうか。順番に見ていきましょう。

## Dockerfileの解説

この例ではマルチステージのDockerfileを使用しており、Dockerイメージの作成プロセスを以下のステージに分割しています。

* Base
* Build
* Publish
* Final

マルチステージアプローチは複雑ですが、デプロイ用のより軽量なランタイムイメージを作成できます。以下では各ステージの目的について説明します。

### Baseステージ

baseステージでは、アプリを実行するユーザー、作業ディレクトリを定義し、アプリへのアクセスに使用するポートを公開します。Microsoftの`mcr.microsoft.com/dotnet/aspnet:8.0`イメージをベースにしています。

``` dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER app
WORKDIR /app
EXPOSE 8080
```

`mcr.microsoft.com/dotnet/aspnet:8.0`イメージにはSDKではなく.NETランタイムのみが含まれているため、比較的軽量です。Debian 12 Linuxディストリビューションをベースにしています。ASP.NET Core RuntimeのDockerイメージに関する詳細は、[GitHub](https://github.com/dotnet/dotnet-docker/blob/main/README.aspnet.md)で確認できます。

### Buildステージ

Dockerfileの次のステージはbuildステージです。このステージでは`mcr.microsoft.com/dotnet/sdk:8.0`イメージを使用します。これもDebian 12をベースにしていますが、ランタイムだけでなく完全な[.NET SDK](https://github.com/dotnet/dotnet-docker/blob/main/README.sdk.md)を含んでいます。

このステージでは、`.csproj`ファイルをbuildイメージにコピーし、`dotnet restore`を使用してアプリケーションが使用する依存関係をダウンロードします。

その後、アプリケーションコードをbuildイメージにコピーし、`dotnet build`を使用してプロジェクトとその依存関係を一連の`.dll`バイナリにビルドします。

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

3番目のステージはpublishで、Microsoftのイメージではなくbuildステージのイメージをベースにしています。このステージでは、`dotnet publish`を使用してアプリケーションとその依存関係をデプロイ用にパッケージ化します。

``` dockerfile
FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false
```

### Finalステージ

4番目のステージはfinalステージで、baseステージのイメージ（buildやpublishステージよりも軽量）をベースにしています。publishステージのイメージから出力をコピーし、アプリケーションのエントリーポイントを定義します。

``` dockerfile
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

ENTRYPOINT ["dotnet", "helloworld.dll"]
```

## Dockerイメージのビルド

`Dockerfile`が用意できたので、これを使ってアプリケーションを含むDockerイメージをビルドできます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker build -t helloworld:1.0 .
```

{{% /tab %}}
{{% tab title="Example Output" %}}

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

これは、現在のディレクトリにある`Dockerfile`を使用して、`helloworld:1.0`というタグでイメージをビルドするようDockerに指示しています。

以下のコマンドで、イメージが正常に作成されたことを確認できます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker images
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
helloworld   1.0       db19077b9445   20 seconds ago   217MB
```

{{% /tab %}}
{{< /tabs >}}

## Dockerイメージのテスト

> 続行する前に、以前に起動したアプリケーションがインスタンス上で実行されていないことを確認してください。

Dockerイメージを使用してアプリケーションを以下のように実行できます。

``` bash
docker run --name helloworld \
--detach \
--expose 8080 \
--network=host \
helloworld:1.0
```

> 注: `--network=host`パラメーターを含めているのは、Dockerコンテナがインスタンス上のリソースにアクセスできるようにするためです。これは後ほど、アプリケーションがlocalhostで実行されているcollectorにデータを送信する必要がある際に重要になります。

Dockerコンテナが実行されていることを確認しましょう。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker ps | grep helloworld
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
$ docker ps | grep helloworld
CONTAINER ID   IMAGE            COMMAND                  CREATED       STATUS       PORTS     NAMES
5f5b9cd56ac5   helloworld:1.0   "dotnet helloworld.d…"   2 mins ago    Up 2 mins              helloworld
```

{{% /tab %}}
{{< /tabs >}}

以前と同様にアプリケーションにアクセスできます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl http://localhost:8080/hello/Docker
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Hello, Docker! 
```

{{% /tab %}}
{{< /tabs >}}

おめでとうございます。ここまで進めた方は、.NETアプリケーションのDocker化に成功しました。
