---
title: Digital Experience (RUM)
linkTitle:  3. Digital Experience (RUM)
weight: 3
archetype: chapter
time: 15 minutes
description: このセクションでは、Splunk RUM を使用してエンドユーザーの視点からアプリケーションのパフォーマンスを監視する方法を理解します。
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは **フロントエンドエンジニア**、もしくはパフォーマンス問題の初期トリアージを任された **SRE** です。Online Boutique アプリケーションで顧客満足度に影響しうる問題が発生している可能性があるため、調査を依頼されました。

{{% /notice %}}

>[!IMPORTANT]
> ここでは、あなたや他の参加者が Online Boutique を利用することで生成された *Real User Monitoring* (**RUM**) データを確認します。目的は、パフォーマンスが芳しくなかったブラウザ、モバイル、またはタブレットのセッションを見つけ出し、トラブルシューティングを開始することです。

{{< webex chat="Bill Grant" date="Today • 28/01/2026" seenby="PH" >}}
{{< webex-msg from="BG" name="Bill Grant" time="09:42" >}}
やあ！Online Boutique アプリケーションで顧客満足度に関わる問題が発生している可能性があるという報告が上がっています。最初のトリアージをして何が起きているか確認してもらえますか？
{{< /webex-msg >}}

{{< webex-msg me=true time="09:43" >}}
了解です。まずは Splunk Observability の RUM をチェックして、ユーザーが何を体験しているか確認してみます。👍
{{< /webex-msg >}}
{{< /webex >}}
