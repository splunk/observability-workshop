---
title: 3. 両方のプラットフォームで確認
weight: 3
---

デュアルモードを有効にしてロードが流れている状態では、数分以内にトレースが Splunk Observability Cloud に到着するはずです。両方の送信先で確認しましょう。

## AppDynamics での確認（変更なし）

[AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/) に戻り、アプリケーションを開いて以下を確認します

- **OrderService** ティアがフローマップに引き続き表示されている
- `/order` と `/inventory` のビジネストランザクションが引き続き記録されている
- デュアルモードの追加によるエラーや性能低下がない

デュアルモードは AppDynamics のデータ収集に影響を与えません。両方のストリームは独立して動作します。

## Splunk Observability Cloud での確認

1. [Splunk Observability Cloud](https://app.signalfx.com) に移動し、インストラクターから提供された認証情報でログインします。
2. 左側のナビゲーションパネルで **APM** をクリックします。
3. **Environment** ドロップダウンで `<INSTANCE>-appd-dual` を選択します（これはリソース属性で設定した `deployment.environment` の値と一致します）。
![AppDynamics Application](../../_images/o11y-service.png?width=30vw)

{{% notice title="数分お待ちください" style="info" icon="info-circle" %}}
デュアルモードを有効にしてからトレースが表示されるまで2〜5分かかることがあります。サービスがまだ表示されない場合は、少し待ってからページを更新してください。
{{% /notice %}}

4. サービスリストに **OrderService** が表示されるはずです。

## トレースの確認

1. **OrderService** サービスをクリックします。
2. **Traces** をクリックして個々のトレースを表示します。
3. `GET /order` のトレースを選択してトレース詳細のウォーターフォールを開きます。

トレースウォーターフォールでは、OTel Java 自動計装によって生成されたスパンが表示されます。これらは AppDynamics も監視している同じリクエストです。
![APM waterall](../../_images/waterfall.png)

## AppDynamics 相関属性の確認

**ルートスパン**をクリックして、スパン属性を確認します。AppDynamics の相関属性が表示されるはずです

| Attribute | Example Value |
|---|---|
| `appd.app.name` | `Dual-Ingest-YOURINITIALS` |
| `appd.tier.name` | `OrderService` |
| `appd.bt.name` | `/order` or `/inventory` |
| `appd.request.guid` | *(the AppDynamics request GUID)* |

これらの属性は、デュアルモードの AppDynamics エージェントによって自動的に追加されます。これにより、この OTel トレースと AppDynamics Controller 内の対応するデータとの間に直接的なリンクが作成されます。

{{% notice title="重要なポイント" style="primary" icon="lightbulb" %}}
`appd.tier.name` 属性は、ティアが変わるたびにトレースの途中のスパンにも表示されます。マルチティアアプリケーションでは、各スパンが正しい AppDynamics ティア ID を保持します。
{{% /notice %}}

これで、同じアプリケーションが単一のエージェントから **2つのプラットフォームに同時に** APM データを送信しています。次のセクションでは、グローバルデータリンクを作成して2つのプラットフォームを接続します。
