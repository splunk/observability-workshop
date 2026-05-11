---
title: シナリオレビュー
linkTitle: 6. シナリオレビュー
weight: 6
time: 10 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px;">

## シナリオ: 小売店舗でのネットワーク障害

このシナリオでは、キャンパス、ブランチ、および店舗拠点を持つ組織を対象としています。ネットワーク障害が発生した場合、運用チームはどのサイトが影響を受けているか、またネットワークのどのコンポーネントが正常でないかを迅速に把握する必要があります。このシナリオのウォークスルーでは、ITSI が Cisco Catalyst Center からのデバイスヘルスデータを使用し、他のツール（この場合は Solarwinds）からのアラートと相関させることで、数分で障害の全体像を把握する方法を示します。

実際の環境では、同じシステムを多くの異なるツールで監視していることが一般的です。障害が発生すると、すべてのツールがアラートやアラームを発報し始めます。これによりアラートストームが発生し、どこからトラブルシューティングを始めればよいか理解することが非常に困難になります。その結果、障害解決に大幅な遅延が生じ、運用チーム全体にアラート疲れが広がります。

ITSI は、サイトおよびネットワークレイヤーごとにネットワークの健全性を把握し、任意の数の異なる監視ソリューションからのアラートを相関させる高度にアクション可能なエピソードを提供することで、この課題に対処します。コンソール間を行き来する代わりに、チームは何が起きているか、どこで起きているか、どのツールのどのアラートが関連しているかを単一のビューで確認できます。

## シナリオフロー: Catalyst Center による根本原因分析

<div style="max-width: 80%; margin: 0 auto;">
{{% notice title="シナリオレビュー" style="primary" icon="play" %}}

**1.** ITSI で **Service Analyzer** を開きます。**Access Points** KPI のヘルスステータスが低下していることに注目してください

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Service Analyzer は、インポートされたすべての Catalyst Center サイトサービスとその現在のヘルス状態の概要ビューを提供します
</div>

![Service Analyzer](../images/service-analyzer.png?width=40vw)
{{% / notice %}}
</div>

**2.** 右側の **Tree** を選択して **Service Tree** を表示します

**3.** **Store-SJC12** サービスを選択して KPI を展開します。**Access Points** KPI が正常でないことに注目してください。これは、この拠点でワイヤレスの問題が発生していることを示しています

**4.** **Access Points** KPI を選択してエンティティの詳細にドリルダウンします。この問題がこの拠点の **Floor-1** に影響していることが確認できるはずです

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
サービスを選択すると、個々の KPI が表示されます。Access Points KPI のヘルススコアが低下した状態を示しています
</div>

![Store-SJC12 Access Points KPI](../images/service-kpis.png?width=40vw)
{{% / notice %}}
</div>

{{% notice title="ボーナス" style="primary" icon="lightbulb" %}}
**Site Health Summary** リンクを使用してエンティティにドリルダウンし、この店舗のワイヤレスアクセスポイントのヘルス状態をより詳細に確認します。このダッシュボードは、Catalyst Center から直接取得された個々のデバイスヘルススコアの詳細なビューを提供します。

<div style="max-width: 60%; margin: 0 auto;">

<div style="text-align: center;">
Site Health Summary ダッシュボードは、選択した拠点の個々のアクセスポイントのヘルススコアを表示します
</div>

![Site Health Summary](../images/site-health.png?width=40vw)

</div>
{{% / notice %}}

**5.** KPI ヘルス詳細の下にある **Episode Review** セクションを確認します。このサイトで現在オープンしている **High** または **Critical** のエピソードがある場合、ここに表示されます。

{{% notice style="info" %}}
このシナリオは **Medium** の重大度から始まり、追加のアラートが生成されるにつれて **High** にエスカレートします。30分の休止サイクルのどの時点にいるかによっては、このリストにまだエピソードが表示されない場合があります。表示されない場合は、次のステップに進み、Alerts and Episodes の完全なビューを確認してください。
{{% / notice %}}

現在 **High** または **Critical** のエピソードがない場合は、**Alerts and Episodes** に移動してエピソードの完全なリストを確認します。シナリオの実行時間に応じて、このサイトの以前に解決されたエピソードが表示される場合があります。これは、ITSI が基盤となる問題が解消された際に、オープンなエピソードを自動的にクローズし、ステータスを **Resolved** に設定できることを示しています

**6.** 進行中のエピソードがある場合は、それを選択します。ない場合は、最近解決されたエピソードの1つを選択してレビューします

**7.** エピソード詳細で**影響を受けたサービスと KPI** を確認します。このビューは、このエピソード中にどのサービスと KPI が影響を受けたかを正確に示します。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
エピソード詳細は、アラートを影響を受けたサービスと KPI に紐付け、ビジネスへの影響の全体像を提供します
</div>

![Episode Review under KPI](../images/ongoing-episode-overview.png?width=40vw)
{{% / notice %}}
</div>

**8.** **Events Timeline** タブを選択して、イベントが発生した順序を確認します

**9.** **Sort** ドロップダウンから **Root cause analysis** を選択して、イベントを時系列順に並べ替えます

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Root Cause Analysis でソートされた Events Timeline は、アラートが発報された順序を明らかにし、最初の障害からカスケードする影響への進行を示します
</div>

![Episode Detail](../images/ongoing-episode.png?width=40vw)
{{% / notice %}}
</div>

**10.** リストから個々のアラートを選択して確認します。このエピソードには **Solarwinds** と **Catalyst Center** の両方からのアラートが含まれていることに注目してください。これは、エピソードが前のセクションで作成した **Network Events by Location NEAP** を使用しているためで、ソースに関係なく特定のサイトのすべてのアラートをグループ化します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
単一のエピソードでのクロスベンダーアラート相関。Catalyst Center と Solarwinds の両方のアラートが拠点ごとにグループ化されています
</div>

![Alert Detail](../images/ongoing-episode-event-view.png?width=40vw)
{{% / notice %}}
</div>

これで、アラートをコンテキスト内で確認し、発生時刻を把握し、状況の進展に伴う重大度の変化を追跡できるようになりました。Catalyst Center または Solarwinds からクリアリングイベントを受信すると、アラートの重大度は自動的に **Normal** に変更されます。NEAP で設定したアクションルールにより、すべての関連アラートが正常に戻った後、エピソードが自動的に解決され、手動介入なしにループが閉じられます。

{{% notice style="Primary" title="ワークショップ完了!" %}}
<div style="text-align: center;">

**これが重要な理由**

このワークショップを通じて、Catalyst Center のトポロジーデータを使用した**拠点ベースのネットワーク可視性**を提供するように ITSI を設定し、**2つの独立した監視ツール**からのアラートを取り込んで正規化し、それらのアラートを**サイトごとの単一のアクション可能なエピソード**に相関させるカスタム集約ポリシーを構築しました。

その結果、ツール間の切り替えを排除し、アラートノイズを削減し、運用チームに3つの重要な質問に対する即座の回答を提供するシステムが構築されました: *問題はどこにあるのか？何が影響を受けているのか？状況は改善しているのか悪化しているのか？*

エピソードの作成と解決を自動化することで、ITSI は平均復旧時間を短縮し、チームが切り離されたコンソール間で重複するアラートを追いかけるのではなく、実際の問題の調査に時間を費やせるようにします。

### Happy Splunking

![Dancing Buttercup](../../../ninja-workshops/11-ingest-processor-for-observability-cloud/images/Splunk-dancing-buttercup-GIF-103.gif?width=40vw)

</div>
{{% / notice %}}

{{% /notice %}}
</div>

</div>
