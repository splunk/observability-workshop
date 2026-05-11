---
title: Solarwinds Content Pack のインストール
linkTitle: 4.1 Solarwinds Content Pack のインストール
weight: 1
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px; margin-top: 25px;">
<center>
このセクションでは、SolarWinds Content Pack をインストールおよび設定し、SolarWinds アラートを ITSI に取り込みます。これにより、クロスベンダー相関に必要な2ソースのアラートパイプラインが完成します。
</center>

{{% notice title="演習: Solarwinds Content Pack のインストール" style="primary" icon="running" %}}

**1.** ITSI で、**Configuration** > **Data Integrations** に移動します。

**2.** **Integrations library** の **Alerts** セクションで、**Solarwinds** を選択します。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
SolarWinds Content Pack には、ITSI 用の構築済みフィールドマッピングとアラートテンプレートが含まれています
</div>

![Content Pack for Solarwinds](../../images/solarwinds-content-pack.png?width=40vw)
{{% / notice %}}
</div>

**3.** 接続タイトルに `Solarwinds Alerts` と入力します。

**4.** 検索に以下の SPL を使用します:

```text
index=netops sourcetype="solarwinds:alert:hec"
```

**5.** **Validate** をクリックします。

**6.** **Lookback period** を **5 minutes** に設定します。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
バリデーションにより、接続を保存する前に検索が SolarWinds イベントを返していることを確認できます
</div>

![Validate Connection](../../images/solarwinds-validate.png?width=40vw)
{{% / notice %}}
</div>

**7.** **Signature** を `title` に設定します。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Signature フィールドは各アラートタイプを一意に識別し、ITSI 内での重複排除に使用されます
</div>

![Signature](../../images/solarwinds-signature.png?width=40vw)
{{% / notice %}}
</div>

**8.** **Severity ID** のマッピングを、タイプとして **Value case mapping** を使用する **Mapping rule** に更新します

**9.** `severity_id` **is equal to (not case sensitive)** を `1` に、**then use** を `Normal` に設定します

**10.** 残りの if 文に以下の値をマッピングします:

`severity_id` **is equal to (not case sensitive)** を `2` に、**then use** を `Low` に設定

`severity_id` **is equal to (not case sensitive)** を `3` に、**then use** を `Medium` に設定

`severity_id` **is equal to (not case sensitive)** を `4` に、**then use** を `High` に設定

`severity_id` **is equal to (not case sensitive)** を `5` に、**then use** を `Critical` に設定

最後に、**else use this default value** を `Info` に設定します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
SolarWinds の重大度の値を ITSI の重大度スケールにマッピングし、エピソードに正しい優先度が表示されるようにします
</div>

![Severity ID Mapping](../../images/solarwinds-severity.png?width=40vw)
{{% / notice %}}
</div>

**11.** **subcomponent** を `vendor_region` に更新します。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
subcomponent フィールドは各 SolarWinds アラートを対応するサイトにリンクし、クロスベンダー相関を可能にします
</div>

![Subcomponent](../../images/solarwinds-subcomponent.png?width=40vw)
{{% / notice %}}
</div>

**12.** **additional fields** を展開し、**description** を `signature` に設定します。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
追加フィールドは、ITSI でエピソードを確認する際に表示される追加のコンテキストを提供します
</div>

![Additional Fields](../../images/solarwinds-additional-fields.png?width=40vw)
{{% / notice %}}
</div>

**13.** Schedule を **Run Every Minute** に設定します。

**14.** **Service Association** セクションに `NY HQ`、`Store-SJC10`、`Store-SJC12` を追加します

**15.** **Enable throttling** トグルをオンにします

**16.** **Suppress period** を **5 minutes** ごとに設定します

**17.** 右上の **Preview Results** をクリックします（**注:** プレビューで結果が表示されない場合があります。イベントは **Create a custom NEAP** セクションで確認します）

**18.** **Save and Activate** をクリックします

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
保存前に Preview Results で変換されたフィールドを確認し、マッピングが正しいことを確認します
</div>

![Save and Activate](../../images/solarwinds-save-activate.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="Primary" title="お疲れ様でした！" %}}
<div style="text-align: center;">
SolarWinds アラートが Catalyst Center イベントとともに ITSI に取り込まれるようになりました。両方のソースが正規化され、相関の準備が整いました。

次のセクションでは、両方のベンダーからのアラートをサイトごとに1つのエピソードにグループ化するカスタム NEAP を作成します。
</div>
{{% / notice %}}

{{% /notice %}}
</div>
