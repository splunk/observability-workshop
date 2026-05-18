---
title: Cisco Catalyst インバウンド通知の設定
linkTitle: 3.1 Cisco Catalyst インバウンド通知の設定
weight: 1
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px; margin-top: 25px;">
<center>
ITSI 4.21 には、Cisco Meraki および Catalyst Center アラート用のネイティブデータインテグレーションが含まれています。推奨される方法は、アラートを正規化するために必要な設定が事前に構成されたデフォルトの接続を有効にすることです。デフォルトの構成は、お客様固有のユースケースに合わせてカスタマイズできます。

このセクションでは、ロケーション間でイベントを相関できるようにアラートをカスタマイズし、サービスの正常性が正常に戻ったときにエピソードが自動的に解決されるようにステータスマッピングを更新します。
</center>

{{% notice title="演習: アラートインテグレーションの設定" style="primary" icon="running" %}}

**1.** ITSI で、**Configuration** > **Data Integrations** に移動します。

**2.** **Integrations library** の **Alerts** セクションで、**Cisco Catalyst Center** を選択します。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Data Integrations ライブラリの Alerts セクションには、Catalyst Center と Meraki 用の事前構築済み接続が含まれています
</div>

![Data Integrations](../../images/data-integrations-alerts.png?width=40vw)
{{% / notice %}}
</div>

**3.** **+ Add Connection** をクリックします。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
カスタム接続を追加すると、サーチ、フィールドマッピング、スロットリングの動作をデフォルトとは独立して制御できます
</div>

![Add Connection](../../images/add-connection.png?width=40vw)
{{% / notice %}}
</div>

**4.** 名前に `Catalyst Center Alerts` と入力します。以下のサーチを使用します:

```splunk
index=netops sourcetype="cisco:dnac:issue"  
| eval itsi_site = case( isnotnull(SiteNameHierarchy) AND SiteNameHierarchy!="", mvindex(split(SiteNameHierarchy, "/"), 3), isnotnull(DeviceName) AND DeviceName!="", "Store-" . mvindex(split(DeviceName, "-"), 0) ) 
```

**5.** **Validate** をクリックします

**6.** **Lookback period** を **5 minutes** に設定します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
検証により、保存前にサーチがイベントを返し、フィールドマッピングが正しいことが確認されます
</div>

![Validate Connection](../../images/validate-connection.png?width=40vw)
{{% / notice %}}
</div>

**7.** **Source** を **Mapping rule** に更新し、タイプに **Coalesce** を使用します

**8.** 最初のフィールドとして `DeviceName` を、2番目のフィールドとして `SiteName` を選択します

**9.** **else use the default value** フィールドに `IssueSpecificEntityValue` と入力します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Source フィールドは、ITSI エピソード内でアラートの発生元を識別するために使用されます
</div>

![Update Source](../../images/cat-center-notification-config-1.png?width=40vw)
{{% / notice %}}
</div>

**10.** **Severity ID** マッピングを **Mapping rule** に更新し、タイプとして **Value case mapping** を使用します

**11.** `IssueStatus` **is equal to (not case sensitive)** を `resolved` に設定し、**then use** を `Normal` にします

**12.** if ステートメントの残りの部分に以下の値をマッピングします:

`vendor_severity` **is equal to (not case sensitive)** を `P1` に設定し、**then use** を `Critical` にします

`vendor_severity` **is equal to (not case sensitive)** を `P2` に設定し、**then use** を `High` にします

`vendor_severity` **is equal to (not case sensitive)** を `P3` に設定し、**then use** を `Medium` にします

`vendor_severity` **is equal to (not case sensitive)** を `P4` に設定し、**then use** を `Low` にします

最後に、**else use this default value** を `Info` に設定します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
Catalyst Center の重要度の値を ITSI の重要度スケールにマッピングして、エピソードに正しい優先度が表示されるようにします
</div>

![Severity ID Mapping](../../images/severity-mapping.png?width=40vw)
{{% / notice %}}
</div>

**13.** **Title** フィールドを `IssueSpecificSummary` に変更します

**14.** **subcomponent** を `itsi_site` に更新します

**15.** **Run every** を **1 minute** に変更します

**16.** **Service Association** セクションに `NY HQ`、`Store-SJC10`、`Store-SJC12` を追加します

**17.** **Entity Lookup Field** に `SiteNameHierarchy` を使用します

**18.** **Enable throttling** トグルをオンにします

**19.** **Suppress period** を **5 minutes** ごとに設定します

**20.** 右上の **Preview Results** をクリックします（**注:** プレビューで結果が表示されない場合があります。イベントは **Create a custom NEAP** セクションで確認します）

**21.** **Save and Activate** をクリックします

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
subcomponent フィールドは、各アラートを ITSI 内の対応する Catalyst Center サイトサービスにリンクするものです
</div>

![Subcomponent Configuration](../../images/subcomponent-config.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="Primary" title="よくできました！" %}}
<div style="text-align: center;">
Catalyst Center のアラートが、正規化されたNotable Eventとしてサイトサービスにリンクされた状態で ITSI に取り込まれるようになりました。

次のセクションでは、ITSI が両方のベンダーからのイベントを相関できるように、SolarWinds を2番目のアラートソースとして追加します。
</div>
{{% / notice %}}

{{% /notice %}}
</div>
