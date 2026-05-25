---
title: ITSI サービスと KPI の検証
linkTitle: 2.2 ITSI サービスと KPI の検証
weight: 2
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

ITSI 4.21 では、手動のインポートプロセスがガイド付きワークフローと事前構築済みのデータインテグレーションに置き換えられました。コンテンツパックには、Meraki と Catalyst Center のサービス階層を自動的に検出して構築するサービスインポートモジュールが含まれています。

{{% notice title="演習: サービスのインポートとアラートの設定" style="primary" icon="running" %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
Catalyst Center のサービスインポートページに戻るには、**Configuration** > **Data Integrations** > **Content Library** > **Cisco Enterprise Networks** に移動します。
{{% / notice %}}

**1.** **Service Import Modules** の下で、**Cisco Catalyst Center** を選択します。

{{% notice style="Info"  %}}
**Catalyst Center** と **Meraki** の両方で自動サービス階層インポートがサポートされています

![Service Import Modules](../../images/service-import-modules.png?width=40vw)
{{% / notice %}}

**2.** Catalyst Center ホストと利用可能なすべてのサービスを選択します。**Next** をクリックします。

{{% notice style="Info" %}}
Catalyst Center ホストと利用可能なすべてのサイトを選択して、ITSI サービスとしてインポートします

![Select Services](../../images/select-services.png?width=40vw)
{{% / notice %}}

**3.** **Default Service Sandbox** を選択します。**Next** をクリックします。

{{% notice style="Info" %}}
サービスは本番環境の ITSI に公開する前に、レビュー用のサンドボックスにインポートされます

![Default Service Sandbox](../../images/default-service-sandbox.png?width=40vw)
{{% / notice %}}

**4.** インポートされるサービスを確認します。**Import** をクリックします。

{{% notice style="Info" %}}
Import をクリックする前に、作成される Catalyst Center サイトサービスの完全なリストを確認します

![Review Services](../../images/review-services.png?width=40vw)
{{% / notice %}}

**5.** Service Sandbox を確認します。**Publish** をクリックします。事前チェックが完了したら、**Next** をクリックします。

{{% notice style="Info" %}}
サンドボックスでサービス階層を確認し、公開して ITSI でサービスをアクティブにします

![Service Sandbox](../../images/service-sandbox-publish.png?width=40vw)
{{% / notice %}}

**6.** **Configuration** > **Service Monitoring** > **Service and KPI Management** に移動します。

**7.** **Select All** チェックボックスを使用して、すべてのサービスを選択します。

**8.** すべてのサービスを選択した状態で、**Bulk Action** > **Enable** をクリックします。

{{% notice style="Info" %}}
Service and KPI Management ページから Bulk Action を使用して、インポートされたすべてのサービスを一括で有効にします

![Service and KPI Management](../../images/service-kpi-management.png?width=40vw)
{{% / notice %}}

**9.** **Enable** をクリックします。数分後に KPI が表示されます。

{{% notice style="Info" %}}
有効化アクションを確認します。KPI は数分以内に計算を開始します

![Enable KPIs](../../images/enable-kpis.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="お疲れ様でした！" %}}
CSV やルックアップの作成、SPL の記述、サービス依存関係の手動設定を一切行うことなく、すべての Catalyst Center サービスをインポートできました。とても便利ですね！

次のセクションに進んで、設定が正しく動作していることを検証しましょう。
{{% / notice %}}

{{% /notice %}}
