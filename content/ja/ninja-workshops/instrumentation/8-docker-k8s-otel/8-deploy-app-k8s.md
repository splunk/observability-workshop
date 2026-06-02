---
title: Deploy Application to K8s
linkTitle: 8. Deploy Application to K8s
weight: 8
time: 15 minutes
---

## Dockerfile を更新する

Kubernetes では、環境変数は Docker イメージに埋め込むのではなく、`.yaml` マニフェストファイルで管理するのが一般的です。そこで、Dockerfile から次の 2 つの環境変数を削除します。

``` bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile
```

削除する 2 つの環境変数は次のとおりです。

``` dockerfile
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_RESOURCE_ATTRIBUTES='deployment.environment=otel-$INSTANCE'
```

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押してください。

## 新しい Docker イメージをビルドする

環境変数を除外した新しい Docker イメージをビルドします。

``` bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld 

docker build -t helloworld:1.2 .
```

> 注：以前のバージョンと区別するために、別のバージョン (1.2) を使用しています。
> 古いバージョンを整理するには、次のコマンドを実行してコンテナ ID を取得します。
>
> ``` bash
> docker ps -a | grep helloworld
> ```
>
> 次に、以下のコマンドを実行してコンテナを削除します。
>
> ``` bash
> docker rm <old container id> --force
> ```
>
> コンテナイメージ ID を取得します。
>
> ``` bash
> docker images | grep 1.1
> ```
>
> 最後に、以下のコマンドを実行して古いイメージを削除します。
>
> ``` bash
> docker image rm <old image id>
> ```

## Docker イメージをローカルコンテナリポジトリにインポートする

通常は Docker Hub のようなリポジトリに Docker イメージをプッシュします。
ですが、このワークショップでは、EC2 インスタンス上の `localhost:9999` で動作しているローカルコンテナリポジトリに Docker イメージをプッシュします。

``` bash
# Update the image tag
docker tag helloworld:1.2 localhost:9999/helloworld:1.2

# Import the image into the local repository
docker push localhost:9999/helloworld:1.2
```

## .NET アプリケーションをデプロイする

> ヒント：vi で編集モードに入るには、`i` キーを押します。変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

.NET アプリケーションを K8s にデプロイするために、`/home/splunk` に `deployment.yaml` という名前のファイルを作成します。

``` bash
vi /home/splunk/deployment.yaml
```

以下の内容を貼り付けます。

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: helloworld
spec:
  selector:
    matchLabels:
      app: helloworld
  replicas: 1
  template:
    metadata:
      labels:
        app: helloworld
    spec:
      containers:
        - name: helloworld
          image: localhost:9999/helloworld:1.2
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
          env:
            - name: PORT
              value: "8080"
```

> [!tip]- Kubernetes における Deployment とは何か？
> deployment.yaml ファイルは、デプロイメントリソースを定義するために使用される Kubernetes の設定ファイルです。このファイルは Kubernetes でアプリケーションを管理するための基盤です。デプロイメントの設定では、デプロイメントの ***望ましい状態 (desired state)*** を定義し、Kubernetes は ***実際の (actual)*** 状態がそれと一致するように維持します。これにより、アプリケーション Pod がセルフヒーリングできるようになるほか、アプリケーションのアップデートやロールバックも容易になります。

次に、同じディレクトリに `service.yaml` という名前のファイルを作成します。

``` bash
vi /home/splunk/service.yaml
```

以下の内容を貼り付けます。

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: helloworld
  labels:
    app: helloworld
spec:
  type: ClusterIP
  selector:
    app: helloworld
  ports:
    - port: 8080
      protocol: TCP
```

> [!tip]- Kubernetes における Service とは何か？
> Kubernetes における Service は抽象化レイヤーで、仲介役のように機能します。Pod にアクセスするための固定 IP アドレスや DNS 名を提供し、Pod の追加・削除・置換が行われても変わりません。

次に、同じディレクトリに `ingress.yaml` という名前のファイルを作成します。

``` bash
vi /home/splunk/ingress.yaml
```

以下の内容を貼り付けます。

``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: helloworld-ingress
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
spec:
  ingressClassName: traefik
  rules:
    - host: helloworld.localhost
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: helloworld
                port:
                  number: 8080
```

> [!tip]- Kubernetes における Ingress とは何か？
> Kubernetes における Ingress は、クラスタ内のサービスへの外部アクセス（通常は HTTP および HTTPS トラフィック）を管理する Kubernetes API オブジェクトです。受信した接続を適切な内部サービスや Pod にルーティングするためのルールセットとして機能し、ロードバランシング、SSL/TLS 終端、名前ベースの仮想ホスティングなどの機能を提供します。

これらのマニフェストファイルを使ってアプリケーションをデプロイできます。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
cd /home/splunk

# create the deployment
kubectl apply -f deployment.yaml

# create the service
kubectl apply -f service.yaml

# create the ingress
kubectl apply -f ingress.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
deployment.apps/helloworld created
service/helloworld created
ingress.networking.k8s.io/helloworld-ingress created
```

{{% /tab %}}
{{< /tabs >}}

## アプリケーションをテストする

次のコマンドを使用してアプリケーションにアクセスします。

``` bash
curl http://helloworld.localhost/hello/Kubernetes
```

## OpenTelemetry を構成する

.NET の OpenTelemetry インストルメンテーションは、すでに Docker イメージに組み込まれています。ですが、データの送信先を伝えるために、いくつかの環境変数を設定する必要があります。

先ほど作成した `deployment.yaml` ファイルに以下を追加します。

> **重要** 以下の YAML 内の `$INSTANCE` を、ご自分のインスタンス名に置き換えてください。インスタンス名は `echo $INSTANCE` を実行して確認できます。

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
```

完成した `deployment.yaml` ファイルは次のようになります（`$INSTANCE` の代わりに **ご自分の** インスタンス名を入れてください）。

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: helloworld
spec:
  selector:
    matchLabels:
      app: helloworld
  replicas: 1
  template:
    metadata:
      labels:
        app: helloworld
    spec:
      containers:
        - name: helloworld
          image: localhost:9999/helloworld:1.2
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
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
```

次のコマンドで変更を適用します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
deployment.apps/helloworld configured
```

{{% /tab %}}
{{< /tabs >}}

次に、以下のコマンドでトラフィックを生成します。

``` bash
curl http://helloworld.localhost/hello/Kubernetes
```

1 分ほどすると、o11y cloud にトレースが流れ込んでくるはずです。ですが、もっと早くトレースを確認したい方のために、次のセクションがあります...

## チャレンジ

開発者として、トレース ID を素早く取得したり、コンソールでフィードバックを確認したい場合、deployment.yaml ファイルにどのような環境変数を追加できるでしょうか？

<details>
  <summary><b>クリックして回答を表示</b></summary>

セクション 4 *Instrument a .NET Application with OpenTelemetry* のチャレンジを思い出してください。`OTEL_TRACES_EXPORTER` 環境変数を使ってトレースをコンソールに書き出すコツを紹介しました。この変数を deployment.yaml に追加してアプリケーションを再デプロイし、helloworld アプリのログを tail することで、トレース ID を取得して Splunk Observability Cloud でトレースを見つけることができます。（次のセクションでは、K8s 環境でアプリケーションをデバッグする際に通常使用する debug exporter の使い方も説明します。）

まず、vi で deployment.yaml ファイルを開きます。

``` bash
vi deployment.yaml

```

次に、`OTEL_TRACES_EXPORTER` 環境変数を追加します。

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
              value: "deployment.environment=YOURINSTANCE"
            # NEW VALUE HERE:
            - name: OTEL_TRACES_EXPORTER
              value: "otlp,console" 
```

変更を保存し、アプリケーションを再デプロイします。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
deployment.apps/helloworld configured
```

{{% /tab %}}
{{< /tabs >}}

helloworld のログを tail します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
kubectl logs -l app=helloworld -f
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
info: HelloWorldController[0]
      /hello endpoint invoked by K8s9
Activity.TraceId:            5bceb747cc7b79a77cfbde285f0f09cb
Activity.SpanId:             ac67afe500e7ad12
Activity.TraceFlags:         Recorded
Activity.ActivitySourceName: Microsoft.AspNetCore
Activity.DisplayName:        GET hello/{name?}
Activity.Kind:               Server
Activity.StartTime:          2025-02-04T15:22:48.2381736Z
Activity.Duration:           00:00:00.0027334
Activity.Tags:
    server.address: 10.43.226.224
    server.port: 8080
    http.request.method: GET
    url.scheme: http
    url.path: /hello/K8s9
    network.protocol.version: 1.1
    user_agent.original: curl/7.81.0
    http.route: hello/{name?}
    http.response.status_code: 200
Resource associated with Activity:
    splunk.distro.version: 1.8.0
    telemetry.distro.name: splunk-otel-dotnet
    telemetry.distro.version: 1.8.0
    os.type: linux
    os.description: Debian GNU/Linux 12 (bookworm)
    os.build_id: 6.2.0-1018-aws
    os.name: Debian GNU/Linux
    os.version: 12
    host.name: helloworld-69f5c7988b-dxkwh
    process.owner: app
    process.pid: 1
    process.runtime.description: .NET 8.0.12
    process.runtime.name: .NET
    process.runtime.version: 8.0.12
    container.id: 39c2061d7605d8c390b4fe5f8054719f2fe91391a5c32df5684605202ca39ae9
    telemetry.sdk.name: opentelemetry
    telemetry.sdk.language: dotnet
    telemetry.sdk.version: 1.9.0
    service.name: helloworld
    deployment.environment: otel-jen-tko-1b75

```

{{% /tab %}}
{{< /tabs >}}

次に、別のターミナルウィンドウで curl コマンドを使ってトレースを生成します。ログを tail しているコンソールにトレース ID が表示されます。`Activity.TraceId:` の値をコピーして、APM の Trace 検索フィールドに貼り付けます。

</details>
