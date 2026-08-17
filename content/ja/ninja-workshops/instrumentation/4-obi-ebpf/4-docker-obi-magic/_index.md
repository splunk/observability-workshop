---
title: "フェーズ 2: OBI マジック"
linkTitle: 4. Docker with OBI
weight: 4
archetype: chapter
time: 20 minutes
description: OBI eBPF エージェントを Docker Compose スタックに追加します。アプリケーションコードを一切変更せずに、完全な分散トレースが Splunk APM に表示されます。
---

このフェーズでは、Docker Composeスタックに1つのコンテナを追加します。アプリケーションコードを一切変更せずに、3つすべてのサービスにわたる完全な分散トレースがSplunk APMに表示されます。

{{% notice icon="user" style="orange" title="重要なポイント" %}}
これがこのワークショップのコアデモです。**1つのコンテナ**を追加し、**アプリケーションコードを1行も変更せずに**、**トレースゼロ**から**完全な分散トレーシング**へ移行します。
{{% /notice %}}
