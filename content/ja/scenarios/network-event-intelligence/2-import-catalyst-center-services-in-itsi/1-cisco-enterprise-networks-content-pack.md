---
title: Cisco Enterprise Networks Content Pack のインストール
linkTitle: 2.1 Cisco Enterprise Networks Content Pack のインストール
weight: 1
time: 5 minutes
authors: ["Chris Putnam", "Sam Scudere-Weiss", "Tim Hard"]
---

<div style="max-width: 80%; margin: 0 auto; font-size: 18px; margin-top: 25px;">
<center>
このセクションでは、Cisco ネットワークインフラストラクチャ向けの事前構築済みサービス、KPI、およびデータ統合を提供する Cisco Enterprise Networks Content Pack をインストールします。
</center>

{{% notice title="演習: Cisco Enterprise Networks Content Pack のインストール" style="primary" icon="running" %}}
**1.** ITSI で **Configuration -> Data Integrations** に移動します

**2.** Data Integrations の下にあるタブから **Content Library** を選択します

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
ここでは、Splunk App for Content Packs で利用可能なすべてのすぐに使える統合を確認できます
</div>

![Data Integrations](../../images/content-library.png?width=40vw)
{{% / notice %}}
</div>

**3.** **Content Pack for Cisco Enterprise Networks** を選択し、**Proceed** をクリックします

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
このページでは、Content Pack で利用可能な内容の概要を確認できます
</div>

![Content Pack for Cisco Enterprise Networks](../../images/content-pack-overview.png?width=40vw)
{{% / notice %}}
</div>

**5.** **Add all 14 objects** が有効になっていることを確認します

**6.** **Import As Enabled** トグルを有効にします

**重要: Add a prefix to your new objects セクションにプレフィックスを入力しないでください**

**7.** **Install Selected** をクリックします

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
**Install Selected** をクリックする前に、Add all 14 objects と Import As Enabled の両方がオンになっていることを確認してください
</div>

![Install Selected](../../images/install-selected.png?width=40vw)
{{% / notice %}}
</div>

**8.** **Install** をクリックします。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
本番環境では、大きな変更を行う前にバックアップを取ることがベストプラクティスです
</div>

![Install](../../images/install-confirm.png?width=40vw)
{{% / notice %}}
</div>

**9.** インストールが完了したことを確認します。

<div style="max-width: 60%; margin: 0 auto;">
{{% notice style="Info" %}}
<div style="text-align: center;">
サマリーにすべてのオブジェクトが正常にインストールされたことが表示されます
</div>

![Installation Complete](../../images/installation-complete.png?width=40vw)
{{% / notice %}}
</div>

{{% notice style="Primary" title="お疲れ様でした!" %}}
<div style="text-align: center;">
Cisco Enterprise Networks Content Pack のインストールが完了しました！

次のセクションでは、Content Pack を使用して Catalyst Center Sites を ITSI のサービスとして自動的にインポートする方法を確認します。

**Configure Services** をクリックして、ワークショップの次のセクションに進んでください。
</div>
{{% / notice %}}

{{% / notice %}}
</div>
