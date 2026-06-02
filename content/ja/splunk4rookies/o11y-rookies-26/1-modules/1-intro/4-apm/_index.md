---
title: Application Performance Monitoring (APM)
linkTitle: 4. APM
weight: 4
archetype: chapter
time: 20 minutes
description: このセクションでは、APM を使用してドリルダウンし、問題がどこにあるかを特定します。
---

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは **バックエンド開発者** で、SRE が発見した問題の調査を依頼されています。SRE はユーザーエクスペリエンスの低下を確認しており、その問題の調査をあなたに依頼してきました。

{{% /notice %}}

> [!IMPORTANT]
> RUM はクライアント側の視点を提供し、APM はサーバー側の視点を提供します。RUM のトレースから対応する APM のトレースへとたどっていく操作こそが、エンドツーエンドの可視性そのものであり、バックエンドの問題へとドリルダウンしていく方法です。

{{< webex chat="Pieter Hagen" date="Today • 28/01/2026" seenby="RC" >}}
{{< webex-msg from="PH" name="Pieter Hagen" time="09:42" color="#571bc0" >}}
Robert さん、お疲れさまです。Online Boutique で顧客満足度に関わる問題のトリアージをしました。RUM ではページの読み込み時間が悪化しています。Related Content を使ってユーザーセッションをバックエンドまで追跡したところ、レイテンシーは **paymentservice** から発生しているようです。
{{< /webex-msg >}}

{{< webex-msg from="PH" name="Pieter Hagen" time="09:43" color="#571bc0" >}}
バックエンドを掘り下げて、根本原因を見つけてもらえますか？トレースのリンクを送りますね。
{{< /webex-msg >}}

{{< webex-msg me=true time="09:43" >}}
了解です。APM とサービスマップを確認します。👍
{{< /webex-msg >}}
{{< /webex >}}
