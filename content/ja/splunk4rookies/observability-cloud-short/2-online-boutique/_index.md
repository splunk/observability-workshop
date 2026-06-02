---
title: ショッピングに出かけましょう 💶
linkTitle: 2. Online Boutiqueでのショッピング
weight: 2
time: 5 minutes
description: Online Boutique Web アプリケーションを操作して、Splunk Observability Cloud 用のデータを生成します。
---

{{< presenter title="Timing" >}}
このセクションを参加者が完了するまで約10分を確保してください。
{{< /presenter >}}

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは**おしゃれな都会のプロフェッショナル**で、有名な Online Boutique ショップで次の目新しいアイテムを買いたいと思っています。Online Boutique は、ヒップスターのニーズを満たす場所だと聞いています。

{{% /notice %}}

{{% exercise title="Retail Therapy" %}}

* アプリケーションは事前にデプロイされており、インストラクターが Online Boutique Web サイトへのリンクを提供します（例：`http://<s4r-workshop-i-xxx.splunk>.show:81/`）。ポート 81 にアクセスできない場合は、ポート 80 および 443 も利用可能です。
* Online Boutique を閲覧し、いくつかのアイテムをカートに追加して、チェックアウトを完了してください。
* アプリケーションに意図的に組み込まれているパフォーマンスの問題を表面化させるため、これを少なくとも3〜5回繰り返してください。

{{< tabs >}}
{{% tab title="Question" %}}

**チェックアウトプロセス全体は、本来ミリ秒しかかからないはずです。チェックアウトプロセスについて何か気付いたことはありますか？**

{{% /tab %}}
{{% tab title="Answer" %}}

**時々遅い！** 🐌

{{% /tab %}}
{{< /tabs >}}

* チェックアウトプロセスが遅いと、ユーザーにフラストレーションを与える体験を生み出します。これは顧客満足度に直接影響するため、問題の調査と解決を優先すべきです。

{{% image src="images/shop.png" align="center" %}}

{{% /exercise %}}

次のページに進み、Splunk Observability Cloud の使用を開始して、**Splunk Real User Monitoring (RUM)** でデータがどのように表示されるかを見ていきましょう。
