---
title: ITSI サービスと KPI のレビュー
linkTitle: 5.2 ITSI サービスと KPI のレビュー
weight: 2
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

このセクションでは、前のステップで設定したコンテンツパックとアラート統合によって作成されたサービスとエピソードをレビューし、エンドツーエンドのパイプライン全体が正しく動作していることを確認します。

{{% notice title="演習: サービスとエピソードのレビュー" style="primary" icon="running" %}}

{{% notice style="info" %}}
IT Service Intelligence (ITSI) の Service Insights は、組織内のビジネスサービスおよび技術サービスのマッピングと監視を表します。ITSI において、サービスとは組織に特定のサービスを提供するように構成された、相互接続されたアプリケーションとホストのセットです。ITSI Service Insights は、デバイスとアプリケーション間の接続に基づいてサービスの依存関係をマッピングし、問題のあるオブジェクトがサービス運用の残りの部分に与える影響を即座に確認できるようにします。
{{% /notice %}}

**1.** **ITSI Service Analyzer** > **Default Service Analyzer** に移動します。インポートしたサービスが表示されるはずです

**2.** Analyzer の名前を `Network Health by Location` に編集します

{{% notice style="Info" %}}
Tree ビューは、各 Catalyst Center サイトとその基盤となる KPI の正常性を含む完全なサービス階層を表示します

![Service Analyzer Tree View](../../images/service-analyzer.png?width=40vw)
{{% / notice %}}

**3.** 右側の **Tree** をクリックします

**4.** **Filter Services** に **United States** を追加します

**5.** 時間範囲を **Last 1 hour** に、**Auto Refresh** を **1 minute** に設定します

{{% notice style="Info" %}}
United States でフィルタリングし、Auto Refresh を設定することで、すべてのロケーションにわたるサイトの正常性をリアルタイムで表示できます

![Episode Review](../../images/service-kpis.png?width=40vw)
{{% / notice %}}

**6.** **Save** をクリックします。表示は以下のグラフィックと同一になるはずです

**7.** **Alerts and Episodes** をクリックします

**8.** 最も新しく作成されたエピソードを選択します

**9.** **Episode details** で、使用された **Aggregation Policy** が前のステップで作成した NEAP であることを確認します

{{% notice style="Info" %}}
カスタム NEAP によって作成されたエピソードは、Catalyst Center と SolarWinds のアラートを単一のサイト名付きエピソードの下にグループ化します

![Alerts and Episodes](../../images/episode-review.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="お疲れ様でした！" %}}
パイプライン全体が確認されました。サービスとその依存関係が設定され、KPI が計算されており、カスタム NEAP がクロスベンダーのアラートをサイトごとにグループ化しています。

次のセクションに進んで、このシナリオのウォークスルーを行います。
{{% / notice %}}

{{% /notice %}}
