---
title: 3. 両プラットフォームで確認
weight: 3
---

デュアルモードを有効にして負荷が流れている状態では、数分以内にトレースがSplunk Observability Cloudに届きます。両方の送信先を確認しましょう。

## AppDynamicsでの確認（変更なし）

[AppDynamics Controller](https://se-lab.saas.appdynamics.com/controller/)に戻り、アプリケーションを開いて以下を確認します。

- **OrderService** ティアがフローマップに表示されている
- `/order` と `/inventory` のビジネストランザクションが記録されている
- デュアルモードの追加によるエラーやパフォーマンス低下がない

デュアルモードはAppDynamicsのデータ収集に影響を与えません。両方のストリームは独立して動作します。

## Splunk Observability Cloudでの確認

1. [Splunk Observability Cloud](https://app.signalfx.com)に移動し、インストラクターから提供された認証情報でログインします。
2. 左側のナビゲーションパネルで **APM** をクリックします。
3. **Environment** ドロップダウンで `<INSTANCE>-appd-dual` を選択します（これはリソース属性で設定した `deployment.environment` の値と一致します）。
![AppDynamics Application](../../_images/o11y-service.png?width=30vw)

{{% notice title="数分お待ちください" style="info" icon="info-circle" %}}
デュアルモードを有効にしてからトレースが表示されるまで2〜5分かかることがあります。サービスがまだ表示されない場合は、しばらく待ってからページを更新してください。
{{% /notice %}}

1. サービスリストに **OrderService** が表示されます。

## トレースの確認

1. **OrderService** サービスをクリックします。
2. **Traces** をクリックして個々のトレースを表示します。
3. `GET /order` のトレースを選択して、トレース詳細のウォーターフォールを開きます。

トレースウォーターフォールには、OTel Java自動計装によって生成されたSpanが表示されます。これらはAppDynamicsも同時にモニタリングしているリクエストと同じものです。
![APM waterall](../../_images/waterfall.png)

## AppDynamics相関属性の確認

**ルートSpan** をクリックして、Span属性を確認します。AppDynamicsの相関属性が表示されます。

| 属性 | 値の例 |
|---|---|
| `appd.app.name` | `Dual-Ingest-YOURINITIALS` |
| `appd.tier.name` | `OrderService` |
| `appd.bt.name` | `/order` or `/inventory` |
| `appd.request.guid` | *（AppDynamicsのリクエストGUID）* |

これらの属性は、デュアルモードでAppDynamicsエージェントによって自動的に追加されます。このOTelトレースとAppDynamics Controllerの対応するデータとの間に直接的なリンクを作成します。

{{% notice title="重要なポイント" style="primary" icon="lightbulb" %}}
`appd.tier.name` 属性は、ティアが変わるたびにトレースの途中のSpanにも表示されます。マルチティアアプリケーションでは、各Spanが正しいAppDynamicsティアIDを持ちます。
{{% /notice %}}

これで、同じアプリケーションが単一のエージェントから **2つのプラットフォームに同時に** APMデータを送信しています。次のセクションでは、グローバルデータリンクを作成して2つを接続します。
