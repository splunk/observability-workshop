---
title: Application
linkTitle: 2.3 Application
weight: 3
time: 10 minutes
description: アプリケーションをデプロイする
---

このステップでは、サンプルアプリケーション (Pet Clinic) をデプロイします。

## インストール手順

### Step 1: アプリケーションをデプロイする

アプリケーションをデプロイするには、次のコマンドを実行します。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl apply -f ~/workshop/petclinic/deployment.yaml
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
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
ingress.networking.k8s.io/api-gateway-ingress created
deployment.apps/petclinic-loadgen-deployment created
configmap/scriptfile created
```

{{% /tab %}}
{{< /tabs >}}

アプリケーションが他の Pod とともにデプロイされていることを確認できます。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
NAME                                                        READY   STATUS    RESTARTS   AGE
admin-server-54b4d6f54-sfnsz                                1/1     Running   0          4m
api-gateway-c78dc6695-mxg6d                                 1/1     Running   0          4m
config-server-5cc585ff59-b6dvv                              1/1     Running   0          4m
customers-service-7d6575b99c-8sx9l                          1/1     Running   0          4m
discovery-server-796f6c4dc-8fkss                            1/1     Running   0          4m
petclinic-db-dfb77856f-zcl4s                                1/1     Running   0          4m
petclinic-loadgen-deployment-7c8f6bd8f5-ms5xk               1/1     Running   0          4m
splunk-otel-collector-agent-2dn2t                           1/1     Running   0          9m
splunk-otel-collector-agent-7vrdr                           1/1     Running   0          9m
splunk-otel-collector-agent-hcg9p                           1/1     Running   0          9m
splunk-otel-collector-k8s-cluster-receiver-8d89b497-cqn8x   1/1     Running   0          9m
splunk-otel-collector-operator-78b94dddd7-ctpw6             2/2     Running   0          9m
thousandeyes-746b4d894b-rxb55                               1/1     Running   0          11m
vets-service-5bfb88c5f8-69zwl                               1/1     Running   0          4m
visits-service-5966f7b74f-hrch9                             1/1     Running   0          4m
```

{{% /tab %}}
{{< /tabs >}}

### Step 2: アプリケーションが外部からアクセス可能であることを確認する

アプリケーションをテストするには、インスタンスのパブリック IP アドレスを取得する必要があります。次のコマンドを実行することで取得できます。
{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl http://ifconfig.me
```

{{% /tab %}}
{{% tab title="IP ADDRESS" %}}

```text
32.157.204.101
```

{{% /tab %}}
{{< /tabs >}}

**http://<IP_ADDRESS>:81** にアクセスして、アプリケーションが動作していることを確認してください (**<IP_ADDRESS>** は、上記で取得した IP アドレスに置き換えてください)。PetClinic アプリケーションが動作している様子が表示されるはずです。ポート **81** にアクセスできない場合や、別のポートを使用したい場合は、ポート **80** および **443** でもアプリケーションが稼働しています。

![Pet shop](../../images/petclinic.png?width=45vw)

**All Owners** **(1)** タブと **Veterinarians** **(2)** タブにアクセスし、各ページに名前のリストが表示されることを確認して、アプリケーションが正しく動作していることを確かめてください。

![Owners](../../images/petclinic-owners.png?width=45vw)

{{% notice title="Success" style="success" icon="check" %}}
アプリケーションが外部から確認できれば、次のステップに進む準備が整っています。
{{% /notice %}}
