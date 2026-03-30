---
title: 3. AppD で実行して確認する
weight: 3
---

AppDynamicsエージェントをアタッチしてアプリケーションを実行します。これは「通常の」単一送信先へのインストルメンテーションです。

## AppDynamics エージェントで実行する

前のステップで取得した値で `<YOUR-ACCESS-KEY>` と `<YourInitials>` を置き換えてください：

{{< tabs >}}
{{% tab title="Command" %}}

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
  -jar app/target/ingest-workshop-1.0.0.jar &
```

{{% /tab %}}
{{% tab title="Example" %}}

```text
java -javaagent:agent/javaagent.jar \
  -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com \
  -Dappdynamics.controller.port=443 \
  -Dappdynamics.controller.ssl.enabled=true \
  -Dappdynamics.agent.applicationName=Dual-Ingest-JRH \
  -Dappdynamics.agent.tierName=OrderService \
  -Dappdynamics.agent.nodeName=OrderService-Node \
  -Dappdynamics.agent.accountName=se-lab \
  -Dappdynamics.agent.accountAccessKey="hj9999999999" \
  -jar app/target/ingest-workshop-1.0.0.jar &
```

{{% /tab %}}
{{< /tabs >}}

Spring Bootの起動バナーが表示されるまで待ちます（約10〜15秒）。

## 負荷を生成する

シンプルな負荷生成器をバックグラウンドで起動します：

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## AppDynamics Controller で確認する

1. [AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/) を開きます
2. **Applications** に移動し、ご自身のアプリケーションを見つけます（例：`Dual-Ingest-YOURINITIALS`）
3. アプリケーションをクリックして **Flow Map** を表示します

{{% notice title="お待ちください" style="info" icon="info-circle" %}}
アプリケーションが登録され、ビジネストランザクションがフローマップに表示されるまで2〜5分かかる場合があります。必要に応じてページを更新してください。
{{% /notice %}}

以下が表示されるはずです：

- フローマップ内の **OrderService** ティア
- `/order` と `/inventory` エンドポイントのビジネストランザクション
- コントローラーに流れるメトリクスデータ

この時点では、データは **AppDynamics にのみ**送信されています。アプリケーションはSplunk Observability Cloudには接続されていません。次のフェーズでは、デュアルシグナルモードを有効にしてこれを変更します。
![AppDynamics Application](../../_images/appd-service.png?width=30vw)

{{% notice title="実行したままにしてください" style="warning" icon="exclamation-triangle" %}}
アプリケーションと負荷生成器は実行したままにしておいてください。次のセクションでデュアルモードフラグを追加するために停止します。
{{% /notice %}}
