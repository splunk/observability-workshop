---
title: Solarwinds Content Pack のインストール
linkTitle: 4.1 Solarwinds Content Pack のインストール
weight: 1
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

このセクションでは、SolarWinds Content Pack をインストールおよび設定して、SolarWinds アラートを ITSI に取り込みます。これにより、クロスベンダー相関に必要な2ソースのアラートパイプラインが完成します。

{{% notice title="演習: Solarwinds Content Pack のインストール" style="primary" icon="running" %}}

**1.** ITSI で、**Configuration** > **Data Integrations** に移動します。

**2.** **Integrations library** の **Alerts** セクションで、**Solarwinds** を選択します。

{{% notice style="Info" %}}
SolarWinds Content Pack には、ITSI 用の事前構築済みフィールドマッピングとアラートテンプレートが含まれています

![Content Pack for Solarwinds](../../images/solarwinds-content-pack.png?width=40vw)
{{% / notice %}}

**3.** 接続タイトルに `Solarwinds Alerts` と入力します。

**4.** 検索に以下の SPL を使用します:

```text
index=netops sourcetype="solarwinds:alert:hec"
```

**5.** **Validate** をクリックします。

**6.** **Lookback period** を **5 minutes** に設定します。

{{% notice style="Info" %}}
検証により、接続を保存する前に検索が SolarWinds イベントを返していることを確認します

![Validate Connection](../../images/solarwinds-validate.png?width=40vw)
{{% / notice %}}

**7.** **Signature** を `title` に設定します。

{{% notice style="Info" %}}
Signature フィールドは各アラートタイプを一意に識別し、ITSI 内での重複排除に使用されます

![Signature](../../images/solarwinds-signature.png?width=40vw)
{{% / notice %}}

**8.** **Severity ID** のマッピングを、タイプとして **Value case mapping** を使用する **Mapping rule** に更新します

**9.** `severity_id` **is equal to (not case sensitive)** を `1` に設定し、**then use** を `Normal` に設定します

**10.** if 文の残りの部分について、以下の値をマッピングします:

`severity_id` **is equal to (not case sensitive)** を `2` に設定し、**then use** を `Low` に設定します

`severity_id` **is equal to (not case sensitive)** を `3` に設定し、**then use** を `Medium` に設定します

`severity_id` **is equal to (not case sensitive)** を `4` に設定し、**then use** を `High` に設定します

`severity_id` **is equal to (not case sensitive)** を `5` に設定し、**then use** を `Critical` に設定します

最後に、**else use this default value** を `Info` に設定します

{{% notice style="Info" %}}
SolarWinds の重要度の値を ITSI の重要度スケールにマッピングして、エピソードに正しい優先度が表示されるようにします

![Severity ID Mapping](../../images/solarwinds-severity.png?width=40vw)
{{% / notice %}}

**11.** **subcomponent** を `vendor_region` に更新します。

{{% notice style="Info" %}}
subcomponent フィールドは、各 SolarWinds アラートを対応するサイトにリンクし、クロスベンダー相関を可能にします

![Subcomponent](../../images/solarwinds-subcomponent.png?width=40vw)
{{% / notice %}}

**12.** **additional fields** を展開し、**description** を `signature` に設定します。

{{% notice style="Info" %}}
追加フィールドは、ITSI でエピソードを確認する際に表示される追加のコンテキストを提供します

![Additional Fields](../../images/solarwinds-additional-fields.png?width=40vw)
{{% / notice %}}

**13.** スケジュールを **Run Every Minute** に設定します。

**14.** **Service Association** セクションに `NY HQ`、`Store-SJC10`、および `Store-SJC12` を追加します

**15.** **Enable throttling** トグルをオンにします

**16.** **Suppress period** を **5 minutes** ごとに設定します

**17.** 右上の **Preview Results** をクリックします（**注意:** プレビューで結果が表示されない場合があります。イベントは **Create a custom NEAP** セクションで確認します）

**18.** **Save and Activate** をクリックします

{{% notice style="Info" %}}
保存する前に Preview Results で変換されたフィールドを確認し、マッピングが正しいことを確認します

![Save and Activate](../../images/solarwinds-save-activate.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="お疲れ様でした！" %}}
SolarWinds アラートが Catalyst Center イベントとともに ITSI に流入するようになりました。両方のソースが正規化され、相関の準備が整いました。

次のセクションでは、両方のベンダーからのアラートをサイトごとに1つのエピソードにグループ化するカスタム NEAP を構築します。
{{% / notice %}}

{{% /notice %}}
