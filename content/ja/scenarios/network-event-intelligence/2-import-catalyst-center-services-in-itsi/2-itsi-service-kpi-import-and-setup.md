---
title: ITSI サービスと KPI の検証
linkTitle: 2.2 ITSI サービスと KPI の検証
weight: 2
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px; margin-top: 25px;">
<center>
ITSI 4.21 では、手動のインポートプロセスがガイド付きワークフローと事前構築済みのデータ統合に置き換えられました。コンテンツパックには、Meraki と Catalyst Center のサービス階層を自動的に検出して構築するサービスインポートモジュールが含まれています。
</center>

{{% notice title="演習: サービスのインポートとアラートの設定" style="primary" icon="running" %}}

{{% notice title="ヒント" style="primary" icon="lightbulb" %}}
Catalyst Center の Import Services ページに戻るには、**Configuration** > **Data Integrations** > **Content Library** > **Cisco Enterprise Networks** に移動します。
{{% / notice %}}

**1.** **Service Import Modules** の下で、**Cisco Catalyst Center** を選択します。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info"  %}}
<div style="text-align: center;">
自動サービス階層インポートは、<strong>Catalyst Center</strong> と <strong>Meraki</strong> の両方でサポートされています
</div>

![Service Import Modules](../../images/service-import-modules.png?width=40vw)
{{% / notice %}}
</div>

**2.** Catalyst Center ホストと利用可能なすべてのサービスを選択します。**Next** をクリックします。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Catalyst Center ホストと利用可能なすべてのサイトを選択して、ITSI サービスとしてインポートします
</div>

![Select Services](../../images/select-services.png?width=40vw)
{{% / notice %}}
</div>

**3.** **Default Service Sandbox** を選択します。**Next** をクリックします。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
サービスは、本番環境の ITSI に公開される前にレビュー用のサンドボックスにインポートされます
</div>

![Default Service Sandbox](../../images/default-service-sandbox.png?width=40vw)
{{% / notice %}}
</div>

**4.** インポートされるサービスを確認します。**Import** をクリックします。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Import をクリックする前に、作成される Catalyst Center サイトサービスの完全なリストを確認します
</div>

![Review Services](../../images/review-services.png?width=40vw)
{{% / notice %}}
</div>

**5.** Service Sandbox を確認します。**Publish** をクリックします。事前チェックが完了したら、**Next** をクリックします。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
サンドボックスでサービス階層を確認し、公開して ITSI でサービスを有効にします
</div>

![Service Sandbox](../../images/service-sandbox-publish.png?width=40vw)
{{% / notice %}}
</div>

**6.** **Configuration** > **Service Monitoring** > **Service and KPI Management** に移動します。

**7.** **Select All** チェックボックスを使用して、すべてのサービスを選択します。

**8.** すべてのサービスを選択した状態で、**Bulk Action** > **Enable** をクリックします。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Service and KPI Management ページから Bulk Action を使用して、インポートされたすべてのサービスを一度に有効にします
</div>

![Service and KPI Management](../../images/service-kpi-management.png?width=40vw)
{{% / notice %}}
</div>

**9.** **Enable** をクリックします。数分後に KPI が表示されます。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
有効化アクションを確認します。KPI は数分以内に計算を開始します
</div>

![Enable KPIs](../../images/enable-kpis.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="Primary" title="お疲れ様でした！" %}}
<div style="text-align: center;">
CSV やルックアップの作成、SPL の記述、サービス依存関係の手動設定を行うことなく、すべての Catalyst Center サービスをインポートできました。とても便利ですね。

次のセクションに進んで、設定が正しく動作していることを検証しましょう。
</div>
{{% / notice %}}

{{% /notice %}}
</div>
