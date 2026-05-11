---
title: 設定の検証
linkTitle: 2.3 設定の検証
weight: 3
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px; margin-top: 25px;">
<center>
インポートしたサービスと KPI が正しく計算されていること、および Catalyst Center からのアラートパイプラインがアクティブであることを確認してから、次に進みます。
</center>

{{% notice title="演習: 設定の検証" style="primary" icon="running" %}}

**1.** **Service Analyzer** > **Default Service Analyzer** に移動します。

インポートしたサービスと、Catalyst Center Site Service Template に含まれる KPI が表示されるはずです。

サービスと KPI のヘルスステータスが表示されるまで数分かかる場合があります。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Service Analyzer には、インポートした Catalyst Center サイトサービスとその現在のヘルスステータスが表示されます
</div>

![ITSI Service Analyzer](../../images/service-analyzer.png?width=40vw)
{{% / notice %}}
</div>

**2.** **Tree** をクリックして **Service Tree** ビューに切り替えます

**3.** サービスツリー内の Store サービスのいずれかをクリックして、Catalyst Center Site に関連付けられた KPI を表示します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
サービスをクリックすると、個々の KPI とネットワークレイヤーごとの現在のヘルススコアが表示されます
</div>

![Service KPIs](../../images/service-kpis.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="Primary" title="おめでとうございます！" %}}
<div style="text-align: center;">
Catalyst Center サービスが ITSI で稼働しています！

次のセクションでは、**Inbound Notification Service** を設定します。これにより、ネットワークパフォーマンスの低下を示す Catalyst Center Issue が発生した際に、ITSI でノータブルイベントが自動的に作成されるようになります。
</div>
{{% / notice %}}

{{% / notice %}}
</div>
