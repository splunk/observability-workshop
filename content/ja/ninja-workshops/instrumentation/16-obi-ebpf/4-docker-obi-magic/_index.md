---
title: "Phase 2: The OBI Magic"
linkTitle: 4. Docker with OBI
weight: 4
archetype: chapter
time: 20 minutes
description: Docker Compose スタックに OBI eBPF エージェントを追加します。アプリケーションコードを一切変更せずに、Splunk APM で完全な分散トレースが表示されます。
---

このフェーズでは、Docker Compose スタックに 1 つのコンテナを追加します。アプリケーションコードを一切変更せずに、3 つのサービスすべてにわたる完全な分散トレースが Splunk APM に表示されます。

{{% notice icon="user" style="orange" title="The Key Moment" %}}
これはワークショップの中核となるデモです。**1 つのコンテナ**を追加し、アプリケーションコードを**一行も変更せず**に、**トレースゼロ**の状態から**完全な分散トレーシング**へと進もうとしています。
{{% /notice %}}
