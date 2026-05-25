---
title: 設定の検証
linkTitle: 2.3 設定の検証
weight: 3
time: 2 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

インポートしたサービスと KPI が正しく計算されていること、および Catalyst Center からのアラートパイプラインがアクティブであることを確認してから次に進みます。

{{% notice title="演習: 設定の検証" style="primary" icon="running" %}}

**1.** **Service Analyzer** > **Default Service Analyzer** に移動します。

インポートしたサービスと、Catalyst Center Site Service Template に含まれる KPI が表示されるはずです。

サービスと KPI のヘルスステータスが表示されるまで数分かかる場合があります。

{{% notice style="Info" %}}
Service Analyzer には、インポートした Catalyst Center サイトサービスとその現在のヘルスステータスが表示されます

![ITSI Service Analyzer](../../images/service-analyzer.png?width=40vw)
{{% / notice %}}

**2.** **Tree** をクリックして **Service Tree** ビューに切り替えます

**3.** サービスツリーで Store サービスのいずれかをクリックして、Catalyst Center Site に関連付けられた KPI を表示します

{{% notice style="Info" %}}
サービスをクリックすると、個々の KPI とネットワークレイヤーごとの現在のヘルススコアが表示されます

![Service KPIs](../../images/service-kpis.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="おめでとうございます！" %}}
Catalyst Center サービスが ITSI で稼働しています！

次のセクションでは、**Inbound Notification Service** を設定します。これにより、ネットワークパフォーマンスの低下を示す Catalyst Center Issue が発生した際に、ITSI で自動的にNotable Event が作成されるようになります。
{{% / notice %}}

{{% / notice %}}
