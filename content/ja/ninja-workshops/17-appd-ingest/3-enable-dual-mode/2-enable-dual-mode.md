---
title: 2. デュアルモードの有効化
weight: 2
---

JVMコマンドラインにデュアルシグナルモードのフラグを追加して、アプリケーションを再起動します。

## 実行中のアプリケーションを停止する

Phase 1で起動したアプリケーションとロードジェネレーターを停止します：

```bash
kill %2 2>/dev/null   # stop load generator
kill %1 2>/dev/null   # stop the java app
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
`kill %1` が動作しない場合は、`ps aux | grep ingest-workshop` でPIDを確認して直接killしてください。
{{% /notice %}}

## デュアルモードで再起動する

同じAppDフラグに加えて、デュアルモードとOTelエクスポーターのフラグを追加してアプリケーションを再度実行します。`<YOUR-ACCESS-KEY>` と `<YourInitials>` はPhase 1で使用したものと同じ値に置き換えてください：

アプリケーションを起動する `-jar app/target/ingest-workshop-1.0.0.jar &` の直前に4行追加します。

```bash
cd ~/workshop/appd

java -javaagent:agent/javaagent.jar \
  -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com \
  -Dappdynamics.controller.port=443 \
  -Dappdynamics.controller.ssl.enabled=true \
  -Dappdynamics.agent.applicationName=Dual-Ingest-<YourInitials> \
  -Dappdynamics.agent.tierName=OrderService \
  -Dappdynamics.agent.nodeName=OrderService-Node \
  -Dappdynamics.agent.accountName=se-lab \
  -Dappdynamics.agent.accountAccessKey=<YOUR-ACCESS-KEY> \
  -Dagent.deployment.mode=dual \
  -Dotel.traces.exporter=otlp \
  -Dotel.exporter.otlp.endpoint=http://localhost:4318 \
  -Dotel.resource.attributes=service.name=OrderService,service.namespace=Dual-Ingest-${INSTANCE},deployment.environment=${INSTANCE}-appd-dual \
  -jar app/target/ingest-workshop-1.0.0.jar &
```

Spring Bootの起動バナーが表示されるまで待ちます。

### 新しいフラグの説明

| フラグ | 目的 |
|---|---|
| `-Dagent.deployment.mode=dual` | デュアルシグナルモードを有効にします -- OTel Java 自動計装が AppD エージェントと並行して動作します |
| `-Dotel.traces.exporter=otlp` | OTel 計装に OTLP 経由でスパンをエクスポートするよう指示します |
| `-Dotel.exporter.otlp.endpoint` | ポート 4318（HTTP/protobuf）のローカル OTel Collector を指定します |
| `-Dotel.resource.attributes` | OTel リソース属性を設定します：`service.name` は AppD の tier に、`service.namespace` は AppD の application に、`deployment.environment` はワークショップインスタンスのデータにタグ付けされます |

## ロードジェネレーターを再起動する

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## デュアルモードが有効であることを確認する

アプリケーションログを確認して、デュアルモードが開始されたことを確認します：

{{< tabs >}}
{{% tab title="Command" %}}

```bash
ps aux | grep "deployment.mode=dual" | grep -v grep
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
splunk@ip-172-31-77-108 ~/workshop/appd $ ps aux | grep "deployment.mode=dual" | grep -v grep
splunk    181598  172  2.1 14402900 717736 pts/0 SNl  21:31   1:02 java -javaagent:agent/javaagent.jar -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com -Dappdynamics.controller.port=443 -Dappdynamics.controller.ssl.enabled=true -Dappdynamics.agent.applicationName=Dual-Ingest-JRH -Dappdynamics.agent.tierName=OrderService -Dappdynamics.agent.nodeName=OrderService-Node -Dappdynamics.agent.accountName=se-lab -Dappdynamics.agent.accountAccessKey=hj9999999999 -Dagent.deployment.mode=dual -Dotel.traces.exporter=otlp -Dotel.exporter.otlp.endpoint=http://localhost:4318 -Dotel.resource.attributes=service.name=OrderService,service.namespace=Dual-Ingest-shw-a79e,deployment.environment=shw-a79e-appd-dual -jar app/target/ingest-workshop-1.0.0.jar
```

{{% /tab %}}
{{< /tabs >}}

`deployment.mode=dual` フラグが設定されたjavaプロセスが表示されるはずです。

AppDynamicsエージェントは現在、以下のデータを送信しています：

- **AppD APM データ** をAppDynamics Controllerへ（変更なし）
- **OTLP トレース** を `localhost:4318` のローカルOTel Collectorへ送信し、そこからSplunk Observability Cloudに転送されます
  - インスタンスで `env` を使用して、環境 `deployment.environment=${INSTANCE}-appd-dual` に使用される `{INSTANCE}` の値を確認できます
