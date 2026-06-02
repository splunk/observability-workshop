---
title: Logs
linkTitle: 5. Logs
weight: 5
archetype: chapter
time: 20 minutes
description: このセクションでは、Log Observer を使用して問題をドリルダウンし、何が問題なのかを特定します。
---

{{% notice icon="user" style="orange" title="Persona" %}}

引き続き **back-end developer** の役割で、アプリケーションのログを調査して問題の根本原因を特定する必要があります。

{{% /notice %}}

> [!IMPORTANT]
> **APM** トレースに関連するコンテンツ（ログ）を使用して、これから **Logs** を使ってさらにドリルダウンし、問題を正確に把握していきます。Related Content は、あるコンポーネントから別のコンポーネントへジャンプできる強力な機能で、**metrics**、**traces**、**logs** で利用できます。

{{< webex chat="Robert Castley" date="Today • 28/01/2026" seenby="PH" >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:42" color="#ef950d" >}}
APM を確認したところ、問題は paymentservice にあることが分かりました。トレースに大きなレイテンシのスパイクが発生しています
{{< /webex-msg >}}
{{< webex-msg from="RC" name="Robert Castley" time="09:43" color="#ef950d">}}
Related Content を使ってログにジャンプし、レイテンシのスパイクを説明できるエラーや異常を見つけられるか確認してみます。
{{< /webex-msg >}}
{{< /webex >}}
