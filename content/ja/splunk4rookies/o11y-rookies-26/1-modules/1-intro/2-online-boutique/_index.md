---
title: Let's go shopping 💶
linkTitle: 2. Shopping at the Online Boutique
weight: 2
time: 5 minutes
description: Online Boutique Web アプリケーションを操作して、Splunk Observability Cloud 用のデータを生成します。
---

{{< presenter title="Timing" >}}
受講者がこのセクションを終えるまで、約 10 分を見込んでください。
{{< /presenter >}}

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは**おしゃれな都市生活のプロフェッショナル**で、有名な Online Boutique で次に買う流行のアイテムを探しています。あなたは、Online Boutique がヒップスター御用達のショップだと聞いています。

{{% /notice %}}

{{% exercise title="Retail Therapy" %}}

* アプリケーションはすでにデプロイ済みです。インストラクターが Online Boutique Web サイトへのリンクを提供します（例: `http://<s4r-workshop-i-xxx.splunk>.show:81/`）。ポート 81 が到達できない場合は、ポート 80 および 443 も利用可能です。
* Online Boutique を閲覧し、カートにいくつかの商品を追加して、チェックアウトを完了させてください。
* アプリケーションに意図的に組み込まれたパフォーマンス問題を表面化させるため、これを少なくとも 3〜5 回繰り返してください。

{{< tabs >}}
{{% tab title="Question" %}}

**チェックアウトの一連のプロセスは、本来であればミリ秒で完了するはずです。チェックアウトの動作で何か気づいたことはありましたか？**

{{% /tab %}}
{{% tab title="Answer" %}}

**ときどき遅い！** 🐌

{{% /tab %}}
{{< /tabs >}}

* チェックアウト処理が遅い場合、ユーザーにストレスを与える体験になります。これは顧客満足度に直接影響するため、私たちは優先的にこの問題を調査・解決する必要があります。

{{% image src="images/shop.png" align="center" %}}

{{% /exercise %}}

それでは次のページに進み、Splunk Observability Cloud を使い始めて、**Splunk Real User Monitoring (RUM)** でデータがどのように見えるかを確認していきましょう。
