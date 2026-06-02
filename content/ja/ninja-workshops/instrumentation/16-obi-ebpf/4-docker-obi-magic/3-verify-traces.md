---
title: 3. Splunk でトレースを確認する
weight: 3
---

## クイック検証

まず、すべてが正常に動作していることを確認します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker-compose ps
curl -s localhost:3000/create-order | jq
docker-compose logs obi | head -30
```

{{% /tab %}}
{{% tab title="Expected" %}}

``` text
# docker-compose ps - all 6 containers running
# curl - returns JSON order confirmation
# obi logs - shows "instrumenting process" for each service
```

{{% /tab %}}
{{< /tabs >}}

OBI のログで、次のような行を探してください。

``` text
level=INFO msg="instrumenting process" cmd=/usr/local/bin/payment-service service=payment-service
level=INFO msg="instrumenting process" cmd=/usr/local/bin/order-processor service=order-processor
level=INFO msg="instrumenting process" cmd=node service=frontend
```

## Splunk APM を確認する

トレースが流れ始めるまで 30〜60 秒待ってから、Splunk APM を確認します。

{{% notice title="演習" style="green" icon="running" %}}

1. **Service Map**: APM に移動し、環境でフィルタリングします。`frontend` -> `order-processor` -> `payment-service` の 3 つのサービスが表示されるはずです。
2. **Traces**: 任意のトレースをクリックします。3 つのサービスすべてにわたる完全な分散トレースと、各ホップのタイミングが表示されます。
3. **フェーズ 1 との比較**: 数分前まで完全に空だった APM ダッシュボードに、完全なサービストポロジーが表示されるようになりました。

{{% /notice %}}

**Compose ファイルに 1 つのコンテナを追加しただけです。アプリケーションコードは 1 行も変更していません。それでも、完全な分散トレーシングが利用できるようになりました。**

## 解答例

途中でつまずいた場合は、すべての変更が適用された最終版の `docker-compose.yaml` が次の場所に用意されています。

``` bash
cat ~/workshop/obi/02-obi-docker/docker-compose.final.yaml
```

ご自身の `docker-compose.yaml` と比較して、相違点を確認してください。

## Docker のクリーンアップ

Kubernetes フェーズに進む前に、Docker スタックを停止します。

``` bash
docker-compose down
```
