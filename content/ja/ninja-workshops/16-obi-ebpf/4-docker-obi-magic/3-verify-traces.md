---
title: 3. Splunk でトレースを確認する
weight: 3
---

## クイック検証

まず、すべてが正常に動作していることを確認します:

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

OBI のログで、以下のような行を探してください:

``` text
level=INFO msg="instrumenting process" cmd=/usr/local/bin/payment-service service=payment-service
level=INFO msg="instrumenting process" cmd=/usr/local/bin/order-processor service=order-processor
level=INFO msg="instrumenting process" cmd=node service=frontend
```

## Splunk APM の確認

トレースが流れるまで 30〜60 秒待ってから、Splunk APM を確認します。

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: APM に移動し、ご自身の環境でフィルタリングします。`frontend` -> `order-processor` -> `payment-service` の3つのサービスが表示されるはずです。
2. **Traces**: 任意のトレースをクリックします。3つのサービスすべてにまたがる分散トレースが、各ホップのタイミングとともに表示されます。
3. **Phase 1 との比較**: 数分前には完全に空だった APM ダッシュボードに、完全なサービストポロジーが表示されるようになりました。

{{% /notice %}}

**compose ファイルにコンテナを1つ追加しただけです。アプリケーションコードの変更はゼロ行です。これで完全な分散トレーシングが実現しました。**

## 解答例

途中で行き詰まった場合、すべての変更が適用された最終版の `docker-compose.yaml` は以下で確認できます:

``` bash
cat ~/workshop/obi/02-obi-docker/docker-compose.final.yaml
```

ご自身の `docker-compose.yaml` と比較して、差分を確認してください。

## Docker のクリーンアップ

Kubernetes フェーズに進む前に、Docker スタックを停止します:

``` bash
docker-compose down
```
