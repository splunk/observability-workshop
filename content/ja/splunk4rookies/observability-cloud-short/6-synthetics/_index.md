---
title: Digital Experience (Synthetics)
linkTitle: 6. Digital Experience (Synthetics)
archetype: chapter
weight: 6
time: 15 minutes
description: このセクションでは、Splunk Synthetics を使用してアプリケーションのパフォーマンスと可用性を監視する方法を学びます。
---

{{% notice icon="user" style="orange" title="Persona" %}}

再び **SRE** の帽子をかぶり、Online Boutique の監視をセットアップするように依頼されました。アプリケーションが 24 時間 365 日、可用性を保ち、良好なパフォーマンスを発揮していることを確認する必要があります。

{{% /notice %}}

> [!IMPORTANT]
> アプリケーションを 24 時間 365 日監視し、問題が発生したときにアラートを受け取ることができたら素晴らしいと思いませんか？そこで Synthetics の出番です。1 分ごとに実行され、Online Boutique の典型的なユーザージャーニーのパフォーマンスと可用性をチェックするシンプルなテストをご紹介します。

{{< webex chat="Bill Grant" date="Today • 28/01/2026" seenby="BG" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
ねえ Bill、`paymentservice` の問題を解決できたから、今後の問題が顧客に影響を与える前に検知できるよう、監視をセットアップすべきだと思うんだ。
{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
Synthetics を使って、1 分ごとに実行され、Online Boutique の典型的なユーザージャーニーのパフォーマンスと可用性をチェックするテストをセットアップすることを提案するよ。これで、何か問題があればすぐにアラートを受け取れるようになるんだ。
{{< /webex-msg >}}
{{< /webex >}}
