---
title: ITSI Create Custom NEAP
linkTitle: 5.1 ITSI Create Custom NEAP
weight: 1
time: 10 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

前のステップで Catalyst Center と Solarwinds のインバウンド通知ルールを設定したため、まもなくこれらのソースに対してエピソードが生成されるのが確認できるはずです。ITSI がデフォルトの集約ポリシーを適用していることに気づくかもしれません。これはアラートをソース別にグループ化することで迅速な集約価値を提供します。しかし、このデータセットではエピソードをロケーション別にグループ化したいと考えています。これにより、Catalyst Center と SolarWinds のアラート間の相関が可能になり、ITSI イベント管理の差別化機能となります。

{{% notice title="演習: カスタム NEAP の作成" style="primary" icon="running" %}}

**1.** **Alerts and Episodes** に移動します。最近作成されたエピソードを確認します。アラートのグループ化に **Default Aggregation Policy** が使用されていることに注目してください。この環境のブレークシナリオは30分サイクル（15分間正常、15分間異常）で動作しているため、エピソードが表示されるまで最大15分かかる場合があります。

{{% notice style="Info" %}}
Alerts and Episodes ビューには、現在のすべてのNotableイベントと、それらがグループ化されたエピソードが表示されます

![Alerts and Episodes](../../images/alerts-and-episodes.png?width=40vw)
{{% / notice %}}

**2.** **Configuration** > **Event Management** > **Notable Event Aggregation Policies** に移動します。

**3.** 右上隅の **Create Notable Event Aggregation Policy** をクリックします。

{{% notice style="Info" %}}
ITSI にはいくつかの組み込みポリシーが含まれています。ここでは、複数のベンダーからのネットワークサイトアラートをグループ化するための新しいポリシーを作成します

![Create NEAP](../../images/create-neap.png?width=40vw)
{{% / notice %}}

**4.** **Filtering Criteria and Instructions** で `orig_sourcetype` matches `cisco:dnac:issue` を追加します。

**5.** **Add Rule (OR)** をクリックし、`orig_sourcetype` matches `solarwinds:alert:hec` と入力します。

**6.** **Group alerts episodes based on...** で `host` を `subcomponent` に置き換えます。

**7.** デフォルトの **Break Episode** スタンザを **If the flow of events into the episode is paused for** に置き換え、**600 seconds** を使用します。

{{% notice style="info" %}}
ブレーク条件が満たされると、現在のエピソードにはイベントを追加できなくなり、次のNotableイベントで新しいエピソードが開始されます。例: 次のイベントが発生した場合にエピソードをブレーク: message matches **status** `Normal`。このルールは、正常なNotableイベントを受信すると（問題が解決したことを示す）エピソードをブレークします。
{{% /notice %}}

{{% notice style="Info" %}}
フィルタリング条件はこのポリシーが適用されるアラートソースを定義し、グループ化フィールドはエピソードの形成方法を決定します

![Filtering Criteria](../../images/filtering-criteria.png?width=40vw)
{{% / notice %}}

{{% notice style="info" %}}
IT Service Intelligence (ITSI) の Event iQ は、機械学習アルゴリズムを使用してフィールド値を比較し、Notableイベントをエピソードに相関させます。イベントを相関させるための手動属性を定義する代わりに、グループ化ポリシーで使用する正しい属性を自動的に特定できます。ITSI にアラートをオンボードした後、アラートをフィルタリングする条件を設定し、Event iQ を使用して過去のイベントデータの分析に基づいてイベント相関ポリシーを作成できます。

ワークフローで Event iQ を使用すると、自動化されたアラート監視の迅速なセットアップ、アラートノイズの削減、イベントアクションの実行が可能になります。さらに、アルゴリズムは環境のアラートニーズに合わせて継続的にチューニングできます。
{{% /notice %}}

**8.** **Episode Information** を展開します。

* **Episode Title** を **Static Value** に設定し、`Network Issue Impacting: %subcomponent%` と入力します
* **Episode Severity** を **Same as the highest Severity** に設定します
* 右上の **Next** をクリックします

{{% notice style="Info" %}}
エピソードタイトルで %subcomponent% を使用すると、このポリシーで作成されるすべてのエピソードに影響を受けるサイト名が自動的に入力されます

![Episode Information](../../images/episode-information.png?width=40vw)
{{% / notice %}}

**9.** **Action Rules** を設定します。

{{% notice style="info" %}}
集約ポリシー内でアクションルールを設定して、エピソードのアクティベーション条件が満たされたときに自動アクションを実行します。アクションルールはオプションであり、集約ポリシーごとに複数定義できます。
{{% /notice %}}

* ルールを追加: If **all event severities are** でドロップダウンから **Normal** を選択し、**60 seconds** と入力します
* Then **Change severity to** でドロップダウンから **Normal** を選択し、**Change status to** > **Resolved** を選択します
* **Next** をクリックします

{{% notice style="Info" %}}
アクションルールにより、すべての関連アラートが正常に戻ったときにエピソードが自動的に解決され、手動トリアージが削減されます

![Action Rules](../../images/action-rules.png?width=40vw)
{{% / notice %}}

**10.** **Policy Title** に `Network Events by Location` と入力します。Status の **Enabled** をクリックします。**Next** をクリックします。

{{% notice style="Info" %}}
ポリシーをすぐに有効にして、保存後すぐに受信アラートのグループ化を開始するようにします

![Policy Title](../../images/policy-title.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="お疲れ様でした！" %}}
カスタム NEAP がアクティブになりました。同じサイトを共有する Catalyst Center と SolarWinds のアラートは、影響を受けるロケーション名がタイトルに付けられた単一のエピソードにグループ化されます。

次のセクションに進み、エンドツーエンドの設定全体を検証しましょう。
{{% / notice %}}

{{% /notice %}}
