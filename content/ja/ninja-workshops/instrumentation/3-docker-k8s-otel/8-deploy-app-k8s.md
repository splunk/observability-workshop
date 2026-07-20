---
title: アプリケーションをK8sにデプロイする
linkTitle: 8. アプリケーションをK8sにデプロイする
weight: 8
time: 15 minutes
---

## Dockerfileを更新する

Kubernetesでは、環境変数は通常Dockerイメージに組み込むのではなく、`.yaml` マニフェストファイルで管理します。Dockerfileから以下の2つの環境変数を削除しましょう。

``` bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile
```

以下の2つの環境変数を削除します。

``` dockerfile
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_RESOURCE_ATTRIBUTES='deployment.environment=otel-$INSTANCE'
```

> viで変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力して `enter/return` キーを押します。

## 新しいDockerイメージをビルドする

環境変数を除外した新しいDockerイメージをビルドします。

``` bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld 

docker build -t helloworld:1.2 .
```

> 注意: 以前のバージョンと区別するために、異なるバージョン（1.2）を使用しています。
> 古いバージョンをクリーンアップするには、以下のコマンドでコンテナIDを取得します。
>
> ``` bash
> docker ps -a | grep helloworld
> ```
>
> 次に以下のコマンドでコンテナを削除します。
>
> ``` bash
> docker rm <old container id> --force
> ```
>
> コンテナイメージIDを取得します。
>
> ``` bash
> docker images | grep 1.1
> ```
>
> 最後に、以下のコマンドで古いイメージを削除します。
>
> ``` bash
> docker image rm <old image id>
> ```

## Dockerイメージをローカルコンテナリポジトリにインポートする

通常はDockerイメージをDocker Hubなどのリポジトリにプッシュしますが、このワークショップでは、EC2インスタンス上の `localhost:9999` で動作しているローカルコンテナリポジトリにDockerイメージをプッシュします。

``` bash
# Update the image tag
docker tag helloworld:1.2 localhost:9999/helloworld:1.2

# Import the image into the local repository
docker push localhost:9999/helloworld:1.2
```

## .NETアプリケーションをデプロイする

> ヒント: viで編集モードに入るには、'i'キーを押します。変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力して `enter/return` キーを押します。

.NETアプリケーションをK8sにデプロイするために、`/home/splunk` に `deployment.yaml` というファイルを作成します。

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

> [!tip]- KubernetesにおけるDeploymentとは？
> deployment.yamlファイルは、Deploymentリソースを定義するためのKubernetes設定ファイルです。このファイルはKubernetesでアプリケーションを管理する際の基盤となります。Deployment設定はデプロイメントの ***望ましい状態*** を定義し、Kubernetesは ***実際の*** 状態がそれに一致するようにします。これにより、アプリケーションPodの自己修復が可能になり、アプリケーションの更新やロールバックも容易になります。

次に、同じディレクトリに `service.yaml` という2つ目のファイルを作成します。

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

> [!tip]- KubernetesにおけるServiceとは？
> KubernetesにおけるServiceは抽象化レイヤーであり、仲介役として機能します。Podにアクセスするための固定IPアドレスまたはDNS名を提供し、Podが追加、削除、または置き換えられても同じアドレスを維持します。

次に、同じディレクトリに `ingress.yaml` という3つ目のファイルを作成します。

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

> [!tip]- KubernetesにおけるIngressとは？
> KubernetesにおけるIngressは、クラスター内のサービスへの外部アクセス（通常はHTTPおよびHTTPSトラフィック）を管理するKubernetes APIオブジェクトです。受信接続を適切な内部サービスやPodにルーティングするためのルールセットとして機能し、ロードバランシング、SSL/TLS終端、名前ベースのバーチャルホスティングなどの機能を処理します。

これらのマニフェストファイルを使用してアプリケーションをデプロイします。

{{< tabs >}}
{{% tab title="スクリプト" %}}

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
{{% tab title="出力例" %}}

``` bash
deployment.apps/helloworld created
service/helloworld created
ingress.networking.k8s.io/helloworld-ingress created
```

{{% /tab %}}
{{< /tabs >}}

## アプリケーションをテストする

以下のコマンドでアプリケーションにアクセスします。

``` bash
curl http://helloworld.localhost/hello/Kubernetes
```

## OpenTelemetryを設定する

.NETのOpenTelemetry計装はすでにDockerイメージに組み込まれています。しかし、データの送信先を指定するためにいくつかの環境変数を設定する必要があります。

先ほど作成した `deployment.yaml` ファイルに以下を追加します。

> **重要** 以下のYAMLの `$INSTANCE` をインスタンス名に置き換えてください。インスタンス名は `echo $INSTANCE` を実行して確認できます。

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

完成した `deployment.yaml` ファイルは以下のようになります（`$INSTANCE` の部分には **自分の** インスタンス名を入れてください）。

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

以下のコマンドで変更を適用します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="出力例" %}}

``` bash
deployment.apps/helloworld configured
```

{{% /tab %}}
{{< /tabs >}}

次に、以下のコマンドでトラフィックを生成します。

``` bash
curl http://helloworld.localhost/hello/Kubernetes
```

1分ほどでSplunk Observability Cloudにトレースが表示されます。しかし、より早くトレースを確認したい場合は...

## チャレンジ

開発者としてトレースIDをすぐに取得したい場合やコンソールのフィードバックを確認したい場合、deployment.yamlファイルにどの環境変数を追加すればよいでしょうか？

{{< details summary="ここをクリックして回答を確認" >}}
セクション4「.NETアプリケーションにOpenTelemetryを計装する」のチャレンジを思い出してください。`OTEL_TRACES_EXPORTER` 環境変数を使用してトレースをコンソールに出力するテクニックを紹介しました。この変数をdeployment.yamlに追加し、アプリケーションを再デプロイし、helloworldアプリのログをtailすることで、トレースIDを取得してSplunk Observability Cloudでトレースを検索できます。（次のセクションでは、K8s環境でアプリケーションをデバッグする際の一般的な方法であるdebug exporterの使用方法についても説明します。）

まず、viでdeployment.yamlファイルを開きます。

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

変更を保存してアプリケーションを再デプロイします。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="出力例" %}}

```bash
deployment.apps/helloworld configured
```

{{% /tab %}}
{{< /tabs >}}

helloworldのログをtailします。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
kubectl logs -l app=helloworld -f
```

{{% /tab %}}
{{% tab title="出力例" %}}

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

別のターミナルウィンドウでcurlコマンドを使用してトレースを生成します。ログをtailしているコンソールにトレースIDが表示されます。`Activity.TraceId:` の値をコピーして、APMのTrace検索フィールドに貼り付けます。
{{< /details >}}
