---
title: アプリケーションのDocker化
linkTitle: 5. アプリケーションのDocker化
weight: 5
time: 15 minutes
---

このワークショップの後半では、.NET アプリケーションを Kubernetes クラスターにデプロイします。

しかし、どのようにそれを行うのでしょうか？

最初のステップは、アプリケーション用の Docker イメージを作成することです。これは
アプリケーションの「Docker 化」として知られており、プロセスは`Dockerfile`の作成から始まります。

しかし、まず重要な用語を定義しましょう。

## 重要な用語

### Docker とは何ですか？

> 「Docker は、コンテナと呼ばれる緩い分離環境でアプリケーションをパッケージ化して実行する機能を提供します。分離とセキュリティにより、指定されたホスト上で同時に多くのコンテナを実行できます。コンテナは軽量で、アプリケーションの実行に必要なすべてを含んでいるため、ホストにインストールされているものに依存する必要がありません。」

ソース: <https://docs.docker.com/get-started/docker-overview/>

### コンテナとは何ですか？

> 「コンテナは、アプリのコンポーネントごとの分離されたプロセスです。各コンポーネントは...独自の分離された環境で実行され、マシン上の他のすべてのものから完全に分離されています。」

ソース: <https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/>

### コンテナイメージとは何ですか？

> 「コンテナイメージは、コンテナを実行するためのすべてのファイル、バイナリ、ライブラリ、および設定を含む標準化されたパッケージです。」

### Dockerfile

> 「Dockerfile は、コンテナイメージを作成するために使用されるテキストベースのドキュメントです。実行するコマンド、コピーするファイル、起動コマンドなどに関するイメージビルダーへの指示を提供します。」

## Dockerfile の作成

`/home/splunk/workshop/docker-k8s-otel/helloworld`ディレクトリに`Dockerfile`という名前のファイルを作成しましょう。

```bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld
```

ファイルの作成には vi または nano を使用できます。vi を使用した例を示します：

```bash
vi Dockerfile
```

新しく開いたファイルに以下の内容をコピー＆ペーストします：

> 以下のテキストを貼り付ける前に、vi で「i」を押して挿入モードに入ってください。

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

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

ENTRYPOINT ["dotnet", "helloworld.dll"]
```

> vi での変更を保存するには、`esc`キーを押してコマンドモードに入り、`:wq!`と入力してから`enter/return`キーを押します。

これはすべて何を意味するのでしょうか？詳しく見てみましょう。

## Dockerfile の詳細解説

この例では、マルチステージ Dockerfile を使用しており、Docker イメージ作成プロセスを以下のステージに分けています：

- Base（ベース）
- Build（ビルド）
- Publish（パブリッシュ）
- Final（最終）

マルチステージアプローチはより複雑ですが、デプロイメント用により
軽量なランタイムイメージを作成することができます。以下では、
これらの各ステージの目的を説明します。

### ベースステージ

ベースステージでは、アプリを実行するユーザー、作業ディレクトリを定義し、
アプリにアクセスするために使用されるポートを公開します。
これは Microsoft の`mcr.microsoft.com/dotnet/aspnet:8.0`イメージをベースにしています：

```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER app
WORKDIR /app
EXPOSE 8080
```

なお、`mcr.microsoft.com/dotnet/aspnet:8.0`イメージには.NET runtime のみが含まれており、
SDK は含まれていないため、比較的軽量です。これは Debian 12 Linux
distribution がベースになっています。ASP.NET Core Runtime Docker イメージの詳細については
[GitHub](https://github.com/dotnet/dotnet-docker/blob/main/README.aspnet.md)で確認できます。

### Build ステージ

Dockerfile の次のステージは build ステージです。このステージでは、
`mcr.microsoft.com/dotnet/sdk:8.0`イメージが使用されます。これも Debian 12 がベースになっていますが、
runtime だけでなく完全な[.NET SDK](https://github.com/dotnet/dotnet-docker/blob/main/README.sdk.md)が含まれています。

このステージでは`.csproj`ファイルを build イメージにコピーし、その後`dotnet restore`を使用して
アプリケーションが使用する依存関係をダウンロードします。

次に、アプリケーションコードを build イメージにコピーし、
`dotnet build`を使用してプロジェクトとその依存関係を
`.dll`バイナリのセットにビルドします：

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["helloworld.csproj", "helloworld/"]
RUN dotnet restore "./helloworld/./helloworld.csproj"
WORKDIR "/src/helloworld"
COPY . .
RUN dotnet build "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/build
```

### Publish ステージ

3 番目のステージは publish で、これは Microsoft イメージではなく build ステージイメージをベースにしています。このステージでは、`dotnet publish`を使用して
アプリケーションとその依存関係を deployment 用にパッケージ化します：

```dockerfile
FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./helloworld.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false
```

### Final ステージ

4 番目のステージは最終ステージで、これは base
ステージイメージをベースにしています（build と publish ステージよりも軽量）。publish ステージイメージからの出力をコピーし、
アプリケーションの entry point を定義します：

```dockerfile
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .

ENTRYPOINT ["dotnet", "helloworld.dll"]
```

## Docker イメージのビルド

`Dockerfile`ができたので、これを使用してアプリケーションを含む Docker イメージを
ビルドできます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker build -t helloworld:1.0 .
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
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

これは、現在のディレクトリの`Dockerfile`を使用して`helloworld:1.0`のタグでイメージをビルドするよう Docker に指示します。

以下のコマンドで正常に作成されたことを確認できます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker images
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
helloworld   1.0       db19077b9445   20 seconds ago   217MB
```

{{% /tab %}}
{{< /tabs >}}

## Docker イメージのテスト

> 続行する前に、以前に開始したアプリケーションがインスタンス上で実行されていないことを確認してください。

Docker イメージを使用して以下のようにアプリケーションを実行できます：

```bash
docker run --name helloworld \
--detach \
--expose 8080 \
--network=host \
helloworld:1.0
```

> 注意：`--network=host`パラメータを含めて、Docker コンテナが
> インスタンス上のリソースにアクセスできるようにしています。これは後でアプリケーションが
> localhost 上で実行されているコレクターにデータを送信する必要がある場合に重要です。

Docker コンテナが実行されていることを確認しましょう：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
docker ps
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
$ docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED       STATUS       PORTS     NAMES
5f5b9cd56ac5   helloworld:1.0   "dotnet helloworld.d…"   2 mins ago    Up 2 mins              helloworld
```

{{% /tab %}}
{{< /tabs >}}

以前と同様にアプリケーションにアクセスできます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl http://localhost:8080/hello/Docker
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
Hello, Docker!
```

{{% /tab %}}
{{< /tabs >}}

おめでとうございます。ここまで到達したということは、.NET アプリケーションの Docker 化に成功したということです。
