---
title: 3. AppD での実行と確認
weight: 3
---

AppDynamics エージェントをアタッチしてアプリケーションを実行します。これは「通常の」単一送信先へのインストルメンテーションです。

## AppDynamics エージェントで実行する

`<YOUR-ACCESS-KEY>` を前のステップで取得した AppDynamics トークンに置き換えてください:

{{< tabs >}}
{{% tab title="Command" %}}
環境変数をエクスポートします

```bash
export APPD_ACCESS_KEY=<Your-AppDynamics-access-key>
export APPD_APP_NAME=Dual-Ingest-${INSTANCE}
```

次に、エージェント付きで Java を起動します:

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
  -jar app/target/ingest-workshop-1.0.0.jar & 
```

{{% /tab %}}
{{% tab title="Example" %}}

```text
java -javaagent:agent/javaagent.jar \
  -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com \
  -Dappdynamics.controller.port=443 \
  -Dappdynamics.controller.ssl.enabled=true \
  -Dappdynamics.agent.applicationName=Dual-Ingest-shw-4267 \
  -Dappdynamics.agent.tierName=OrderService \
  -Dappdynamics.agent.nodeName=OrderService-Node \
  -Dappdynamics.agent.accountName=se-lab \
  -Dappdynamics.agent.accountAccessKey="hj9999999999" \
  -jar app/target/ingest-workshop-1.0.0.jar &
```

{{% /tab %}}
{{< /tabs >}}

Spring Boot の起動バナーが表示されるまで待ちます（約10〜15秒）。
Enter キーを押してプロンプトに戻ります。

## 負荷を生成する

バックグラウンドでシンプルな負荷生成ツールを起動します:

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## AppDynamics Controller で確認する

1. [AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/) を開きます
2. **Applications** に移動し、お使いのアプリケーションを見つけます（例: `Dual-Ingest-<your_INSTANCE_var>`）
3. アプリケーションをクリックして **Flow Map** を表示します

{{% notice title="お待ちください" style="info" icon="info-circle" %}}
アプリケーションが登録され、ビジネストランザクションがフローマップに表示されるまで2〜5分かかる場合があります。必要に応じてページを更新してください。
{{% /notice %}}

以下が表示されるはずです:

- フローマップ内の **OrderService** ティア
- `/order` および `/inventory` エンドポイントのビジネストランザクション
- コントローラーに流入するメトリクスデータ

この時点では、データは **AppDynamics にのみ** 送信されています。アプリケーションは Splunk Observability Cloud に接続されていません。次のフェーズでは、デュアルシグナルモードを有効にしてこれを変更します。
![AppDynamics Application](../../_images/appd-service.png?width=30vw)

{{% notice title="実行を継続してください" style="warning" icon="exclamation-triangle" %}}
アプリケーションと負荷生成ツールは実行したままにしてください。次のセクションでデュアルモードフラグを追加するために停止します。
{{% /notice %}}
