---
title: OpenTelemetry Demo のデプロイ
linkTitle: 1. Deploy OpenTelemetry Demo
weight: 1
---

## 1. namespace の作成

他のワークショップと競合しないように、OpenTelemetry Demo を `otel-demo` という別の namespace にデプロイします。namespace を作成するには、以下のコマンドを実行します

``` bash
kubectl create namespace otel-demo
```

## 2. OpenTelemetry Demo のデプロイ

次に、OpenTelemetry Demo アプリケーションが含まれるディレクトリに移動します

``` bash
cd ~/workshop/apm
```

OpenTelemetry Demo アプリケーションをデプロイします

{{% tabs %}}
{{% tab title="Command" %}}

``` bash
kubectl apply -n otel-demo -f otel-demo.yaml
```

{{% /tab %}}
{{% tab title="Output" %}}

``` text
serviceaccount/opentelemetry-demo created
service/opentelemetry-demo-adservice created
service/opentelemetry-demo-cartservice created
service/opentelemetry-demo-checkoutservice created
service/opentelemetry-demo-currencyservice created
service/opentelemetry-demo-emailservice created
service/opentelemetry-demo-featureflagservice created
service/opentelemetry-demo-ffspostgres created
service/opentelemetry-demo-frontend created
service/opentelemetry-demo-kafka created
service/opentelemetry-demo-loadgenerator created
service/opentelemetry-demo-paymentservice created
service/opentelemetry-demo-productcatalogservice created
service/opentelemetry-demo-quoteservice created
service/opentelemetry-demo-recommendationservice created
service/opentelemetry-demo-redis created
service/opentelemetry-demo-shippingservice created
deployment.apps/opentelemetry-demo-accountingservice created
deployment.apps/opentelemetry-demo-adservice created
deployment.apps/opentelemetry-demo-cartservice created
deployment.apps/opentelemetry-demo-checkoutservice created
deployment.apps/opentelemetry-demo-currencyservice created
deployment.apps/opentelemetry-demo-emailservice created
deployment.apps/opentelemetry-demo-featureflagservice created
deployment.apps/opentelemetry-demo-ffspostgres created
deployment.apps/opentelemetry-demo-frauddetectionservice created
deployment.apps/opentelemetry-demo-frontend created
deployment.apps/opentelemetry-demo-kafka created
deployment.apps/opentelemetry-demo-loadgenerator created
deployment.apps/opentelemetry-demo-paymentservice created
deployment.apps/opentelemetry-demo-productcatalogservice created
deployment.apps/opentelemetry-demo-quoteservice created
deployment.apps/opentelemetry-demo-recommendationservice created
deployment.apps/opentelemetry-demo-redis created
deployment.apps/opentelemetry-demo-shippingservice created
```

{{% /tab %}}
{{% /tabs %}}

アプリケーションがデプロイされたら、Pod が `Running` 状態になるまで待つ必要があります。Pod のステータスを確認するには、以下のコマンドを実行します

{{% tabs %}}
{{% tab title="Command" %}}

``` bash
kubectl get pods -n otel-demo
```

{{% /tab %}}
{{% tab title="Output" %}}

``` text
NAME                                                        READY   STATUS    RESTARTS   AGE
opentelemetry-demo-emailservice-847d6fb577-bxll6            1/1     Running   0          40s
opentelemetry-demo-ffspostgres-55f65465dd-2gsj4             1/1     Running   0          40s
opentelemetry-demo-adservice-5b7c68859d-5hx5f               1/1     Running   0          40s
opentelemetry-demo-currencyservice-c4cb78446-qsd68          1/1     Running   0          40s
opentelemetry-demo-frontend-5d7cdb8786-5dl76                1/1     Running   0          39s
opentelemetry-demo-kafka-79868d56d8-62wsd                   1/1     Running   0          39s
opentelemetry-demo-paymentservice-5cb4ccc47c-65hxl          1/1     Running   0          39s
opentelemetry-demo-productcatalogservice-59d955f9d6-xtnjr   1/1     Running   0          38s
opentelemetry-demo-loadgenerator-755d6cd5b-r5lqs            1/1     Running   0          39s
opentelemetry-demo-quoteservice-5fbfb97778-vm62m            1/1     Running   0          38s
opentelemetry-demo-redis-57c49b7b5b-b2klr                   1/1     Running   0          37s
opentelemetry-demo-shippingservice-6667f69f78-cwj8q         1/1     Running   0          37s
opentelemetry-demo-recommendationservice-749f55f9b6-5k4lc   1/1     Running   0          37s
opentelemetry-demo-featureflagservice-67677647c-85xtm       1/1     Running   0          40s
opentelemetry-demo-checkoutservice-5474bf74b8-2nmns         1/1     Running   0          40s
opentelemetry-demo-frauddetectionservice-77fd69d967-lnjcg   1/1     Running   0          39s
opentelemetry-demo-accountingservice-96d44cfbc-vmtzb        1/1     Running   0          40s
opentelemetry-demo-cartservice-7c4f59bdd5-rfkf4             1/1     Running   0          40s
```

{{% /tab %}}
{{% /tabs %}}

## 3. アプリケーションの動作確認

アプリケーションが動作していることを確認するために、frontend サービスをポートフォワードします。以下のコマンドを実行します

``` bash
kubectl port-forward svc/opentelemetry-demo-frontend 8083:8080 -n otel-demo --address='0.0.0.0'
```

実行しているインスタンスの**パブリック IP アドレス**を取得します。以下のコマンドを実行して取得できます

``` bash
curl ifconfig.me
```

ポートフォワードが実行されたら、ブラウザを開いて `http://<public IP address>:8083` にアクセスすることでアプリケーションにアクセスできます。以下のように表示されるはずです

![OpenTelemetry Demo](../images/otel-demo.png)

アプリケーションが動作していることを確認できたら、`ctrl + c` を押してポートフォワードを終了します。

次に、**OpenTelemetry Collector** をデプロイします。
