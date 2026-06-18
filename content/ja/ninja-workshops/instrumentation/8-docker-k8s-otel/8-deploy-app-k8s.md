---
title: アプリケーションを K8s にデプロイする
linkTitle: 8. Deploy Application to K8s
weight: 8
time: 15 minutes
---

## Dockerfile を更新する

Kubernetes では、環境変数は通常 Docker イメージに組み込むのではなく、`.yaml` マニフェストファイルで管理します。そのため、Dockerfile から以下の2つの環境変数を削除しましょう

``` bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile
```

次の2つの環境変数を削除します

``` dockerfile
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_RESOURCE_ATTRIBUTES='deployment.environment=otel-$INSTANCE'
```

> vi で変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

## 新しい Docker イメージをビルドする

環境変数を除外した新しい Docker イメージをビルドしましょう

``` bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld 

docker build -t helloworld:1.2 .
```

> 注意: 以前のバージョンと区別するために、異なるバージョン (1.2) を使用しています。
> 古いバージョンをクリーンアップするには、以下のコマンドでコンテナ ID を取得します
>
> ``` bash
> docker ps -a | grep helloworld
> ```
>
> 次に、以下のコマンドでコンテナを削除します
>
> ``` bash
> docker rm <old container id> --force
> ```
>
> コンテナイメージ ID を取得します
>
> ``` bash
> docker images | grep 1.1
> ```
>
> 最後に、以下のコマンドで古いイメージを削除します
>
> ``` bash
> docker image rm <old image id>
> ```

## Docker イメージをローカルコンテナリポジトリにインポートする

通常は Docker イメージを Docker Hub などのリポジトリにプッシュします。
しかし、このワークショップでは、EC2 インスタンス上の `localhost:9999` で動作しているローカルコンテナリポジトリに Docker イメージをプッシュします。

``` bash
# Update the image tag
docker tag helloworld:1.2 localhost:9999/helloworld:1.2

# Import the image into the local repository
docker push localhost:9999/helloworld:1.2
```

## .NET アプリケーションをデプロイする

> ヒント: vi で編集モードに入るには、'i' キーを押します。変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

.NET アプリケーションを K8s にデプロイするために、`/home/splunk` に `deployment.yaml` というファイルを作成しましょう

``` bash
vi /home/splunk/deployment.yaml
```

以下の内容を貼り付けます

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

> [!tip]- Kubernetes の Deployment とは？
> deployment.yaml ファイルは、Deployment リソースを定義するための Kubernetes 設定ファイルです。このファイルは Kubernetes でアプリケーションを管理する上での基盤となります！Deployment 設定はデプロイメントの***望ましい状態***を定義し、Kubernetes が***実際の***状態をそれに一致させます。これにより、アプリケーション Pod の自己修復が可能になり、アプリケーションの更新やロールバックも容易になります。

次に、同じディレクトリに `service.yaml` という名前の2つ目のファイルを作成します

``` bash
vi /home/splunk/service.yaml
```

以下の内容を貼り付けます

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

> [!tip]- Kubernetes の Service とは？
> Kubernetes の Service は抽象化レイヤーであり、仲介者のように機能し、Pod にアクセスするための固定 IP アドレスまたは DNS 名を提供します。これは、Pod が追加、削除、または置き換えられても変わりません。

次に、同じディレクトリに `ingress.yaml` という名前の3つ目のファイルを作成します

``` bash
vi /home/splunk/ingress.yaml
```

以下の内容を貼り付けます

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

> [!tip]- Kubernetes の Ingress とは？
> Kubernetes の Ingress は、クラスター内のサービスへの外部アクセス（通常は HTTP および HTTPS トラフィック）を管理する Kubernetes API オブジェクトです。受信接続を適切な内部サービスおよび Pod にルーティングするためのルールセットとして機能し、ロードバランシング、SSL/TLS 終端、名前ベースのバーチャルホスティングなどの機能を処理します。

これらのマニフェストファイルを使用してアプリケーションをデプロイできます

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

以下のコマンドを使用してアプリケーションにアクセスします

``` bash
curl http://helloworld.localhost/hello/Kubernetes
```

## OpenTelemetry を設定する

.NET OpenTelemetry 計装は既に Docker イメージに組み込まれています。しかし、データの送信先を指定するためにいくつかの環境変数を設定する必要があります。

先ほど作成した `deployment.yaml` ファイルに以下を追加します

> **重要** 以下の YAML 内の `$INSTANCE` をご自身のインスタンス名に置き換えてください。
> インスタンス名は `echo $INSTANCE` を実行して確認できます。

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

完成した `deployment.yaml` ファイルは以下のようになります（`$INSTANCE` の部分は**ご自身の**インスタンス名に置き換えてください）

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

以下のコマンドで変更を適用します

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

次に、以下のコマンドでトラフィックを生成します

``` bash
curl http://helloworld.localhost/hello/Kubernetes
```

1分ほどで、o11y cloud にトレースが流れ始めるはずです。しかし、トレースをすぐに確認したい場合は...

## チャレンジ

開発者としてトレース ID をすぐに取得したい場合やコンソールのフィードバックを確認したい場合、deployment.yaml ファイルにどの環境変数を追加すればよいでしょうか？

{{< details summary="ここをクリックして回答を確認" >}}
セクション4「*.NET アプリケーションを OpenTelemetry で計装する*」のチャレンジを思い出してください。`OTEL_TRACES_EXPORTER` 環境変数を使用してトレースをコンソールに書き込むテクニックを紹介しました。この変数を deployment.yaml に追加し、アプリケーションを再デプロイし、helloworld アプリのログを tail することで、トレース ID を取得して Splunk Observability Cloud でトレースを見つけることができます。（ワークショップの次のセクションでは、debug exporter の使用方法も説明します。これは K8s 環境でアプリケーションをデバッグする一般的な方法です。）

まず、vi で deployment.yaml ファイルを開きます

``` bash
vi deployment.yaml

```

次に、`OTEL_TRACES_EXPORTER` 環境変数を追加します

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

変更を保存してからアプリケーションを再デプロイします

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

helloworld のログを tail します

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

次に、別のターミナルウィンドウで curl コマンドを使用してトレースを生成します。ログを tail しているコンソールにトレース ID が表示されます。`Activity.TraceId:` の値をコピーして、APM のトレース検索フィールドに貼り付けてください。
{{< /details >}}
