---
title: 2. デュアルモードの有効化
weight: 2
---

JVM コマンドラインにデュアルシグナルモードのフラグを追加して、アプリケーションを再起動します。

## 実行中のアプリケーションを停止する

フェーズ 1 のアプリケーションとロードジェネレーターを停止します

```bash
kill %2 2>/dev/null   # stop load generator
kill %1 2>/dev/null   # stop the java app
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
`kill %1` が動作しない場合は、`ps aux | grep ingest-workshop` で PID を確認し、直接 kill してください。
{{% /notice %}}

## デュアルモードで再起動する

同じ AppD フラグに加えて、デュアルモードと OTel エクスポーターのフラグを追加してアプリケーションを再度実行します。フェーズ 1 で設定した `${APPD_ACCESS_KEY}` と `${APPD_APP_NAME}` の変数を同じ値で使用します

アプリケーションを起動する `-jar app/target/ingest-workshop-1.0.0.jar &` の直前に 4 行を追加しています。

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
| `-Dagent.deployment.mode=dual` | デュアルシグナルモードを有効にし、完全な OTel Java 自動インストルメンテーションが AppD エージェントと並行して動作します |
| `-Dotel.traces.exporter=otlp` | OTel インストルメンテーションに OTLP 経由でスパンをエクスポートするよう指示します |
| `-Dotel.exporter.otlp.endpoint` | ポート 4318（HTTP/protobuf）のローカル OTel Collector を指定します |
| `-Dotel.resource.attributes` | OTel リソース属性を設定します`service.name` は AppD ティアに、`service.namespace` は AppD アプリケーションにマッピングされ、`deployment.environment`/`deployment.environment.name` はワークショップインスタンスのデータにタグ付けします |

## ロードジェネレーターを再起動する

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## デュアルモードがアクティブであることを確認する

アプリケーションログでデュアルモードが開始されたことを確認します

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

`deployment.mode=dual` フラグが付いた Java プロセスが表示されるはずです。

AppDynamics エージェントは以下のデータを送信しています

- **AppD APM データ** を AppDynamics Controller へ（変更なし）
- **OTLP トレース** をローカル OTel Collector（`localhost:4318`）へ送信し、そこから Splunk Observability Cloud に転送されます
  - インスタンスで `env` を使用して、環境 `deployment.environment=${INSTANCE}-appd-dual` に使用される `{INSTANCE}` の値を確認できます
