---
title: Cisco Catalyst インバウンド通知の設定
linkTitle: 3.1 Cisco Catalyst インバウンド通知の設定
weight: 1
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

ITSI 4.21 には、Cisco Meraki および Catalyst Center アラート用のネイティブデータ統合が含まれています。推奨される方法は、アラートを正規化するために必要な設定が事前構成されているデフォルト接続を有効化することです。デフォルト構成は、お客様固有のユースケースに合わせてカスタマイズできます。

このセクションでは、ロケーション間でイベントを相関できるようにアラートをカスタマイズし、サービスの健全性が正常に戻ったときにエピソードが自動的に解決されるようにステータスマッピングを更新します。

{{% notice title="演習: アラート統合の構成" style="primary" icon="running" %}}

**1.** ITSI で、**Configuration** > **Data Integrations** に移動します。

**2.** **Integrations library** の **Alerts** セクションで、**Cisco Catalyst Center** を選択します。

{{% notice style="Info" %}}
Data Integrations library の Alerts セクションには、Catalyst Center と Meraki 用の事前構築された接続が含まれています

![Data Integrations](../../images/data-integrations-alerts.png?width=40vw)
{{% / notice %}}

**3.** **+ Add Connection** をクリックします。

{{% notice style="Info" %}}
カスタム接続を追加すると、検索、フィールドマッピング、およびスロットリング動作をデフォルトとは独立して制御できます

![Add Connection](../../images/add-connection.png?width=40vw)
{{% / notice %}}

**4.** 名前に `Catalyst Center Alerts` と入力します。以下の検索を使用します

```splunk
index=netops sourcetype="cisco:dnac:issue"
| eval itsi_site = case( isnotnull(SiteNameHierarchy) AND SiteNameHierarchy!="", mvindex(split(SiteNameHierarchy, "/"), 3), isnotnull(DeviceName) AND DeviceName!="", "Store-" . mvindex(split(DeviceName, "-"), 0) )
```

**5.** **Validate** をクリックします

**6.** **Lookback period** を **5 minutes** に設定します

{{% notice style="Info" %}}
検証により、保存前に検索がイベントを返し、フィールドマッピングが正しいことを確認します

![Validate Connection](../../images/validate-connection.png?width=40vw)
{{% / notice %}}

**7.** **Source** を **Coalesce** タイプの **Mapping rule** に更新します

**8.** 最初のフィールドとして `DeviceName` を、2番目のフィールドとして `SiteName` を選択します

**9.** **else use the default value** フィールドに `IssueSpecificEntityValue` と入力します

{{% notice style="Info" %}}
Source フィールドは、ITSI エピソード内でアラートの発生元を識別するために使用されます

![Update Source](../../images/cat-center-notification-config-1.png?width=40vw)
{{% / notice %}}

**10.** **Severity ID** マッピングを **Value case mapping** タイプの **Mapping rule** に更新します

**11.** `IssueStatus` **is equal to (not case sensitive)** を `resolved` に設定し、**then use** を `Normal` に設定します

**12.** 残りの if ステートメントについて、以下の値をマッピングします

`vendor_severity` **is equal to (not case sensitive)** を `P1` に設定し、**then use** を `Critical` に設定します

`vendor_severity` **is equal to (not case sensitive)** を `P2` に設定し、**then use** を `High` に設定します

`vendor_severity` **is equal to (not case sensitive)** を `P3` に設定し、**then use** を `Medium` に設定します

`vendor_severity` **is equal to (not case sensitive)** を `P4` に設定し、**then use** を `Low` に設定します

最後に、**else use this default value** を `Info` に設定します

{{% notice style="Info" %}}
Catalyst Center の重大度値を ITSI の重大度スケールにマッピングして、エピソードに正しい優先度が表示されるようにします

![Severity ID Mapping](../../images/severity-mapping.png?width=40vw)
{{% / notice %}}

**13.** **Title** フィールドを `IssueSpecificSummary` に変更します

**14.** **subcomponent** を `itsi_site` に更新します

**15.** **Run every** を **1 minute** に変更します

**16.** **Service Association** セクションに `NY HQ`、`Store-SJC10`、および `Store-SJC12` を追加します

**17.** **Entity Lookup Field** に `SiteNameHierarchy` を使用します

**18.** **Enable throttling** トグルをオンにします

**19.** **Suppress period** を **5 minutes** ごとに設定します

**20.** 右上の **Preview Results** をクリックします（**注意** プレビューで結果が表示されない場合があります。イベントは **Create a custom NEAP** セクションで確認します）

**21.** **Save and Activate** をクリックします

{{% notice style="Info" %}}
subcomponent フィールドは、各アラートを ITSI 内の対応する Catalyst Center サイトサービスにリンクするものです

![Subcomponent Configuration](../../images/subcomponent-config.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="お疲れ様でした！" %}}
Catalyst Center アラートが、サイトサービスにリンクされた正規化済みの注目すべきイベントとして ITSI に流入するようになりました。

次のセクションでは、ITSI が両方のベンダーからのイベントを相関できるように、SolarWinds を2番目のアラートソースとして追加します。
{{% / notice %}}

{{% /notice %}}
