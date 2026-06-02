---
title: Digital Experience (RUM)
linkTitle:  3. Digital Experience (RUM)
weight: 3
archetype: chapter
time: 15 minutes
description: このセクションでは、Splunk RUM を使用してエンドユーザーの視点からアプリケーションのパフォーマンスを監視する方法について学びます。
---

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは **フロントエンドエンジニア**、もしくはパフォーマンス問題のファーストトリアージを担当する **SRE** です。Online Boutique アプリケーションで顧客満足度に関わる問題が発生している可能性があるため、その調査を依頼されています。

{{% /notice %}}

>[!IMPORTANT]
> ここでは、あなたや他の参加者が Online Boutique を利用した際に生成された *Real User Monitoring*（**RUM**）データを確認していきます。目的は、パフォーマンスが低下したブラウザ・モバイル・タブレットのセッションを見つけ出し、トラブルシューティングのプロセスを開始することです。

{{< webex chat="Bill Grant" date="Today • 28/01/2026" seenby="PH" >}}
{{< webex-msg from="BG" name="Bill Grant" time="09:42" >}}
お疲れさま！Online Boutique アプリケーションで顧客満足度に関わる問題が発生している可能性があるとの報告が来ています。ファーストトリアージをして、何が起きているか確認してもらえますか？
{{< /webex-msg >}}

{{< webex-msg me=true time="09:43" >}}
了解です。まずは Splunk Observability で RUM を確認して、ユーザーがどのような体験をしているか見てみます。👍
{{< /webex-msg >}}
{{< /webex >}}
