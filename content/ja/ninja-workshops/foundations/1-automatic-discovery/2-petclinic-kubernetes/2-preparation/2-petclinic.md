---
title: Deploy the PetClinic Application
linkTitle: 2. Deploy PetClinic Application
weight: 3
---

アプリケーションの最初のデプロイでは、事前にビルドされたコンテナを使用して、観測対象としたい Kubernetes 上で動作する一般的な Java マイクロサービスベースのアプリケーションというベースシナリオを構築します。それでは、アプリケーションをデプロイしましょう。

{{< tabs >}}
{{% tab title="kubectl apply" %}}

``` bash
kubectl apply -f ~/workshop/petclinic/deployment.yaml
```

{{% /tab %}}
{{% tab title="Output" %}}

``` text
deployment.apps/config-server created
service/config-server created
deployment.apps/discovery-server created
service/discovery-server created
deployment.apps/api-gateway created
service/api-gateway created
service/api-gateway-external created
deployment.apps/customers-service created
service/customers-service created
deployment.apps/vets-service created
service/vets-service created
deployment.apps/visits-service created
service/visits-service created
deployment.apps/admin-server created
service/admin-server created
service/petclinic-db created
deployment.apps/petclinic-db created
configmap/petclinic-db-initdb-config created
deployment.apps/petclinic-loadgen-deployment created
configmap/scriptfile created
```

{{% /tab %}}
{{< /tabs >}}

ここで、Pod が動作していることを確認することで、デプロイが成功したかを検証できます。コンテナはダウンロードして起動する必要があるため、数分かかる場合があります。

{{< tabs >}}
{{% tab title="kubectl get pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Output" %}}

```bash
NAME                                                            READY   STATUS    RESTARTS   AGE
splunk-otel-collector-k8s-cluster-receiver-655dcd9b6b-dcvkb     1/1     Running   0          114s
splunk-otel-collector-agent-dg2vj                               1/1     Running   0          114s
splunk-otel-collector-operator-57cbb8d7b4-dk5wf                 2/2     Running   0          114s
petclinic-db-64d998bb66-2vzpn                                   1/1     Running   0          58s
api-gateway-d88bc765-jd5lg                                      1/1     Running   0          58s
visits-service-7f97b6c579-bh9zj                                 1/1     Running   0          58s
admin-server-76d8b956c5-mb2zv                                   1/1     Running   0          58s
customers-service-847db99f79-mzlg2                              1/1     Running   0          58s
vets-service-7bdcd7dd6d-2tcfd                                   1/1     Running   0          58s
petclinic-loadgen-deployment-5d69d7f4dd-xxkn4                   1/1     Running   0          58s
config-server-67f7876d48-qrsr5                                  1/1     Running   0          58s
discovery-server-554b45cfb-bqhgt                                1/1     Running   0          58s
```

{{% /tab %}}
{{< /tabs >}}

`kubectl get pods` の出力が、上記の Output タブに表示されている出力と一致することを確認してください。すべてのサービスが **Running** と表示されていることを確認します（または `k9s` を使用してステータスを継続的に監視します）。

アプリケーションをテストするには、インスタンスのパブリック IP アドレスを取得する必要があります。次のコマンドを実行して取得できます。

``` bash
curl http://ifconfig.me

```

**http://<IP_ADDRESS>:81** にアクセスして、アプリケーションが動作しているかを確認します（**<IP_ADDRESS>** は上記で取得した IP アドレスに置き換えてください）。PetClinic アプリケーションが動作しているはずです。ポート **81** に到達できない場合や、別のポートを使用したい場合は、ポート **80** および **443** でも動作しています。

![Pet shop](../../images/petclinic.png)

**All Owners** **(1)** および **Veterinarians** **(2)** タブにアクセスして、それぞれのページに名前のリストが表示されることを確認し、アプリケーションが正しく動作していることを確かめてください。

![Owners](../../images/petclinic-owners.png)

<!--
Once they are all running, the application will take a few minutes to fully start up, create the database and synchronize all the services, so let's use the time to check the local private repository is active.

#### Verify the local Private Registry

Later on, when we test our **automatic discovery and configuration** we are going to build new containers to highlight some of the additional features of Splunk Observability Cloud.

As configuration files and source code will be changed, the containers will need to be built and stored in a local private registry (which has already been enabled for you).

To check if the private registry is avaiable, run the following command (this will return an empty list):

{{< tabs >}}
{{% tab title="Check the local Private Registry" %}}

``` bash
curl -X GET http://localhost:9999/v2/_catalog
```

{{% /tab %}}
{{% tab title="Output" %}}

```text
**{"repositories":[]}**
```

{{% /tab %}}
{{< /tabs >}}
-->
