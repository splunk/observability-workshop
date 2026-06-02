---
title: 2. デュアルモードを有効化する
weight: 2
---

JVMコマンドラインにデュアルシグナルモードのフラグを追加して、アプリケーションを再起動します。

## 実行中のアプリケーションを停止する

Phase 1 のアプリと負荷生成プロセスを停止します:

```bash
kill %2 2>/dev/null   # stop load generator
kill %1 2>/dev/null   # stop the java app
```

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
`kill %1` がうまくいかない場合は、`ps aux | grep ingest-workshop` で PID を確認し、直接 kill してください。
{{% /notice %}}

## デュアルモードで再起動する

同じ AppD のフラグに加え、デュアルモードと OTel エクスポーターのフラグを指定してアプリを再度実行します。Phase 1 で使用した値と同じ `${APPD_ACCESS_KEY}` および `${APPD_APP_NAME}` の変数をそのまま利用します:

アプリケーション起動行 `-jar app/target/ingest-workshop-1.0.0.jar &` の直前に 4 行を追加します。

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

Spring Boot の起動バナーが表示されるまで待機します。
return キーを押してプロンプトに戻ります。

### 新しく追加したフラグの役割

| フラグ | 目的 |
|---|---|
| `-Dagent.deployment.mode=dual` | デュアルシグナルモードを有効化します。OTel Java の自動計装が AppD エージェントと並行して動作します |
| `-Dotel.traces.exporter=otlp` | OTel 計装に対して、スパンを OTLP 経由でエクスポートするよう指示します |
| `-Dotel.exporter.otlp.endpoint` | ポート 4318 (HTTP/protobuf) で動作するローカルの OTel Collector を指定します |
| `-Dotel.resource.attributes` | OTel のリソース属性を設定します: `service.name` は AppD のティア、`service.namespace` は AppD のアプリケーションにマッピングされ、`deployment.environment`/`deployment.environment.name` はワークショップのインスタンス向けにデータをタグ付けします |

## 負荷生成プロセスを再起動する

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## デュアルモードが有効化されていることを確認する

アプリケーションログでデュアルモードが起動したことを確認します:

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

`deployment.mode=dual` フラグが付与された java プロセスが確認できるはずです。

これで AppDynamics エージェントは以下を送信しています:

- **AppD APM データ** を AppDynamics Controller へ送信 (変更なし)
- **OTLP トレース** を `localhost:4318` のローカル OTel Collector へ送信し、そこから Splunk Observability Cloud へ転送
  - 自分のインスタンスで `env` を実行すると、環境で使用されている `{INSTANCE}` の値が確認できます (`deployment.environment=${INSTANCE}-appd-dual`)
