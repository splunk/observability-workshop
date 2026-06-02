---
title: 3. アプリケーション負荷の生成
weight: 3
description: このセクションでは、サンプルアプリケーションをインストールし、負荷生成を開始します
---
このエクササイズでは、以下のアクションを実行します。

* サンプルアプリが実行されていることを確認します。
* サンプルアプリケーション向けの負荷生成を開始します。
* Controller でトランザクション負荷を確認します。

## サンプルアプリケーションが実行されていることを確認する

サンプルアプリケーションのホームページは、以下の形式の URL でウェブブラウザからアクセスできます。EC2 インスタンスの IP アドレスに置き換えて、その URL をブラウザのアドレスバーに入力してください。

```bash
http://[ec2-ip-address]:8080/Supercar-Trader/home.do
```

Supercar Trader アプリケーションのホームページが表示されるはずです。
![Supercar Trade Home Page](images/SuperCarHomePage-rz.png)

## 負荷生成を開始する

EC2 インスタンスに SSH 接続し、負荷生成を開始します。すべてのスクリプトの実行には数分かかる場合があります。

{{< tabs >}}
{{% tab title="Command" %}}

``` bash
cd /opt/appdynamics/lab-artifacts/phantomjs
./start_load.sh
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Cleaning up artifacts from previous load...
Starting home-init-01
Waiting for additional JVMs to initialize... 1
Waiting for additional JVMs to initialize... 2
Waiting for additional JVMs to initialize... 3
Waiting for additional JVMs to initialize... 4
Waiting for additional JVMs to initialize... 5
Waiting for additional JVMs to initialize... 6
Waiting for additional JVMs to initialize... 7
Waiting for additional JVMs to initialize... 8
Waiting for additional JVMs to initialize... 9
Waiting for additional JVMs to initialize... 10
Waiting for additional JVMs to initialize... 11
Waiting for additional JVMs to initialize... 12
Waiting for additional JVMs to initialize... 13
Waiting for additional JVMs to initialize... 14
Waiting for additional JVMs to initialize... 15
Waiting for additional JVMs to initialize... 16
Waiting for additional JVMs to initialize... 17
Waiting for additional JVMs to initialize... 18
Waiting for additional JVMs to initialize... 19
Waiting for additional JVMs to initialize... 20
Starting slow-query-01
Starting slow-query-02
Starting slow-query-03
Starting slow-query-04
Starting sessions-01
Starting sessions-02
Starting sell-car-01
Starting sell-car-02
Starting sessions-03
Starting sessions-04
Starting search-01
Starting request-error-01
Starting mem-leak-insurance
Finished starting load generator scripts                                                                100%   22MB 255.5KB/s   01:26
```

{{% /tab %}}
{{< /tabs >}}

## Controller でトランザクション負荷を確認する

Getting Started Wizard をウェブブラウザで開いたままにしている場合、エージェントが接続され、Controller がデータを受信していることが確認できるはずです。

![Agent Connected](images/agent_connected.png)

**Continue** をクリックすると、**Application Flow Map** に移動します（以下の Flow Map の画像までスキップしても構いません）。

Controller のブラウザウィンドウを既に閉じている場合は、Controller に再度ログインしてください。

1. Overview ページ（ランディングページ）から、左側のナビゲーションパネルにある **Applications** タブをクリックします。

    ![Controller Overview Page](images/ControllerOverviewPage.png)

2. **Applications** ページ内で、アプリケーションを手動で検索するか、右上の検索バーを使って検索を絞り込むことができます。

    ![Applications Search](images/ApplicationsSearch.png)

アプリケーション名をクリックすると、**Application Flow Map** に移動します。12 分後にすべてのアプリケーションコンポーネントが表示されるはずです。

12 分経ってもすべてのアプリケーションコンポーネントが表示されない場合は、もう少し待ってからブラウザのタブを更新してみてください。

![FlowMap](images/SuperCarTrader_FlowMap-rz.png)  

エージェントのダウンロード手順では、Tomcat サーバー用に Tier 名と Node 名を割り当てました。

``` bash
<tier-name>Web-Portal</tier-name>
<node-name>Web-Portal_Node-01</node-name>
```

他の 4 つのサービスにどのように Tier 名と Node 名が割り当てられたのか疑問に思うかもしれません。サンプルアプリケーションは、最初の Tomcat JVM から 4 つの追加の JVM を動的に作成し、4 つの各サービス向けに Tier 名と Node 名を JVM 起動コマンドの -D プロパティとして渡すことで割り当てます。JVM 起動コマンドラインに含まれる -D プロパティは、Java エージェントの ```controller-info.xml``` ファイルで定義されたプロパティよりも優先されます。

動的に起動された 4 つの各サービスに使用された JVM 起動パラメータを確認するには、EC2 インスタンスのターミナルウィンドウで以下のコマンドを実行してください。
  
{{< tabs >}}
{{% tab title="Command" %}}

``` bash
ps -ef | grep appdynamics.agent.tierName
```

{{% /tab %}}
{{% tab title="Loadgen Output" %}}

``` bash
splunk     47131   46757  3 15:34 pts/1    00:08:17 /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -javaagent:/opt/appdynamics/javaagent/javaagent.jar -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com -Dappdynamics.controller.port=443 -Dappdynamics.controller.ssl.enabled=true -Dappdynamics.agent.applicationName=Supercar-Trader-AppD-Workshop -Dappdynamics.agent.tierName=Api-Services -Dappdynamics.agent.nodeName=Api-Services_Node-01 -Dappdynamics.agent.accountName=se-lab -Dappdynamics.agent.accountAccessKey=hj6a4d7h2cuq -Xms64m -Xmx512m -XX:MaxPermSize=256m supercars.services.api.ApiService
splunk     47133   46757  2 15:34 pts/1    00:08:11 /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -javaagent:/opt/appdynamics/javaagent/javaagent.jar -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com -Dappdynamics.controller.port=443 -Dappdynamics.controller.ssl.enabled=true -Dappdynamics.agent.applicationName=Supercar-Trader-AppD-Workshop -Dappdynamics.agent.tierName=Inventory-Services -Dappdynamics.agent.nodeName=Inventory-Services_Node-01 -Dappdynamics.agent.accountName=se-lab -Dappdynamics.agent.accountAccessKey=hj6a4d7h2cuq -Xms64m -Xmx512m -XX:MaxPermSize=256m supercars.services.inventory.InventoryService
splunk     47151   46757  1 15:34 pts/1    00:04:58 /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -javaagent:/opt/appdynamics/javaagent/javaagent.jar -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com -Dappdynamics.controller.port=443 -Dappdynamics.controller.ssl.enabled=true -Dappdynamics.agent.applicationName=Supercar-Trader-AppD-Workshop -Dappdynamics.agent.tierName=Insurance-Services -Dappdynamics.agent.nodeName=Insurance-Services_Node-01 -Dappdynamics.agent.accountName=se-lab -Dappdynamics.agent.accountAccessKey=hj6a4d7h2cuq -Xms64m -Xmx68m -XX:MaxPermSize=256m supercars.services.insurance.InsuranceService
splunk     47153   46757  3 15:34 pts/1    00:08:17 /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -javaagent:/opt/appdynamics/javaagent/javaagent.jar -Dappdynamics.controller.hostName=se-lab.saas.appdynamics.com -Dappdynamics.controller.port=443 -Dappdynamics.controller.ssl.enabled=true -Dappdynamics.agent.applicationName=Supercar-Trader-AppD-Workshop -Dappdynamics.agent.tierName=Enquiry-Services -Dappdynamics.agent.nodeName=Enquiry-Services_Node-01 -Dappdynamics.agent.accountName=se-lab -Dappdynamics.agent.accountAccessKey=hj6a4d7h2cuq -Xms64m -Xmx512m -XX:MaxPermSize=256m supercars.services.enquiry.EnquiryService
splunk    144789   46722  0 20:09 pts/1    00:00:00 grep --color=auto appdynamics.agent.tierName
```

{{% /tab %}}
{{< /tabs >}}
  
すべてのコンポーネントがフローマップに表示されると、Insurance-Services Tier から呼び出されている 3 つの HTTP バックエンドを表す HTTP クラウドアイコンが見えるはずです。

以下の手順に従って、3 つの HTTP バックエンドのグループを解除します。

1. 「3 HTTP backends」とラベル付けされた HTTP クラウドアイコンを右クリックします
2. ドロップダウンメニューから「Ungroup Backends」を選択します

![Ungroup Http](images/ungroup-http-rz.png)
  
HTTP バックエンドのグループが解除されると、以下の画像のように 3 つの HTTP バックエンドがすべて表示されるはずです。

![Ungroup flow](images/ungrouped_flow-rz.png)
