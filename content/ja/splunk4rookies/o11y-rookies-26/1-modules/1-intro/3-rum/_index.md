---
title: Digital Experience (RUM)
linkTitle: 3 . Digital Experience (RUM)
weight: 3
archetype: chapter
time: 15 minutes
description: このセクションでは、Splunk RUMを使用してエンドユーザーの視点からアプリケーションのパフォーマンスをモニタリングする方法を説明します。
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

あなたは **フロントエンドエンジニア** 、またはパフォーマンス問題の最初のトリアージを担当する **SRE** です。Online Boutiqueアプリケーションの顧客満足度に関する潜在的な問題を調査するよう依頼されました。

{{% /notice %}}

>[!IMPORTANT]
> ここでは、Online Boutiqueを使用しているあなたや他の参加者によって生成された *Real User Monitoring*（**RUM**）データを確認します。目的は、パフォーマンスが低下したブラウザ、モバイル、またはタブレットのセッションを見つけ、トラブルシューティングプロセスを開始することです。

{{< webex chat="Bill Grant" date="Today • 28/01/2026" seenby="PH" >}}
{{< webex-msg from="BG" name="Bill Grant" time="09:42" >}}
やあ！Astronomy shopアプリケーションで顧客満足度に問題がある可能性があるという報告が来ています。最初のトリアージをして、何が起きているか確認してもらえますか？
{{< /webex-msg >}}

{{< webex-msg me=true time="09:43" >}}
了解です。まずSplunk ObservabilityのRUMを確認して、ユーザーが何を体験しているか見てみます。👍
{{< /webex-msg >}}
{{< /webex >}}
