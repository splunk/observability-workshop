---
title: TBD
linkTitle: 4.4 TBD
weight: 4
time: 10 minutes
description: TBD
draft: true
---

これは置き場所が必要なコンテンツです:

TE エージェントからトレース有効化された ThousandEyes の **HTTP Server** または **API** テストで、以下の URL を使用します:

```text
http://api-gateway.default.svc.cluster.local:82/api/customer/owners
```

## トレースの存在を検証する

1. デプロイメントのロールアウトが完了するのを待ちます:

   ```bash
   kubectl rollout status deployment/api-gateway
   ```

2. PetClinic API gateway に対してリクエストを数回生成します:

   ```text
   http://api-gateway.default.svc.cluster.local:82/api/customer/owners
   ```

   このリクエストは PetClinic API gateway を経由して `customers-service` にルーティングされ、PetClinic データベースに対してクエリを実行します。単純なヘルスチェックよりも有用なトレースが生成されます。

3. 続行する前に、トレースが **Splunk APM** に到着していることを確認します。

{{% notice title="学習のヒント" style="info" %}}
トレース演習では、純粋な `/health` エンドポイントではなく、ビジネストランザクションを使用してください。複数サービスにまたがるリクエストの方が、ThousandEyes でのサービスマップが格段に充実し、Splunk APM でのトレースもより有用になります。
{{% /notice %}}

### Step 3: ThousandEyes テストで分散トレーシングを設定する

Step 1 のインストルメンテーション済みバックエンドエンドポイントを対象とした **API** テストを作成または編集します。

1. ThousandEyes で **Network&App Synthetics > Test Settings** に移動します。
2. **Add New Test** をクリックし、**API** を選択します。
3. URL を入力します（例: `http://api-gateway.default.svc.cluster.local:82/api/customer/owners`）。
4. テスト実行元: `Select your agent` を選択して **close** します。
5. 名前を `Your name - API` に設定します。
6. **API Performance (Optional)** で **Distributed Tracing** を有効にします。
7. **Next** をクリックします。
8. ステップ名を **Test Kubernetes** にし、URL を `http://api-gateway.default.svc.cluster.local:82/api/customer/owners` に設定します。
9. **Deploy** をクリックし、テスト結果を確認します。変更を加えなくてもテストを実行できます。

![Enable Distributed Tracing in ThousandEyes](../images/distributed-tracing-enable.png)

テスト実行後、ThousandEyes はトレースヘッダーを注入し、そのリクエストのトレースコンテキストをキャプチャします。

トレースが表示されるまでに時間がかかる場合があります。ThousandEyes のサービスマップに移動してトレース ID をコピーし、Observability Cloud で検索することができます。トレースはまだ進行中である可能性が高いでしょう。

### Step 4: 双方向の調査ループを検証する

テストが実行され、コネクタが有効になったら、両方向のワークフローを検証します。

### ThousandEyes から開始する

1. ThousandEyes でテストを開きます。
2. **Service Map** タブに移動します。
3. トレースパス、サービスのレイテンシ、ダウンストリームのエラーが確認できることを検証します。
4. ThousandEyes のリンクから **Splunk APM** へ移動し、完全なトレースを調査します。

![ThousandEyes Service Map with Splunk APM correlation](../images/thousandeyes-service-map.png)

#### Splunk APM で続行する

Splunk APM 内で、トレースに以下のような ThousandEyes メタデータが含まれていることを確認します:

- `thousandeyes.account.id`
- `thousandeyes.test.id`
- `thousandeyes.permalink`
- `thousandeyes.source.agent.id`

`thousandeyes.permalink` フィールド、またはトレースのウォーターフォールビューにある **Go to ThousandEyes test** ボタンを使って、元の ThousandEyes テストに戻ることができます。

![Splunk APM trace linked back to ThousandEyes](../images/splunk-apm-trace.png)

## 推奨される学習シナリオ

クラウドエージェントと自分の URL（例: `http://i-0cedf3429f9192aaa.splunk.show:81/#!/owners`、自分のインスタンスに置き換えてください）を使って、Web テストを作成してみてください。

## このセクションは再確認が必要

ワークショップでは以下のフローを使用します:

1. 複数のサービスを呼び出す内部 API ルートに対して ThousandEyes テストを作成します。
2. ThousandEyes に最初に問題を浮き上がらせ、ネットワークと合成監視の視点からクラスを開始します。
3. ThousandEyes で **Service Map** を開き、レイテンシまたはエラーの発生箇所を特定します。
4. **Splunk APM** に移動してスパンレベルの分析を行います。
5. **ThousandEyes** に戻り、テスト、エージェント、ネットワークパスを再度確認します。

これは異なるチームが実際に働いている方法を反映しているため、優れた教育ループとなります:

- ネットワークおよびエッジチームは ThousandEyes から始めることが多いです。
- SRE およびプラットフォームチームは Splunk のダッシュボードまたはアラートから始めることが多いです。
- アプリケーションチームは通常、Splunk APM でトレースを確認したいと考えます。

この統合があれば、誰もがコンテキストを失わずに視点を切り替えられます。

## よくある落とし穴

- テストが Splunk のダッシュボードに表示されているのに、トレースの相関が取れていないことがあります。これは通常、**メトリクス** ストリームのみが構成されており、**Splunk APM Generic Connector** が構成されていないことを意味します。
- Splunk APM にはトレースが存在するのに、監視対象のエンドポイントが下流にトレースヘッダーを伝播しない場合は、ThousandEyes には表示されないことがあります。
- `/health` のような浅いエンドポイントは、構成が正しい場合でもトレースの価値が限定的であることが多いです。

## 参考資料

- [ThousandEyes Distributed Tracing](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing)
- [ThousandEyes Distributed Tracing with Splunk Observability APM](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing/distributed-tracing-splunk-apm)
- [Splunk APM: View traces with Cisco ThousandEyes integration](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/view-and-filter-for-spans-within-a-trace)
- [Splunk OTel Collector zero-code instrumentation for Kubernetes language runtimes](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/automatic-discovery-of-apps-and-services/kubernetes/language-runtimes)
