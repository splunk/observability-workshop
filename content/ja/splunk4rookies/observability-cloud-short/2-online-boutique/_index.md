---
title: ショッピングに出かけましょう 💶
linkTitle: 2. Online Boutique でお買い物
weight: 2
time: 5 minutes
description: Online Boutique ウェブアプリケーションを操作して、Splunk Observability Cloud 用のデータを生成します。
---

{{< presenter title="Timing" >}}
Allow ~10 minutes for attendees to finish this section.
{{< /presenter >}}

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは**流行に敏感な都会のプロフェッショナル**です。有名な Online Boutique ショップで次のおしゃれアイテムを購入したいと思っています。Online Boutique は、あらゆるトレンドニーズに応えてくれる場所だと聞いています。

> [!splunk] この演習の目的は、Online Boutique ウェブアプリケーションを操作することです。これは Splunk Observability Cloud の機能を実演するために使用されるサンプルアプリケーションです。このアプリケーションはシンプルな EC サイトで、商品の閲覧、カートへの追加、そしてチェックアウトができます。いくつかの問題を体験し、生成したデータを使用してその問題の根本原因を特定します。

{{% /notice %}}

{{% notice style="green" icon="running" title="演習 - ショッピングに出かけましょう" %}}

* アプリケーションはデプロイ済みです。インストラクターが Online Boutique ウェブサイトへのリンクを提供します（例: `http://<s4r-workshop-i-xxx.splunk>.show:81/`）。ポート 81 に接続できない場合は、ポート 80 および 443 も利用可能です。
* Online Boutique を閲覧し、いくつかの商品をカートに追加して、チェックアウトを完了してください。
* アプリケーションに意図的に組み込まれたパフォーマンスの問題を表面化させるために、これを少なくとも 3〜5 回繰り返してください。

---

{{< tabs >}}
{{% tab title="質問" %}}

**チェックアウトプロセス全体はミリ秒単位で完了するはずです。チェックアウトプロセスで何か気づいたことはありましたか？**

{{% /tab %}}
{{% tab title="回答" %}}

**遅い！** 🐌

{{% /tab %}}
{{< /tabs >}}

* チェックアウトプロセスが遅いと、ユーザー体験にフラストレーションを与えます。これは顧客満足度に直接影響するため、問題の調査と解決を優先すべきです。

![Online Boutique](images/shop.png)

{{% /notice %}}

次のページに進み、Splunk Observability Cloud の使用を開始して、**Splunk Real User Monitoring (RUM)** でデータがどのように表示されるかを確認しましょう。
