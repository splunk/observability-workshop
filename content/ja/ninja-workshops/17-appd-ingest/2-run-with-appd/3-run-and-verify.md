---
title: 3. AppD で実行と確認
weight: 3
---

ここで、AppDynamics エージェントをアタッチした状態でアプリケーションを実行します。これは「通常の」単一送信先のインストルメンテーションです。

## AppDynamics エージェントを使った実行

`<YOUR-ACCESS-KEY>` を、前のステップで取得した AppDynamics トークンに置き換えます。

{{< tabs >}}
{{% tab title="コマンド" %}}
環境変数をエクスポートします。

```bash
export APPD_ACCESS_KEY=<Your-AppDynamics-access-key>
export APPD_APP_NAME=Dual-Ingest-${INSTANCE}
```

その後、エージェント付きで Java を起動できます。

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

Spring Boot の起動バナーが表示されるまで待ちます（10〜15秒程度）。

## 負荷を生成する

バックグラウンドでシンプルなロードジェネレーターを開始します。

```bash
while true; do
  curl -s localhost:8080/order > /dev/null
  curl -s localhost:8080/inventory > /dev/null
  sleep 2
done &
```

## AppDynamics Controller で確認する

1. [AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/) を開きます
2. **Applications** に移動し、自分のアプリケーション（例: `Dual-Ingest-<your_INSTANCE_var>`）を見つけます
3. アプリケーションをクリックして **Flow Map** を表示します

{{% notice title="少しお待ちください" style="info" icon="info-circle" %}}
アプリケーションが登録され、ビジネストランザクションが flow map に表示されるまで、2〜5分かかる場合があります。必要に応じてページを更新してください。
{{% /notice %}}

次の内容が表示されるはずです。

- flow map に表示される **OrderService** tier
- `/order` および `/inventory` エンドポイントのビジネストランザクション
- コントローラーに流れているメトリクスデータ

この時点では、データは **AppDynamics のみ**に流れています。アプリケーションは Splunk Observability Cloud には接続されていません。次のフェーズで、デュアルシグナルモードを有効にしてこれを変更します。
![AppDynamics Application](../../_images/appd-service.png?width=30vw)

{{% notice title="実行したままにしておいてください" style="warning" icon="exclamation-triangle" %}}
アプリケーションとロードジェネレーターは実行したままにしておきます。次のセクションで、デュアルモードのフラグを追加するために停止します。
{{% /notice %}}
