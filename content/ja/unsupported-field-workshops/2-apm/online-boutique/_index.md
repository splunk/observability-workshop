---
title: 1. Online Boutique
weight: 1
description: Online Boutique アプリケーションが Kubernetes (K3s) にデプロイされていることを確認し、Load Generator (Locust) を使用して人工的なトラフィックを生成します。
time: 15 minutes
---

* {{% badge style="primary" icon=star title="" %}}**Ninja**{{% /badge %}} Online Boutique アプリケーションを Kubernetes にデプロイする
* アプリケーションが実行されていることを確認する
* Locust を使用して人工的なトラフィックを生成する
* UI で APM メトリクスを確認する

---

{{% expand title="{{% badge style=primary icon=star %}}**Ninja** - Online Boutique のデプロイ{{% /badge %}}" %}}

## 1. EC2 サーバーの確認

このワークショップモジュールは、IM ワークショップを実行した後に続けて実施し、EC2 インスタンスへのアクセスがまだ可能であることを前提としています。

その場合は、[**Online Boutique のデプロイ**](#2-deploy-online-boutique) に進んでください。新しいインスタンスを受け取った場合は、[**OTel Collector のデプロイ**](../../1-imt/gdi/) の最初の2つのセクションを実行してシステムを APM ワークショップ用に準備してから、次のセクションに進んでください。

## 2. Online Boutique のデプロイ

Online Boutique アプリケーションを K3s にデプロイするには、以下のデプロイメントを適用します

{{< tabs >}}
{{% tab title="Deploy Online Boutique" %}}

``` bash
cd ~/workshop/apm
kubectl apply -f deployment.yaml
```

{{% /tab %}}
{{% tab title="Deployment Output" %}}

``` text
APM Only Deployment
deployment.apps/recommendationservice created
service/recommendationservice created
deployment.apps/productcatalogservice created
service/productcatalogservice created
deployment.apps/cartservice created
service/cartservice created
deployment.apps/adservice created
service/adservice created
deployment.apps/paymentservice created
service/paymentservice created
deployment.apps/loadgenerator created
service/loadgenerator created
deployment.apps/shippingservice created
service/shippingservice created
deployment.apps/currencyservice created
service/currencyservice created
deployment.apps/redis-cart created
service/redis-cart created
deployment.apps/checkoutservice created
service/checkoutservice created
deployment.apps/frontend created
service/frontend created
service/frontend-external created
deployment.apps/emailservice created
service/emailservice created
deployment.apps/rum-loadgen-deployment created
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="変数が未設定というメッセージが表示された場合" style="warning" %}}
`kubectl delete -f deployment.yaml` を実行してデプロイメントを削除してください。

次に、ガイド/メッセージに記載されている通りに変数をエクスポートし、上記のデプロイメントスクリプトを再実行してください。
{{% /notice %}}

Online Boutique アプリケーションが実行されていることを確認するには

{{< tabs >}}
{{% tab title="Get Pods" %}}

``` bash
kubectl get pods
```

{{% /tab %}}
{{% tab title="Get Pods Output" %}}

``` text
NAME                                                       READY  STATUS  RESTARTS      AGE
splunk-otel-collector-k8s-cluster-receiver-849cf595bf-l7mnq 1/1   Running   0           31m
splunk-otel-collector-agent-pxrgp                           2/2   Running   0           31m
productcatalogservice-8464cd56d-n8f89                       1/1   Running   0            1m
redis-cart-bcf44df97-djv6z                                  1/1   Running   0            1m
checkoutservice-8558fd7b95-b9pn8                            1/1   Running   0            1m
shippingservice-7cc4bdd6f4-xsvnx                            1/1   Running   0            1m
recommendationservice-647d57fd44-l7tkq                      1/1   Running   0            1m
frontend-66c5d589d-55vzb                                    1/1   Running   0            1m
emailservice-6ff5bbd67d-pdcm2                               1/1   Running   0            1m
paymentservice-6866558995-8xmf2                             1/1   Running   0            1m
currencyservice-8668d75d6f-mr68h                            1/1   Running   0            1m
rum-loadgen-deployment-58ccf7bd8f-cr4pr                     1/1   Running   0            1m
rum-loadgen-deployment-58ccf7bd8f-qjr4b                     1/1   Running   0            1m
rum-loadgen-deployment-58ccf7bd8f-fvb4x                     1/1   Running   0            1m
cartservice-7b58c88c45-xvxhq                                1/1   Running   0            1m
loadgenerator-6bdc7b4857-9kxjd                              1/1   Running   2 (49s ago)  1m
adservice-7b68d5b969-89ft2                                  1/1   Running   0            1m
```

{{% /tab %}}
{{< /tabs >}}

{{% notice title="情報" style="info" %}}
通常、Pod が Running 状態に移行するまでに約1分30秒かかります。
{{% /notice %}}

{{% /expand %}}

## Online Boutique がデプロイされていることを確認する

Splunk UI で **Infrastructure** をクリックすると、Infrastructure Overview ダッシュボードが表示されます。次に **Kubernetes** をクリックしてください。

**Cluster** ドロップダウンを使用してクラスター名を選択すると、新しく起動した Pod とデプロイされたコンテナが表示されます。Splunk UI でクラスターをクリックすると、以下のような画面が表示されます

![Back to cluster](../images/online-boutique-k8s.png)

**WORKLOADS** タブを再度選択すると、いくつかの Deployments と ReplicaSets が表示されます

![Online Boutique loaded](../images/online-boutique-workload.png)

## Online Boutique にアクセスする

{{% expand title="{{% badge style=primary icon=star %}}**Ninja** - デプロイした Online Boutique にアクセスする{{% /badge %}}" %}}
{{% notice style="blue" %}}

Online Boutique は EC2 インスタンスの IP アドレスのポート 81 で表示できます。IP アドレスは、ワークショップの最初に SSH 接続する際に使用したものです。

Web ブラウザを開き、`http://<ec2-ip-address>:81/` にアクセスすると、Online Boutique が実行されているのを確認できます。
{{% /notice %}}
{{% /expand %}}

ワークショップのインストラクターが Online Boutique にアクセスするための URL を提供します。この URL をブラウザに入力すると、Online Boutique のホームページが表示されます。

![Online Boutique](../images/online-boutique.png)
