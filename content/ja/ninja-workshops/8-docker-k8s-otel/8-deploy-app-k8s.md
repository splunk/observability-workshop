---
title: アプリケーションをK8sにデプロイ
linkTitle: 8. アプリケーションをK8sにデプロイ
weight: 8
time: 15 minutes
---

## Dockerfile の更新

Kubernetesでは、環境変数は通常、Dockerイメージに組み込むのではなく `.yaml` マニフェストファイルで管理されます。そこで、Dockerfileから以下の2つの環境変数を削除しましょう：

```bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile
```

次に、以下の2つの環境変数を削除します：

```dockerfile
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_RESOURCE_ATTRIBUTES='deployment.environment=otel-$INSTANCE'
```

> vi での変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

## 新しい Docker イメージのビルド

環境変数を除外した新しいDockerイメージをビルドしましょう：

```bash
cd /home/splunk/workshop/docker-k8s-otel/helloworld

docker build -t helloworld:1.2 .
```

> Note: we've used a different version (1.2) to distinguish the image from our earlier version.
> To clean up the older versions, run the following command to get the container id:
>
> ```bash
> docker ps -a
> ```
>
> Then run the following command to delete the container:
>
> ```bash
> docker rm <old container id> --force
> ```
>
> Now we can get the container image id:
>
> ```bash
> docker images | grep 1.1
> ```
>
> Finally, we can run the following command to delete the old image:
>
> ```bash
> docker image rm <old image id>
> ```

## Docker イメージを Kubernetes にインポート

通常であれば、DockerイメージをDocker Hubなどのリポジトリにプッシュします。
しかし、今回のセッションでは、k3sに直接インポートする回避策を使用します。

```bash
cd /home/splunk

# Import the image into k3d
sudo k3d image import helloworld:1.2 --cluster $INSTANCE-cluster
```

## .NET アプリケーションのデプロイ

> ヒント：vi で編集モードに入るには「i」キーを押します。変更を保存するには、`esc` キーを押してコマンドモードに入り、`:wq!` と入力してから `enter/return` キーを押します。

.NETアプリケーションをK8sにデプロイするために、`/home/splunk` に `deployment.yaml` という名前のファイルを作成しましょう：

```bash
vi /home/splunk/deployment.yaml
```

そして以下を貼り付けます：

```yaml
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
          image: docker.io/library/helloworld:1.2
          imagePullPolicy: Never
          ports:
            - containerPort: 8080
          env:
            - name: PORT
              value: "8080"
```

> [!tip]- Kubernetes における Deployment とは？
> deployment.yaml ファイルは、deployment リソースを定義するために使用される kubernetes 設定ファイルです。このファイルは Kubernetes でアプリケーションを管理するための基盤となります！deployment 設定は deployment の **_望ましい状態_** を定義し、Kubernetes が **_実際の状態_** がそれと一致するよう保証します。これにより、アプリケーション pod の自己修復が可能になり、アプリケーションの簡単な更新やロールバックも可能になります。

次に、同じディレクトリに `service.yaml` という名前の2つ目のファイルを作成します：

```bash
vi /home/splunk/service.yaml
```

そして以下を貼り付けます：

```yaml
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

> [!tip]- Kubernetes における Service とは？
> Kubernetes の Service は抽象化レイヤーであり、仲介者のような役割を果たします。Pod にアクセスするための固定 IP アドレスや DNS 名を提供し、時間の経過とともに Pod が追加、削除、または交換されても同じままです。

これらのマニフェストファイルを使用してアプリケーションをデプロイできます：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
# create the deployment
kubectl apply -f deployment.yaml

# create the service
kubectl apply -f service.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
deployment.apps/helloworld created
service/helloworld created
```

{{% /tab %}}
{{< /tabs >}}

## アプリケーションのテスト

アプリケーションにアクセスするには、まずIPアドレスを取得する必要があります：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl describe svc helloworld | grep IP:
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
IP:                10.43.102.103
```

{{% /tab %}}
{{< /tabs >}}

その後、前のコマンドから返されたCluster IPを使用してアプリケーションにアクセスできます。
例：

```bash
curl http://10.43.102.103:8080/hello/Kubernetes
```

## OpenTelemetry の設定

.NET OpenTelemetry計装はすでにDockerイメージに組み込まれています。しかし、データの送信先を指定するためにいくつかの環境変数を設定する必要があります。

先ほど作成した `deployment.yaml` ファイルに以下を追加します：

> **重要** 以下の YAML の `$INSTANCE` をあなたのインスタンス名に置き換えてください。
> インスタンス名は `echo $INSTANCE` を実行することで確認できます。

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
```

完全な `deployment.yaml` ファイルは以下のようになります（`$INSTANCE` ではなく**あなたの**インスタンス名を使用してください）：

```yaml
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
          image: docker.io/library/helloworld:1.2
          imagePullPolicy: Never
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

以下のコマンドで変更を適用します：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
deployment.apps/helloworld configured
```

{{% /tab %}}
{{< /tabs >}}

その後、`curl` を使用してトラフィックを生成します。

1分ほど経過すると、o11y cloudでトレースが流れているのが確認できるはずです。ただし、より早くトレースを確認したい場合は、以下の方法があります...

## チャレンジ

開発者として、トレースIDを素早く取得するか、コンソールフィードバックを見たい場合、deployment.yamlファイルにどのような環境変数を追加できるでしょうか？

<details>
  <summary><b>答えを見るにはここをクリック</b></summary>

セクション4「.NET ApplicationをOpenTelemetryで計装する」のチャレンジで思い出していただければ、`OTEL_TRACES_EXPORTER` 環境変数を使ってtraceをconsoleに書き込むトリックをお見せしました。この変数をdeployment.yamlに追加し、アプリケーションを再deployして、helloworldアプリからlogをtailすることで、trace idを取得してSplunk Observability Cloudでtraceを見つけることができます。（ワークショップの次のセクションでは、debug exporterの使用についても説明します。これはK8s環境でアプリケーションをdebugする際の典型的な方法です。）

まず、viでdeployment.yamlファイルを開きます：

```bash
vi deployment.yaml

```

次に、`OTEL_TRACES_EXPORTER` 環境変数を追加します：

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
    value: "deployment.environment=YOURINSTANCE"
  # NEW VALUE HERE:
  - name: OTEL_TRACES_EXPORTER
    value: "otlp,console"
```

変更を保存してからアプリケーションを再deployします：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
deployment.apps/helloworld configured
```

{{% /tab %}}
{{< /tabs >}}

helloworldのlogをtailします：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl logs -l app=helloworld -f
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
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

次に、別のterminal windowでcurlコマンドを使ってtraceを生成します。logをtailしているconsoleでtrace idが表示されるはずです。`Activity.TraceId:` の値をコピーして、APMのTrace検索フィールドに貼り付けてください。

</details>
