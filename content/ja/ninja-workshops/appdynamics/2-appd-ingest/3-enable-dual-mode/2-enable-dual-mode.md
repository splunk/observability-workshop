---
title: 2. Dual Modeの有効化
weight: 2
---

Dual Signal Modeフラグを JVMコマンドラインに追加してアプリケーションを再起動します。

## 実行中のアプリケーションを停止する

Phase 1のアプリケーションとロードジェネレーターを停止します。

```bash
kill %2 2>/dev/null   # stop load generator
kill %1 2>/dev/null   # stop the java app
```

{{% notice title="Tip" style="primary" icon="lightbulb" %}}
`kill %1` が機能しない場合は、`ps aux | grep ingest-workshop` でPIDを確認し、直接killしてください。
{{% /notice %}}

## Dual Modeで再起動する

同じAppDフラグに加え、Dual ModeとOTel Exporterフラグを追加してアプリケーションを再度実行します。Phase 1で設定した `${APPD_ACCESS_KEY}` と `${APPD_APP_NAME}` の変数を同じ値で使用します。

アプリケーションを起動する `-jar app/target/ingest-workshop-1.0.0.jar &` の直前に4行を追加しています。

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

Spring Bootのスタートアップバナーが表示されるまで待ちます。
Enterキーを押してプロンプトに戻ります。

### 新しいフラグの説明

| フラグ | 目的 |
|---|---|
| `-Dagent.deployment.mode=dual` | Dual Signal Modeを有効にし、OTel Java自動計装がAppDエージェントと並行して動作します |
| `-Dotel.traces.exporter=otlp` | OTel計装にOTLP経由でSpanをエクスポートするよう指示します |
| `-Dotel.exporter.otlp.endpoint` | ポート4318（HTTP/protobuf）のローカルOTel Collectorを指定します |
| `-Dotel.resource.attributes` | OTelリソース属性を設定します。`service.name` はAppDのtierに、`service.namespace` はAppDのアプリケーションにマッピングされ、`deployment.environment`/`deployment.environment.name` はワークショップインスタンスのデータにタグ付けします |

## ロードジェネレーターを再起動する

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## Dual Modeが有効であることを確認する

アプリケーションログでDual Modeが開始されたことを確認します。

{{< tabs >}}
{{% tab title="コマンド" %}}

```bash
ps aux | grep "deployment.mode=dual"
```

{{% /tab %}}
{{% tab title="出力例" %}}

```text
splunk@ip-172-31-77-108 ~/workshop/appd $ ps aux | grep "deployment.mode=dual" | grep -v grep
splunk    181598  172  2.1 14402900 717736 pts/0 SNl  21:31   1:02 java -javaagent:agent/javaagent.jar -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com -Dappdynamics.controller.port=443 -Dappdynamics.controller.ssl.enabled=true -Dappdynamics.agent.applicationName=Dual-Ingest-shw-1123 -Dappdynamics.agent.tierName=OrderService -Dappdynamics.agent.nodeName=OrderService-Node -Dappdynamics.agent.accountName=se-lab -Dappdynamics.agent.accountAccessKey=hj9999999999 -Dagent.deployment.mode=dual -Dotel.traces.exporter=otlp -Dotel.exporter.otlp.endpoint=http://localhost:4318 -Dotel.resource.attributes=service.name=OrderService,service.namespace=Dual-Ingest-shw-a79e,deployment.environment=shw-a79e-appd-dual -jar app/target/ingest-workshop-1.0.0.jar
```

{{% /tab %}}
{{< /tabs >}}

`deployment.mode=dual` フラグが付いたJavaプロセスが表示されます。

AppDynamicsエージェントは以下を送信しています:

- **AppD APMデータ** をAppDynamics Controllerへ（変更なし）
- **OTLPトレース** を `localhost:4318` のローカルOTel Collectorへ。そこからSplunk Observability Cloudに転送されます
  - インスタンスで `env` を実行すると、環境 `deployment.environment=${INSTANCE}-appd-dual` に使用されている `{INSTANCE}` の値を確認できます
