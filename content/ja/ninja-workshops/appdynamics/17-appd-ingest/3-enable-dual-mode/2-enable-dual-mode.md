---
title: 2. Dual Mode の有効化
weight: 2
---

JVM コマンドラインに dual signal mode フラグを追加してアプリケーションを再起動します。

## 実行中のアプリケーションを停止する

Phase 1 のアプリケーションとロードジェネレーターを停止します:

```bash
kill %2 2>/dev/null   # stop load generator
kill %1 2>/dev/null   # stop the java app
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
`kill %1` が機能しない場合は、`ps aux | grep ingest-workshop` で PID を見つけて直接 kill してください。
{{% /notice %}}

## Dual Mode で再起動する

同じ AppD フラグに加えて、dual mode と OTel エクスポーターフラグを追加してアプリケーションを再度実行します。Phase 1 で設定した `${APPD_ACCESS_KEY}` と `${APPD_APP_NAME}` の変数を同じ値で使用します:

アプリケーションを呼び出す `-jar app/target/ingest-workshop-1.0.0.jar &` の直前に4行追加しています。

```bash
cd ~/workshop/appd

java -javaagent:agent/javaagent.jar \
  -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com \
  -Dappdynamics.controller.port=443 \
  -Dappdynamics.controller.ssl.enabled=true \
  -Dappdynamics.agent.applicationName=${APPD_APP_NAME} \
  -Dappdynamics.agent.tierName=OrderService \
  -Dappdynamics.agent.nodeName=OrderService-Node \
  -Dappdynamics.agent.accountName=se-lab \
  -Dappdynamics.agent.accountAccessKey=${APPD_ACCESS_KEY} \
  -Dagent.deployment.mode=dual \
  -Dotel.traces.exporter=otlp \
  -Dotel.exporter.otlp.endpoint=http://localhost:4318 \
  -Dotel.resource.attributes=service.name=OrderService,service.namespace=Dual-Ingest-${INSTANCE},deployment.environment=${INSTANCE}-appd-dual,deployment.environment.name=${INSTANCE}-appd-dual \
  -jar app/target/ingest-workshop-1.0.0.jar &
```

Spring Boot の起動バナーが表示されるまで待ちます。
Enter キーを押してプロンプトに戻ります。

### 新しいフラグの説明

| フラグ | 目的 |
|---|---|
| `-Dagent.deployment.mode=dual` | dual signal mode を有効にします。完全な OTel Java 自動計装が AppD エージェントと並行して実行されます |
| `-Dotel.traces.exporter=otlp` | OTel 計装に OTLP 経由でスパンをエクスポートするよう指示します |
| `-Dotel.exporter.otlp.endpoint` | ポート 4318 (HTTP/protobuf) のローカル OTel Collector を指定します |
| `-Dotel.resource.attributes` | OTel リソース属性を設定します: `service.name` は AppD ティアに、`service.namespace` は AppD アプリケーションに、`deployment.environment`/`deployment.environment.name` はワークショップインスタンスのデータにタグ付けされます |

## ロードジェネレーターを再起動する

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## Dual Mode が有効であることを確認する

アプリケーションログで dual mode が開始されたことを確認します:

{{< tabs >}}
{{% tab title="Command" %}}

```bash
ps aux | grep "deployment.mode=dual"
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
splunk@ip-172-31-77-108 ~/workshop/appd $ ps aux | grep "deployment.mode=dual" | grep -v grep
splunk    181598  172  2.1 14402900 717736 pts/0 SNl  21:31   1:02 java -javaagent:agent/javaagent.jar -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com -Dappdynamics.controller.port=443 -Dappdynamics.controller.ssl.enabled=true -Dappdynamics.agent.applicationName=Dual-Ingest-shw-1123 -Dappdynamics.agent.tierName=OrderService -Dappdynamics.agent.nodeName=OrderService-Node -Dappdynamics.agent.accountName=se-lab -Dappdynamics.agent.accountAccessKey=hj9999999999 -Dagent.deployment.mode=dual -Dotel.traces.exporter=otlp -Dotel.exporter.otlp.endpoint=http://localhost:4318 -Dotel.resource.attributes=service.name=OrderService,service.namespace=Dual-Ingest-shw-a79e,deployment.environment=shw-a79e-appd-dual -jar app/target/ingest-workshop-1.0.0.jar
```

{{% /tab %}}
{{< /tabs >}}

`deployment.mode=dual` フラグが付いた java プロセスが表示されるはずです。

AppDynamics エージェントは以下を送信しています:

- **AppD APM データ** を AppDynamics Controller へ（変更なし）
- **OTLP トレース** を `localhost:4318` のローカル OTel Collector へ送信し、そこから Splunk Observability Cloud に転送されます
  - インスタンスで `env` を使用して、環境 `deployment.environment=${INSTANCE}-appd-dual` に使用される `{INSTANCE}` の値を確認できます
