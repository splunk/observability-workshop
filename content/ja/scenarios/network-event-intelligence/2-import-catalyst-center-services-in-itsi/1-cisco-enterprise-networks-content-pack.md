---
title: Cisco Enterprise Networks Content Pack のインストール
linkTitle: 2.1 Cisco Enterprise Networks Content Pack のインストール
weight: 1
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

このセクションでは、Cisco ネットワークインフラストラクチャ向けの事前構築済みサービス、KPI、およびデータ統合を提供する Cisco Enterprise Networks Content Pack をインストールします。

{{% exercise %}}
**1.** ITSI で **Configuration -> Data Integrations** に移動します

**2.** Data Integrations の下のタブで **Content Library** を選択します

{{% notice style="Info" %}}
ここでは、Splunk App for Content Packs で利用可能なすべての標準統合を確認できます

![Data Integrations](../../images/content-library.png?width=40vw)
{{% / notice %}}

**3.** **Content Pack for Cisco Enterprise Networks** を選択し、**Proceed** をクリックします

{{% notice style="Info" %}}
このページでは、コンテンツパックで利用可能なものの概要を確認できます

![Content Pack for Cisco Enterprise Networks](../../images/content-pack-overview.png?width=40vw)
{{% / notice %}}

**5.** **Add all 14 objects** が有効になっていることを確認します

**6.** **Import As Enabled** トグルを有効にします

**重要: Add a prefix to your new objects セクションには prefix を入力しないでください**

**7.** **Install Selected** をクリックします

{{% notice style="Info" %}}
Install Selected をクリックする前に、Add all 14 objects と Import As Enabled の両方がオンになっていることを確認してください

![Install Selected](../../images/install-selected.png?width=40vw)
{{% / notice %}}

**8.** **Install** をクリックします。

{{% notice style="Info" %}}
本番環境では、大きな変更を加える前にバックアップを取得することがベストプラクティスです

![Install](../../images/install-confirm.png?width=40vw)
{{% / notice %}}

**9.** インストールが完了したことを確認します。

{{% notice style="Info" %}}
サマリーですべてのオブジェクトが正常にインストールされたことが確認できます

![Installation Complete](../../images/installation-complete.png?width=40vw)
{{% / notice %}}

{{% notice style="Primary" title="お疲れ様でした！" %}}
Cisco Enterprise Networks Content Pack のインストールが完了しました。

次のセクションでは、このコンテンツパックを使用して Catalyst Center のサイトを ITSI のサービスとして自動的にインポートする方法を確認します。

**Configure Services** をクリックして、ワークショップの次のセクションに進んでください。
{{% / notice %}}

{{% / exercise %}}
