---
title: アプリケーションをK8sにデプロイ
linkTitle: 8. アプリケーショ## DockerイメージをKubernetesにインポート

通常であれば、DockerイメージをDocker Hubなどのリポジトリにプッシュします。
しかし、今回のセッションでは、k3sに直接インポートする回避策を使用します。sにデプロイ
weight: 8
time: 15 minutes
---

## Dockerfile の更新

Kubernetes では、環境変数は通常、Docker イメージに組み込むのではなく`.yaml`マニフェストファイルで管理されます。そこで、Dockerfile から以下の 2 つの環境変数を削除しましょう：

```bash
vi /home/splunk/workshop/docker-k8s-otel/helloworld/Dockerfile
```

次に、以下の 2 つの環境変数を削除します：

```dockerfile
ENV OTEL_SERVICE_NAME=helloworld
ENV OTEL_RESOURCE_ATTRIBUTES='deployment.environment=otel-$INSTANCE'
```

> vi での変更を保存するには、`esc`キーを押してコマンドモードに入り、`:wq!`と入力してから`enter/return`キーを押します。

## 新しい Docker イメージのビルド

環境変数を除外した新しい Docker イメージをビルドしましょう：

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

## Import the Docker Image to Kubernetes

Normally we’d push our Docker image to a repository such as Docker Hub.
But for this session, we’ll use a workaround to import it to k3s directly.

```bash
cd /home/splunk

# Export the image from docker
docker save --output helloworld.tar helloworld:1.2

# Import the image into k3s
sudo k3s ctr images import helloworld.tar
```

## .NET アプリケーションのデプロイ

> ヒント：vi で編集モードに入るには「i」キーを押します。変更を保存するには、`esc`キーを押してコマンドモードに入り、`:wq!`と入力してから`enter/return`キーを押します。

.NET アプリケーションを K8s にデプロイするために、`/home/splunk`に`deployment.yaml`という名前のファイルを作成しましょう：

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

> [!tip]- What is a Deployment in Kubernetes?
> The deployment.yaml file is a kubernetes config file that is used to define a deployment resource. This file is the cornerstone of managing applications in Kubernetes! The deployment config defines the deployment’s **_desired state_** and Kubernetes then ensures the **_actual_** state matches it. This allows application pods to self-heal and also allows for easy updates or roll backs to applications.

次に、同じディレクトリに`service.yaml`という名前の 2 つ目のファイルを作成します：

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

> [!tip]- What is a Service in Kubernetes?
> A Service in Kubernetes is an abstraction layer, working like a middleman, giving you a fixed IP address or DNS name to access your Pods, which stays the same, even if Pods are added, removed, or replaced over time.

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

アプリケーションにアクセスするには、まず IP アドレスを取得する必要があります：

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

その後、前のコマンドから返された Cluster IP を使用してアプリケーションにアクセスできます。
例：

```bash
curl http://10.43.102.103:8080/hello/Kubernetes
```

## OpenTelemetry の設定

.NET OpenTelemetry インストゥルメンテーションはすでに Docker イメージに組み込まれています。しかし、データの送信先を指定するためにいくつかの環境変数を設定する必要があります。

先ほど作成した`deployment.yaml`ファイルに以下を追加します：

> **重要** 以下の YAML の`$INSTANCE`をあなたのインスタンス名に置き換えてください。
> インスタンス名は`echo $INSTANCE`を実行することで確認できます。

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

The complete `deployment.yaml` file should be as follows (with **your** instance name rather than `$INSTANCE`):

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

Apply the changes with:

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

Then use `curl` to generate some traffic.

After a minute or so, you should see traces flowing in the o11y cloud. But, if you want to see your trace sooner, we have ...

## チャレンジ

開発者として、トレース ID を素早く取得するか、コンソールフィードバックを見たい場合、deployment.yaml ファイルにどのような環境変数を追加できるでしょうか？

<details>
  <summary><b>答えを見るにはここをクリック</b></summary>

If you recall in our challenge from Section 4, _Instrument a .NET Application with OpenTelemetry_, we showed you a trick to write traces to the console using the `OTEL_TRACES_EXPORTER` environment variable. We can add this variable to our deployment.yaml, redeploy our application, and tail the logs from our helloworld app so that we can grab the trace id to then find the trace in Splunk Observability Cloud. (In the next section of our workshop, we will also walk through using the debug exporter, which is how you would typically debug your application in a K8s environment.)

First, open the deployment.yaml file in vi:

```bash
vi deployment.yaml

```

Then, add the `OTEL_TRACES_EXPORTER` environment variable:

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

Save your changes then redeploy the application:

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

Tail the helloworld logs:

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

Then, in your other terminal window, generate a trace with your curl command. You will see the trace id in the console in which you are tailing the logs. Copy the `Activity.TraceId:` value and paste it into the Trace search field in APM.

</details>
