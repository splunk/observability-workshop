---
title: シナリオレビュー
linkTitle: 6. シナリオレビュー
weight: 6
time: 10 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---


## シナリオ：小売店舗でのネットワーク障害

このシナリオは、キャンパス、ブランチ、店舗の拠点を持つ組織を対象としています。ネットワーク障害が発生した場合、運用チームはどのサイトが影響を受けているか、ネットワークのどのコンポーネントが異常であるかを迅速に把握する必要があります。このシナリオウォークスルーでは、ITSI が Cisco Catalyst Center からのデバイスヘルスデータを使用し、他のツール（この場合は Solarwinds）からのアラートと相関させて、数分で問題の全体像を提供する方法を示します。

実際の環境では、組織は通常、同じシステムを監視する多くの異なるツールを使用しています。障害が発生すると、すべてのツールがアラートやアラームを発報し始めます。これによりアラートストームが発生し、どこからトラブルシューティングを開始すべきかを理解することが非常に困難になります。その結果、障害解決に大幅な遅延が生じ、運用チーム全体にアラート疲れが蔓延します。

ITSI は、サイトおよびネットワークレイヤーごとにネットワークヘルスを把握し、任意の数の異なる監視ソリューションからのアラートを相関させる高度にアクション可能なエピソードを提供することで、この課題に対処します。コンソール間を行き来する代わりに、チームは何が起きているか、どこで起きているか、どのツールのどのアラートが関連しているかを単一のビューで確認できます。

## シナリオフロー：Catalyst Center による根本原因分析

{{% notice title="シナリオレビュー" style="primary" icon="play" %}}

**1.** ITSI で **Service Analyzer** を開きます。**Access Points** KPI が劣化したヘルスステータスを示していることを確認します

{{% notice style="Info" %}}
Service Analyzer は、インポートされたすべての Catalyst Center サイトサービスとその現在のヘルスの概要ビューを提供します

![Service Analyzer](../images/service-analyzer.png?width=40vw)
{{% / notice %}}

**2.** 右側の **Tree** を選択して **Service Tree** を表示します

**3.** **Store-SJC12** サービスを選択して KPI を展開します。**Access Points** KPI が異常であることを確認します。これはこの拠点でワイヤレスの問題が発生していることを示しています

**4.** **Access Points** KPI を選択してエンティティの詳細にドリルダウンします。この問題がこの拠点の **Floor-1** に影響していることが確認できるはずです

{{% notice style="Info" %}}
サービスを選択すると、個々の KPI が表示されます。Access Points KPI のヘルススコアが劣化した状態を示しています

![Store-SJC12 Access Points KPI](../images/service-kpis.png?width=40vw)
{{% / notice %}}

{{% notice title="ボーナス" style="primary" icon="lightbulb" %}}
**Site Health Summary** リンクを使用してエンティティにドリルダウンし、この店舗のワイヤレスアクセスポイントのヘルスをより詳細に確認します。このダッシュボードは、Catalyst Center から直接取得された個々のデバイスヘルススコアの詳細ビューを提供します。

Site Health Summary ダッシュボードは、選択した拠点の個々のアクセスポイントのヘルススコアを表示します

![Site Health Summary](../images/site-health.png?width=40vw)

{{% / notice %}}

**5.** KPI ヘルスの詳細の下にある **Episode Review** セクションを確認します。このサイトに **High** または **Critical** のエピソードが現在オープンされている場合、ここに表示されます。

{{% notice style="info" %}}
このシナリオは **Medium** の重大度で始まり、追加のアラートが生成されると **High** にエスカレートします。30分のブレイクサイクルのどの時点にいるかによっては、このリストにまだエピソードが表示されない場合があります。表示されない場合は、次のステップに進み、完全な Alerts and Episodes ビューを確認してください。
{{% / notice %}}

現在 **High** または **Critical** のエピソードがない場合は、**Alerts and Episodes** に移動してエピソードの完全なリストを確認します。シナリオの実行時間によっては、このサイトの以前に解決されたエピソードが表示される場合があります。これは、ITSI が根本的な問題が解消された際に、オープンされたエピソードを自動的にクローズし、ステータスを **Resolved** に設定できることを示しています

**6.** 進行中のエピソードがある場合はそれを選択します。ない場合は、最近解決されたエピソードの1つを選択してレビューします

**7.** エピソードの詳細で **影響を受けたサービスと KPI** を確認します。このビューは、このエピソード中にどのサービスと KPI が影響を受けたかを正確に示します。

{{% notice style="Info" %}}
エピソードの詳細は、アラートを影響を受けたサービスと KPI に紐づけ、ビジネスインパクトの全体像を提供します

![Episode Review under KPI](../images/ongoing-episode-overview.png?width=40vw)
{{% / notice %}}

**8.** **Events Timeline** タブを選択して、イベントが発生した順序を確認します

**9.** **Sort** ドロップダウンから **Root cause analysis** を選択して、イベントを時系列で並べ替えます

{{% notice style="Info" %}}
Root Cause Analysis でソートされた Events Timeline は、アラートが発報された順序を明らかにし、最初の障害からカスケードする影響への進行を示します

![Episode Detail](../images/ongoing-episode.png?width=40vw)
{{% / notice %}}

**10.** リストから個々のアラートを選択して確認します。このエピソードには **Solarwinds** と **Catalyst Center** の両方からのアラートが含まれていることに注目してください。これは、エピソードが前のセクションで作成した **Network Events by Location NEAP** を使用しているためで、ソースに関係なく特定のサイトのすべてのアラートをグループ化します

{{% notice style="Info" %}}
単一エピソードでのクロスベンダーアラート相関。Catalyst Center と Solarwinds の両方のアラートが拠点ごとにグループ化されています

![Alert Detail](../images/ongoing-episode-event-view.png?width=40vw)
{{% / notice %}}

これで、アラートをコンテキスト内で確認し、いつ発生したかを理解し、状況の進展に伴う重大度の変化を追跡できるようになりました。Catalyst Center または Solarwinds からクリアリングイベントが受信されると、アラートの重大度は自動的に **Normal** に変更されます。NEAP で設定したアクションルールにより、すべてのアラートが正常に戻ると、エピソードは自動的に解決され、手動介入なしにループがクローズされます。

{{% notice style="Primary" title="ワークショップ完了！" %}}

**これが重要な理由**

このワークショップでは、Catalyst Center のトポロジーデータを使用して**拠点ベースのネットワーク可視性**を提供するように ITSI を設定し、**2つの独立した監視ツール**からのアラートを取り込みおよび正規化し、それらのアラートを**サイトごとの単一のアクション可能なエピソード**に相関させるカスタム集約ポリシーを構築しました。

その結果、ツール切り替えを排除し、アラートノイズを削減し、運用チームに3つの重要な質問に対する即座の回答を提供するシステムが構築されました*問題はどこにあるか？何が影響を受けているか？状況は改善しているか、悪化しているか？*

エピソードの作成と解決を自動化することで、ITSI は平均復旧時間を短縮し、チームが切断されたコンソール間で重複するアラートを追いかける代わりに、実際の問題の調査に時間を費やせるようにします。

### Happy Splunking

![Dancing Buttercup](../../../ninja-workshops/11-ingest-processor-for-observability-cloud/images/Splunk-dancing-buttercup-GIF-103.gif?width=40vw)

{{% / notice %}}

{{% /notice %}}
