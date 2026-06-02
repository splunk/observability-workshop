---
title: APM Integration
linkTitle: 4.2 APM Integration
weight: 1
time: 10 minutes
description: APM と ThousandEyes 間の双方向ドリルダウンを設定する
---

## 概要

このセクションでは、ThousandEyes で APM Connector を設定します。

{{< acknowledge "Only need 1 integration" >}}
参加者全員が個別に設定するのではなく、インストラクターが以下の手順を実演しますので、それを見学してください。

次のページで引き続き手順を実施します。
{{< /acknowledge >}}

### Step 1: ThousandEyes で Splunk APM Connector を作成する

前のセクションのメトリックストリーミング統合では **Ingest** トークンを使用しました。今回の手順は異なります。ThousandEyes は Splunk APM にクエリを発行してトレースリンクを構築するため、Splunk の **API** トークンを使用します。

1. Splunk Observability Cloud で、**API** スコープを持つアクセストークンを作成します。
2. ThousandEyes で **Manage > Integrations > Integrations 2.0** に移動し、**Connectors** タブに切り替えます。
3. **Generic Connector** を作成します。Preset として **Splunk Observability APM** を選択できます。
    - **Name**: `Splunk APM`
    - **Target URL**: `https://api.<REALM>.signalfx.com`
    - **Header**: `X-SF-Token: <your-api-scope-token>`
4. **Save and Assign Operation** をクリックします。

    ![Splunk APM Generic Connector in ThousandEyes](../../images/splunk-apm-generic-connector.png?width=35vw)
5. **New Operation** をクリックし、**Splunk Observability APM** を選択します。
6. 名前を `Splunk APM` にします。
7. **Save & Assign Connector** をクリックします。
    ![Splunk APM Operation in ThousandEyes](../../images/splunk-apm-operation.png?width=35vw)
8. 先ほど作成したコネクターを選択し、**Save** をクリックします。

![Splunk APM Manage Operations in ThousandEyes](../../images/splunk-apm-manage-operations.png?width=35vw)

{{< checkpoint "コネクターと、それに割り当てたオペレーションが表示されていれば、正常な状態です。" >}}

{{% notice title="トラブルシューティングのヒント" style="note" %}}
**No assigned operation** のような表示が出ている場合は、**Manage** をクリックして割り当てを行う必要があります。
![Splunk APM Integration Summary](../../images/splunk-apm-integration-summary.png?width=35vw)
{{% /notice %}}
