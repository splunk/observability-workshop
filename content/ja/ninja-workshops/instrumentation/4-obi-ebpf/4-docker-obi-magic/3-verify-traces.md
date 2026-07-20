---
title: 3. Splunkでトレースを確認する
weight: 3
---

## クイック検証

まず、すべてが正常に動作していることを確認します。

{{< tabs >}}
{{% tab title="スクリプト" %}}

``` bash
docker-compose ps
curl -s localhost:3000/create-order | jq
docker-compose logs obi | head -30
```

{{% /tab %}}
{{% tab title="期待される出力" %}}

``` text
# docker-compose ps - all 6 containers running
# curl - returns JSON order confirmation
# obi logs - shows "instrumenting process" for each service
```

{{% /tab %}}
{{< /tabs >}}

OBIのログで、以下のような行を確認します。

``` text
level=INFO msg="instrumenting process" cmd=/usr/local/bin/payment-service service=payment-service
level=INFO msg="instrumenting process" cmd=/usr/local/bin/order-processor service=order-processor
level=INFO msg="instrumenting process" cmd=node service=frontend
```

## Splunk APMを確認する

トレースが流れるまで30〜60秒待ってから、Splunk APMを確認します。

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: APMに移動し、お使いの環境でフィルタリングします。`frontend` -> `order-processor` -> `payment-service` の3つのサービスが表示されます。
2. **Traces**: 任意のトレースをクリックします。3つのサービスすべてにまたがる分散トレースが、各ホップのタイミングとともに表示されます。
3. **フェーズ1との比較**: 数分前には完全に空だったAPMダッシュボードに、完全なサービストポロジーが表示されるようになりました。

{{% /notice %}}

**composeファイルにコンテナを1つ追加しただけです。アプリケーションコードの変更は0行です。これで完全な分散トレーシングが実現しました。**

## 解答例

途中で行き詰まった場合、すべての変更が適用された最終的な `docker-compose.yaml` は以下で確認できます。

``` bash
cat ~/workshop/obi/02-obi-docker/docker-compose.final.yaml
```

お使いの `docker-compose.yaml` と比較して、差分を確認してください。

## Dockerのクリーンアップ

Kubernetesフェーズに進む前に、Dockerスタックを停止します。

``` bash
docker-compose down
```
