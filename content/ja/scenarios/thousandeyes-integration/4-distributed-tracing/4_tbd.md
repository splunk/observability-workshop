---
title: TBD
linkTitle: 4.4 TBD
weight: 4
time: 10 minutes
description: TBD
draft: true
---

以下は整理が必要なコンテンツです

TE エージェントからのトレース対応 ThousandEyes **HTTP Server** または **API** テストに、この URL を使用します

```text
http://api-gateway.default.svc.cluster.local:82/api/customer/owners
```

### トレースの存在を確認する

1. デプロイメントのロールアウトが完了するまで待ちます

   ```bash
   kubectl rollout status deployment/api-gateway
   ```

2. PetClinic API ゲートウェイに対していくつかのリクエストを生成します

   ```text
   http://api-gateway.default.svc.cluster.local:82/api/customer/owners
   ```

   このリクエストは PetClinic API ゲートウェイを通過し、`customers-service` にルーティングされ、PetClinic データベースにクエリを実行します。単純なヘルスチェックよりも有用なトレースが生成されます。

3. 続行する前に、**Splunk APM** にトレースが到着していることを確認します。

{{% notice title="学習のヒント" style="info" %}}
トレーシング演習には、純粋な `/health` エンドポイントではなく、ビジネストランザクションを使用してください。マルチサービスリクエストを使用すると、ThousandEyes ではるかに優れた Service Map が得られ、Splunk APM ではより有用なトレースが得られます。
{{% /notice %}}

### ステップ 3: ThousandEyes テストで Distributed Tracing を設定する

ステップ 1 でインストルメントしたバックエンドエンドポイントをターゲットとする **API** テストを作成または編集します。

1. ThousandEyes で、**Network&App Synthetics > Test Settings** に移動します。
2. **Add New Test** をクリックし、**API** を選択します。
3. URL を入力します（例`http://api-gateway.default.svc.cluster.local:82/api/customer/owners`）
4. テストの実行元`Select your agent` を選択し、**close** をクリックします。
5. 名前を `Your name - API` に設定します。
6. **API Performance (Optional)** の下で、**Distributed Tracing** を有効にします。
7. **Next** をクリックします。
8. ステップ名を **Test Kubernetes** とし、URL を `http://api-gateway.default.svc.cluster.local:82/api/customer/owners` に設定します。
9. **Deploy** をクリックし、テスト結果を確認します。変更なしでテストを実行できます。

![ThousandEyes で Distributed Tracing を有効にする](../images/distributed-tracing-enable.png)

テストが実行されると、ThousandEyes はトレースヘッダーを注入し、そのリクエストのトレースコンテキストをキャプチャします。

トレースが表示されるまでに時間がかかる場合があります。ThousandEyes の Service Map に移動し、トレース ID をコピーして Observability Cloud で検索できます。トレースがまだ進行中である可能性があります。

### ステップ 4: 双方向調査ループを検証する

テストが実行中でコネクタが有効になったら、両方向のワークフローを検証します。

### ThousandEyes から開始する

1. ThousandEyes でテストを開きます。
2. **Service Map** タブに移動します。
3. トレースパス、サービスレイテンシ、およびダウンストリームエラーが表示されることを確認します。
4. ThousandEyes から **Splunk APM** へのリンクを使用して、完全なトレースを検査します。

![ThousandEyes Service Map と Splunk APM の相関](../images/thousandeyes-service-map.png)

#### Splunk APM で続行する

Splunk APM 内で、トレースに以下のような ThousandEyes メタデータが含まれていることを確認します

- `thousandeyes.account.id`
- `thousandeyes.test.id`
- `thousandeyes.permalink`
- `thousandeyes.source.agent.id`

`thousandeyes.permalink` フィールドまたはトレースウォーターフォールビューの **Go to ThousandEyes test** ボタンを使用して、元の ThousandEyes テストに戻ります。

![Splunk APM トレースから ThousandEyes へのリンク](../images/splunk-apm-trace.png)

## 推奨される学習シナリオ

クラウドエージェントと自分の URL を使用して Web テストを作成してみてください（例`http://i-0cedf3429f9192aaa.splunk.show:81/#!/owners`、自分のインスタンスに置き換えてください）。

## 再確認が必要なセクション

ワークショップ中は以下のフローを使用してください

1. 複数のサービスを呼び出す内部 API ルートに対して ThousandEyes テストを作成します。
2. ThousandEyes が最初に問題を検出するようにし、クラスがネットワークおよびシンセティックモニタリングの観点から始められるようにします。
3. ThousandEyes の **Service Map** を開き、レイテンシやエラーが始まる場所を特定します。
4. **Splunk APM** に移動し、スパンレベルの分析を行います。
5. **ThousandEyes** に戻り、テスト、エージェント、およびネットワークパスを再度検査します。

これは強力な学習ループです。異なるチームが実際にどのように作業するかを反映しているためです

- ネットワークおよびエッジチームは、多くの場合 ThousandEyes から開始します。
- SRE およびプラットフォームチームは、多くの場合 Splunk ダッシュボードまたはアラートから開始します。
- アプリケーションチームは通常、Splunk APM でトレースを確認したいと考えます。

この統合が導入されていれば、全員がコンテキストを失うことなく切り替えることができます。

## よくある落とし穴

- テストが Splunk ダッシュボードに表示されていても、トレースの相関がない場合があります。これは通常、**metrics** ストリームのみが設定されており、**Splunk APM Generic Connector** が設定されていないことを意味します。
- トレースが Splunk APM に存在していても、監視対象のエンドポイントがトレースヘッダーをダウンストリームに伝播しない場合、ThousandEyes に表示されないことがあります。
- `/health` のような浅いエンドポイントは、設定が正しくても限定的なトレース値しか生成しないことが多いです。

## 参考資料

- [ThousandEyes Distributed Tracing](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing)
- [ThousandEyes Distributed Tracing with Splunk Observability APM](https://docs.thousandeyes.com/product-documentation/integration-guides/custom-built-integrations/distributed-tracing/distributed-tracing-splunk-apm)
- [Splunk APM: View traces with Cisco ThousandEyes integration](https://help.splunk.com/en/splunk-observability-cloud/monitor-application-performance/manage-services-spans-and-traces-in-splunk-apm/view-and-filter-for-spans-within-a-trace)
- [Splunk OTel Collector zero-code instrumentation for Kubernetes language runtimes](https://help.splunk.com/en/splunk-observability-cloud/manage-data/splunk-distribution-of-the-opentelemetry-collector/get-started-with-the-splunk-distribution-of-the-opentelemetry-collector/automatic-discovery-of-apps-and-services/kubernetes/language-runtimes)
