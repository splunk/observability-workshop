---
title: 3. Splunk でトレースを確認する
weight: 3
---

## クイック検証

まず、すべてが正常に動作していることを確認します：

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
docker-compose ps
curl -s localhost:3000/create-order | python3 -m json.tool
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

OBIのログで、次のような行を探してください：

``` text
level=INFO msg="instrumenting process" cmd=/usr/local/bin/payment-service service=payment-service
level=INFO msg="instrumenting process" cmd=/usr/local/bin/order-processor service=order-processor
level=INFO msg="instrumenting process" cmd=node service=frontend
```

## Splunk APM を確認する

トレースが流れるまで30〜60秒待ってから、Splunk APMを確認します。

{{% notice title="Exercise" style="green" icon="running" %}}

1. **Service Map**: APMに移動し、ご自身の環境でフィルタリングします。3つのサービスが表示されるはずです: `frontend` -> `order-processor` -> `payment-service`。
2. **Traces**: 任意のトレースをクリックします。3つのサービスすべてにまたがる完全な分散トレースと、各ホップのタイミングが表示されます。
3. **フェーズ 1 との比較**: 数分前は完全に空だったAPMダッシュボードに、完全なサービストポロジーが表示されるようになりました。

{{% /notice %}}

**compose ファイルにコンテナを 1 つ追加しただけです。アプリケーションコードは 1 行も変更していません。これで完全な分散トレーシングが実現しました。**

## 解答

途中で詰まった場合は、すべての変更が適用された最終的な `docker-compose.yaml` を以下で確認できます：

``` bash
cat ~/workshop/obi/02-obi-docker/docker-compose.final.yaml
```

ご自身の `docker-compose.yaml` と比較して、違いを確認してください。

## Docker のクリーンアップ

Kubernetesフェーズに進む前に、Dockerスタックを停止します：

``` bash
docker-compose down
```
