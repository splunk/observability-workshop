---
title: 3. AppDでの実行と確認
weight: 3
---

AppDynamicsエージェントをアタッチしてアプリケーションを実行します。これは「通常の」単一送信先への計装です。

## AppDynamicsエージェントでの実行

`<YOUR-ACCESS-KEY>` を前のステップで取得したAppDynamicsトークンに置き換えます。

{{< tabs >}}
{{% tab title="コマンド" %}}
環境変数をエクスポートします

```bash
export APPD_ACCESS_KEY=<Your-AppDynamics-access-key>
```

および

```bash
export APPD_APP_NAME=Dual-Ingest-${INSTANCE}
```

次に、エージェント付きでJavaを起動します

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
{{% tab title="例" %}}

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

Spring Bootの起動バナーが表示されるまで待ちます（約10〜15秒）。
Enterキーを押してプロンプトに戻ります。

## 負荷の生成

バックグラウンドでシンプルな負荷生成ツールを起動します

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## AppDynamics Controllerでの確認

1. [AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/)を開きます
2. **Applications** に移動し、自分のアプリケーションを見つけます（例: `Dual-Ingest-<your_INSTANCE_var>`）
3. アプリケーションをクリックして **Flow Map** を表示します

{{% notice title="少々お待ちください" style="info" icon="info-circle" %}}
アプリケーションが登録され、ビジネストランザクションがFlow Mapに表示されるまで2〜5分かかる場合があります。必要に応じてページを更新してください。
{{% /notice %}}

以下が表示されます

- Flow Mapに **OrderService** ティアが表示される
- `/order` および `/inventory` エンドポイントのビジネストランザクション
- コントローラーに流入するメトリクスデータ

この時点では、データは **AppDynamicsのみ** に送信されています。アプリケーションはSplunk Observability Cloudに接続されていません。次のフェーズでは、デュアルシグナルモードを有効にしてこれを変更します。
![AppDynamics Application](../../_images/appd-service.png?width=30vw)

{{% notice title="実行を継続してください" style="warning" icon="exclamation-triangle" %}}
アプリケーションと負荷生成ツールは実行したままにしてください。次のセクションでデュアルモードフラグを追加するために停止します。
{{% /notice %}}
