---
title: Syntheticsによるプロアクティブなテスト
linkTitle: 5. プロアクティブなテスト
archetype: chapter
weight: 5
time: 15 minutes
description: このセクションでは、Splunk Syntheticsを使用してアプリケーションのパフォーマンスと可用性を監視する方法を学びます。
---

{{% notice icon="user" style="orange" title="ペルソナ" %}}

**SRE** の役割に戻り、Astronomy Shopのモニタリングを設定するよう依頼されました。アプリケーションが24時間365日利用可能で、良好なパフォーマンスを維持していることを確認する必要があります。

{{% /notice %}}

> [!IMPORTANT]
> アプリケーションを24時間365日モニタリングし、問題が発生したときにアラートを受け取ることができたら素晴らしいと思いませんか？ここでSyntheticsの出番です。5分ごとに実行され、Astronomy Shopにおける典型的なユーザージャーニーのパフォーマンスと可用性をチェックするシンプルなテストをお見せします。

{{< webex chat="Bill Grant" date="Today • 28/01/2026" seenby="BG" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
やあBill、`payment`サービスの問題を解決したところだけど、今後の問題がお客様に影響を与える前にキャッチできるよう、モニタリングを設定すべきだと思うんだ。
{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
Syntheticsを使って、5分ごとに実行されるテストを設定し、Astronomy Shopにおける典型的なユーザージャーニーのパフォーマンスと可用性をチェックすることを提案するよ。これにより、問題があればすぐにアラートを受け取ることができる。
{{< /webex-msg >}}
{{< /webex >}}
