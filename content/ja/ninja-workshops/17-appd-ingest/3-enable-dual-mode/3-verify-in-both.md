---
title: 3. 両方のプラットフォームで確認
weight: 3
---

デュアルモードを有効にして負荷を流している状態で、数分以内にトレースがSplunk Observability Cloudに到着するはずです。両方の送信先を確認しましょう。

## AppDynamics の確認（変更なし）

[AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/) に戻り、アプリケーションを開いて以下を確認します：

- **OrderService** ティアがフローマップに引き続き表示されている
- `/order` と `/inventory` のビジネストランザクションが引き続き記録されている
- デュアルモードの追加によるエラーやパフォーマンス低下がない

デュアルモードはAppDynamicsのデータ収集に影響を与えないはずです。両方のストリームは独立して動作します。

## Splunk Observability Cloud の確認

1. [Splunk Observability Cloud](https://app.signalfx.com) に移動し、インストラクターから提供された認証情報でログインします。
2. 左側のナビゲーションパネルで **APM** をクリックします。
3. **Environment** ドロップダウンで `<INSTANCE>-appd-dual` を選択します（これはリソース属性で設定した `deployment.environment` の値と一致します）。
![AppDynamics Application](../../_images/o11y-service.png?width=30vw)

{{% notice title="数分お待ちください" style="info" icon="info-circle" %}}
デュアルモードを有効にしてからトレースが表示されるまで2〜5分かかることがあります。サービスがまだ表示されない場合は、少し待ってからページを更新してください。
{{% /notice %}}

4. サービスリストに **OrderService** が表示されるはずです。

## トレースを探索する

1. **OrderService** サービスをクリックします。
2. **Traces** をクリックして個々のトレースを表示します。
3. `GET /order` のトレースを選択してトレース詳細のウォーターフォールを開きます。

トレースウォーターフォールでは、OTel Java自動計装によって生成されたスパンが表示されます。これらはAppDynamicsも監視している同じリクエストです。
![APM waterall](../../_images/waterfall.png)

## AppDynamics 相関属性の確認

**ルートスパン**をクリックしてスパン属性を確認します。AppDynamicsの相関属性が表示されるはずです：

| Attribute | Example Value |
|---|---|
| `appd.app.name` | `Dual-Ingest-YOURINITIALS` |
| `appd.tier.name` | `OrderService` |
| `appd.bt.name` | `/order` or `/inventory` |
| `appd.request.guid` | *(the AppDynamics request GUID)* |

これらの属性はデュアルモードのAppDynamicsエージェントによって自動的に追加されます。このOTelトレースとAppDynamics Controllerの対応するデータとの直接的なリンクを作成します。

{{% notice title="重要なポイント" style="primary" icon="lightbulb" %}}
`appd.tier.name` 属性は、ティアが変更されるたびにトレースの途中のスパンにも表示されます。マルチティアアプリケーションでは、各スパンが正しいAppDynamicsティアのIDを保持します。
{{% /notice %}}

これで、同じアプリケーションが単一のエージェントから **2 つのプラットフォームに同時に** APMデータを送信するようになりました。次のセクションでは、グローバルデータリンクを作成して2つを接続します。
