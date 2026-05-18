---
title: APM Integration
linkTitle: 4.2 APM Integration
weight: 1
time: 10 minutes
description: APM と ThousandEyes 間の双方向ドリルダウンを設定します
---

## 概要

このセクションでは、ThousandEyes で APM Connector を設定します。

{{% notice title="統合設定は1回のみ必要です" style="warning" %}}
各ワークショップ参加者がこの設定を行う代わりに、インストラクターが以下の手順を実行するのを確認してください。

次のページから手順を続行します。
{{% /notice %}}

### ステップ 1: ThousandEyes で Splunk APM Connector を作成する

前のセクションのメトリクスストリーミング統合では **Ingest** トークンを使用しました。このステップは異なります。ThousandEyes が Splunk APM にクエリを実行してトレースリンクを構築する必要があるため、代わりに Splunk **API** トークンを使用します。

1. Splunk Observability Cloud で、**API** スコープを持つアクセストークンを作成します。
2. ThousandEyes で、**Manage > Integrations > Integrations 2.0** に移動し、**Connectors** タブに切り替えます。
3. **Generic Connector** を作成します。Preset として **Splunk Observability APM** を選択できます:

- **Name**: `Splunk APM`
- **Target URL**: `https://api.<REALM>.signalfx.com`
- **Header**: `X-SF-Token: <your-api-scope-token>`

4. **Save and Assign Operation** をクリックします。

![ThousandEyes での Splunk APM Generic Connector](../../images/splunk-apm-generic-connector.png?width=35vw)

5. **New Operation** をクリックし、**Splunk Observability APM** を選択します。
6. 名前を `Splunk APM` にします。
7. **Save & Assign Connector** をクリックします。

![ThousandEyes での Splunk APM Operation](../../images/splunk-apm-operation.png?width=35vw)

8. 作成したコネクターを選択し、**Save** をクリックします。

![ThousandEyes での Splunk APM Manage Operations](../../images/splunk-apm-manage-operations.png?width=35vw)

{{% notice title="成功" style="success" icon="check" %}}
コネクターと割り当てられたオペレーションが表示されていれば、正常な状態です。
{{% /notice %}}

{{% notice title="トラブルシューティングガイダンス" style="note" %}}
**No assigned operation** のような表示が見える場合は、**Manage** をクリックして割り当てを行う必要があります。
![Splunk APM Integration Summary](../../images/splunk-apm-integration-summary.png?width=35vw)
{{% /notice %}}
