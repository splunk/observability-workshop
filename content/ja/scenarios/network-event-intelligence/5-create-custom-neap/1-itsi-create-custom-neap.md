---
title: ITSI カスタム NEAP の作成
linkTitle: 5.1 ITSI カスタム NEAP の作成
weight: 1
time: 10 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px; margin-top: 25px;">
<center>
前のステップで Catalyst Center と Solarwinds のインバウンド通知ルールを設定したため、まもなくこれらのソースに対してエピソードが生成されるはずです。ITSI がデフォルトの集約ポリシーを適用していることに気づくかもしれません。デフォルトポリシーはアラートをソース別にグループ化することで、迅速な集約値を提供します。しかし、このデータセットではエピソードをロケーション別にグループ化したいと考えています。これにより、Catalyst Center と SolarWinds のアラート間の相関が可能になります。これは ITSI イベント管理の差別化機能です。
</center>

{{% notice title="演習: カスタム NEAP の作成" style="primary" icon="running" %}}

**1.** **Alerts and Episodes** に移動します。最近作成されたエピソードを確認します。アラートのグループ化に **Default Aggregation Policy** が使用されていることに注目してください。この環境のブレークシナリオは30分サイクル（15分間正常、15分間異常）で動作するため、エピソードが表示されるまで最大15分かかる場合があります。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Alerts and Episodes ビューには、現在のすべてのNotableイベントと、それらがグループ化されたエピソードが表示されます
</div>

![Alerts and Episodes](../../images/alerts-and-episodes.png?width=40vw)
{{% / notice %}}
</div>

**2.** **Configuration** > **Event Management** > **Notable Event Aggregation Policies** に移動します。

**3.** 右上の **Create Notable Event Aggregation Policy** をクリックします。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
ITSI にはいくつかの組み込みポリシーが含まれています。ここでは、複数のベンダーからのネットワークサイトアラートをグループ化するための新しいポリシーを作成します
</div>

![Create NEAP](../../images/create-neap.png?width=40vw)
{{% / notice %}}
</div>

**4.** **Filtering Criteria and Instructions** で `orig_sourcetype` matches `cisco:dnac:issue` を追加します。

**5.** **Add Rule (OR)** をクリックし、`orig_sourcetype` matches `solarwinds:alert:hec` を入力します。

**6.** **Group alerts episodes based on...** で `host` を `subcomponent` に置き換えます。

**7.** デフォルトの **Break Episode** スタンザを **If the flow of events into the episode is paused for** に置き換え、**600 seconds** を使用します。

{{% notice style="info" %}}
ブレーク条件が満たされると、現在のエピソードにはイベントを追加できなくなり、次のNotableイベントから新しいエピソードが開始されます。例: 次のイベントが発生した場合にエピソードをブレーク: message matches **status** `Normal`。このルールは、正常なNotableイベントを受信すると（問題が解決されたことを示す）、エピソードをブレークします。
{{% /notice %}}

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
フィルタリング条件は、このポリシーが適用されるアラートソースを定義し、グループ化フィールドはエピソードの形成方法を決定します
</div>

![Filtering Criteria](../../images/filtering-criteria.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="info" %}}
IT Service Intelligence（ITSI）の Event iQ は、機械学習アルゴリズムを使用してフィールド値を比較し、Notableイベントをエピソードに相関させます。イベントを相関させるための手動属性を定義する代わりに、グループ化ポリシーで使用する正しい属性を自動的に識別できます。ITSI にアラートをオンボードした後、アラートをフィルタリングする条件を設定し、Event iQ を使用して履歴イベントデータの分析に基づくイベント相関ポリシーを作成できます。

ワークフローで Event iQ を使用すると、自動化されたアラート監視の迅速なセットアップ、アラートノイズの削減、イベントアクションの実行が可能になります。さらに、アルゴリズムは環境のアラートニーズに合わせて継続的にチューニングできます。
{{% /notice %}}

**8.** **Episode Information** を展開します。

* **Episode Title** を **Static Value** に設定し、`Network Issue Impacting: %subcomponent%` と入力します
* **Episode Severity** を **Same as the highest Severity** に設定します
* 右上の **Next** をクリックします

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
エピソードタイトルで %subcomponent% を使用すると、このポリシーで作成されるすべてのエピソードに影響を受けるサイト名が自動的に入力されます
</div>

![Episode Information](../../images/episode-information.png?width=40vw)
{{% / notice %}}
</div>

**9.** **Action Rules** を設定します。

{{% notice style="info" %}}
集約ポリシー内にアクションルールを設定して、エピソードのアクティベーション条件が満たされたときに自動アクションを実行します。アクションルールはオプションであり、集約ポリシーごとに複数定義できます。
{{% /notice %}}

* ルールを追加: If **all event severities are** でドロップダウンから **Normal** を選択し、**60 seconds** を入力します
* Then **Change severity to** でドロップダウンから **Normal** を選択し、**Change status to** > **Resolved** を選択します
* **Next** をクリックします

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
アクションルールにより、すべての関連アラートが正常に戻ったときにエピソードが自動的に解決され、手動トリアージが削減されます
</div>

![Action Rules](../../images/action-rules.png?width=40vw)
{{% / notice %}}
</div>

**10.** **Policy Title** に `Network Events by Location` と入力します。Status の **Enabled** をクリックします。**Next** をクリックします。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
ポリシーをすぐに有効にして、保存後すぐに受信アラートのグループ化を開始するようにします
</div>

![Policy Title](../../images/policy-title.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="Primary" title="お疲れ様でした！" %}}
<div style="text-align: center;">
カスタム NEAP がアクティブになりました。同じサイトを共有する Catalyst Center と SolarWinds のアラートは、影響を受けるロケーション名がタイトルに付いた単一のエピソードにグループ化されます。

次のセクションに進んで、エンドツーエンドの設定全体を検証しましょう。
</div>
{{% / notice %}}

{{% /notice %}}
</div>
