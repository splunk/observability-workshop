---
title: Logs
linkTitle: 5. Logs
weight: 5
archetype: chapter
time: 20 minutes
description: このセクションでは、Log Observer を使用してドリルダウンし、問題が何であるかを特定します。
---

{{% notice icon="user" style="orange" title="Persona" %}}

引き続き **バックエンド開発者** として、アプリケーションのログを調査し、問題の根本原因を特定します。

{{% /notice %}}

> [!IMPORTANT]
> **APM** トレースに関連するコンテンツ (logs) を使用して、ここからは **Logs** を活用してさらにドリルダウンし、問題の正確な内容を把握します。Related Content は、あるコンポーネントから別のコンポーネントへジャンプできる強力な機能で、**metrics**、**traces**、**logs** で利用できます。

{{< webex chat="Robert Castley" date="Today • 28/01/2026" seenby="PH" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
APM を確認したところ、問題は paymentservice にあることが確認できました。トレースに大きなレイテンシーのスパイクが発生しています。
{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
Related Content を使ってログにジャンプし、レイテンシースパイクの原因となるエラーや異常を見つけられないか確認してみます。
{{< /webex-msg >}}
{{< /webex >}}
