---
title: ITSI Service and KPI Review
linkTitle: 5.2 ITSI Service and KPI Review
weight: 2
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px; margin-top: 25px;">
<center>
このセクションでは、前のステップで構成したコンテンツパックとアラート統合によって作成されたサービスとエピソードを確認し、エンドツーエンドのパイプライン全体が正しく動作していることを確認します。
</center>

{{% notice title="演習: サービスとエピソードの確認" style="primary" icon="running" %}}

{{% notice style="info" %}}
IT Service Intelligence (ITSI) の Service Insights は、組織内のビジネスサービスおよび技術サービスのマッピングと監視を表します。ITSI において、サービスとは、組織に特定のサービスを提供するように構成された、相互接続されたアプリケーションとホストの集合です。ITSI Service Insights は、デバイスとアプリケーション間の接続に基づいてサービスの依存関係をマッピングするのに役立ち、問題のあるオブジェクトがサービス運用の残りの部分に与える影響を即座に確認できます。
{{% /notice %}}

**1.** **ITSI Service Analyzer** > **Default Service Analyzer** に移動します。インポートしたサービスが表示されるはずです

**2.** Analyzer の名前を `Network Health by Location` に編集します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Tree ビューでは、各 Catalyst Center サイトとその基盤となる KPI の正常性を含む、完全なサービス階層が表示されます
</div>

![Service Analyzer Tree View](../../images/service-analyzer.png?width=40vw)
{{% / notice %}}
</div>

**3.** 右側の **Tree** をクリックします

**4.** **Filter Services** に **United States** を追加します

**5.** 時間枠を **Last 1 hour** に、**Auto Refresh** を **1 minute** に設定します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
United States でフィルタリングし Auto Refresh を設定すると、すべてのロケーションにわたるサイトの正常性をライブビューで確認できます
</div>

![Episode Review](../../images/service-kpis.png?width=40vw)
{{% / notice %}}
</div>

**6.** **Save** をクリックします。ビューは下の画像と同じになるはずです

**7.** **Alerts and Episodes** をクリックします

**8.** 最近作成されたエピソードを選択します

**9.** **Episode details** で、使用された **Aggregation Policy** が前のステップで作成した NEAP であることを確認します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
カスタム NEAP によって作成されたエピソードは、Catalyst Center と SolarWinds のアラートをサイト名のエピソードとしてグループ化します
</div>

![Alerts and Episodes](../../images/episode-review.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="Primary" title="お疲れ様でした!" %}}
<div style="text-align: center;">
パイプライン全体が確認されました。サービスとその依存関係が構成され、KPI が計算されており、カスタム NEAP がクロスベンダーのアラートをサイトごとにグループ化しています。

次のセクションに進んで、このシナリオを確認しましょう。
</div>
{{% / notice %}}

{{% /notice %}}
</div>
