---
title: Application Performance Monitoring (APM)
linkTitle: 4. APM
weight: 4
archetype: chapter
time: 20 minutes
description: このセクションでは、APMを使用してドリルダウンし、問題がどこにあるかを特定します。
---

{{% notice icon="user" style="orange" title="Persona" %}}

あなたは **バックエンド開発者** で、SREによって発見された問題の調査を支援するために呼ばれました。SREはユーザーエクスペリエンスの低下を特定し、その問題の調査をあなたに依頼しています。

{{% /notice %}}

> [!IMPORTANT]
> RUMはクライアント側のビューで、APMはサーバー側のビューです。RUMトレースから対応するAPMトレースへたどることが、エンドツーエンドの可視性を実現する方法であり、バックエンドの問題までドリルダウンする手段です。

{{< webex chat="Pieter Hagen" date="Today • 28/01/2026" seenby="RC" >}}
{{< webex-msg from="PH" name="Pieter Hagen" time="09:42" color="#571bc0" >}}
こんにちはRobertさん、Online Boutiqueの顧客満足度に関する問題をトリアージしました。RUMでページの読み込み時間が遅いことが確認できます。Related Contentを使ってユーザーセッションをバックエンドまで追跡したところ、レイテンシは **paymentservice** から発生しています。
{{< /webex-msg >}}

{{< webex-msg from="PH" name="Pieter Hagen" time="09:43" color="#571bc0" >}}
バックエンドを掘り下げて根本原因を見つけてもらえますか？トレースへのリンクを送ります。
{{< /webex-msg >}}

{{< webex-msg me=true time="09:43" >}}
了解しました。APMとサービスマップを確認します。 👍
{{< /webex-msg >}}
{{< /webex >}}
