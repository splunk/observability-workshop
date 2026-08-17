---
title: 3. 両方のプラットフォームで確認する
weight: 3
---

デュアルモードが有効になり、負荷がかかっている状態では、数分以内に Splunk Observability Cloud にトレースが届くはずです。両方の送信先を確認しましょう。

## AppDynamics の確認（変更なし）

[AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/) に戻り、アプリケーションを開いて以下を確認します

- **OrderService** ティアがフローマップに表示されていること
- `/order` と `/inventory` のビジネストランザクションが記録され続けていること
- デュアルモードを追加してもエラーや劣化がないこと

デュアルモードは AppDynamics のデータ収集に影響を与えないはずです。両方のストリームは独立して動作します。

## Splunk Observability Cloud の確認

1. [Splunk Observability Cloud](https://app.signalfx.com) にアクセスし、インストラクターから提供された認証情報でログインします。
2. 左側のナビゲーションパネルで **APM** をクリックします。
3. **Environment** ドロップダウンで `<INSTANCE>-appd-dual` を選択します（これはリソース属性で設定した `deployment.environment` の値と一致します）。
![AppDynamics Application](../../_images/o11y-service.png?width=30vw)

{{% notice title="数分お待ちください" style="info" icon="info-circle" %}}
デュアルモードを有効にしてからトレースが表示されるまで 2〜5 分かかることがあります。サービスがまだ表示されない場合は、しばらく待ってからページを更新してください。
{{% /notice %}}

4. サービスリストに **OrderService** が表示されるはずです。

## トレースを探索する

1. **OrderService** サービスをクリックします。
2. **Traces** をクリックして個々のトレースを表示します。
3. `GET /order` のトレースを選択して、トレース詳細のウォーターフォールを開きます。

トレースウォーターフォールには、OTel Java 自動計装によって生成されたスパンが表示されます。これらは AppDynamics も監視しているのと同じリクエストです。
![APM waterall](../../_images/waterfall.png)

## AppDynamics 相関属性を確認する

**ルートスパン** をクリックしてスパン属性を確認します。AppDynamics の相関属性が表示されるはずです

| 属性 | 値の例 |
|---|---|
| `appd.app.name` | `Dual-Ingest-YOURINITIALS` |
| `appd.tier.name` | `OrderService` |
| `appd.bt.name` | `/order` または `/inventory` |
| `appd.request.guid` | *（AppDynamics リクエスト GUID）* |

これらの属性は、デュアルモードの AppDynamics エージェントによって自動的に追加されます。この OTel トレースと AppDynamics Controller 内の対応するデータとの間に直接リンクを作成します。

{{% notice title="重要なポイント" style="primary" icon="lightbulb" %}}
`appd.tier.name` 属性は、ティアが変わるたびにトレースの途中のスパンにも表示されます。マルチティアアプリケーションでは、各スパンが正しい AppDynamics ティアアイデンティティを持ちます。
{{% /notice %}}

これで、同じアプリケーションが単一のエージェントから **2 つのプラットフォームに同時に** APM データを送信するようになりました。次のセクションでは、グローバルデータリンクを作成して両者を接続します。
