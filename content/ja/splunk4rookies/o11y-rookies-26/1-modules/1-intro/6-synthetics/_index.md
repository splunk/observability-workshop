---
title: Digital Experience (Synthetics)
linkTitle: 6. Digital Experience (Synthetics)
archetype: chapter
weight: 6
time: 15 minutes
description: このセクションでは、Splunk Synthetics を使用してアプリケーションのパフォーマンスと可用性を監視する方法を学びます。
---

{{% notice icon="user" style="orange" title="Persona" %}}

再び **SRE** の役割に戻り、Online Boutique のモニタリングを設定するよう依頼されました。アプリケーションが 24 時間 365 日、確実に利用可能でパフォーマンス良く動作していることを保証する必要があります。

{{% /notice %}}

> [!IMPORTANT]
> アプリケーションを 24 時間 365 日監視し、問題が発生した際にアラートを受け取れたら素晴らしいと思いませんか？ そこで活躍するのが Synthetics です。これから、1 分ごとに実行され、Online Boutique を通じた典型的なユーザージャーニーのパフォーマンスと可用性をチェックするシンプルなテストをご紹介します。

{{< webex chat="Bill Grant" date="Today • 28/01/2026" seenby="BG" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
やあ Bill、`paymentservice` の問題が解決できたから、今後の問題が顧客に影響を与える前に検知できるよう、モニタリングを設定するべきだと思うんだ。
{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
Synthetics を使って、1 分ごとに Online Boutique を通じた典型的なユーザージャーニーのパフォーマンスと可用性をチェックするテストを設定することを提案するよ。これなら、何か問題があればすぐにアラートを受け取ることができる。
{{< /webex-msg >}}
{{< /webex >}}
