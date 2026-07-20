---
title: "Phase 2: OBIの魔法"
linkTitle: 4. Docker with OBI
weight: 4
archetype: chapter
time: 20 minutes
description: OBI eBPFエージェントをDocker Composeスタックに追加します。アプリケーションコードを一切変更せずに、完全な分散トレースがSplunk APMに表示されます。
---

このフェーズでは、Docker Composeスタックにコンテナを1つ追加します。アプリケーションコードを一切変更せずに、3つのサービスすべてにわたる完全な分散トレースがSplunk APMに表示されます。

{{% notice icon="user" style="orange" title="重要なポイント" %}}
これがこのワークショップの核心となるデモです。 **コンテナを1つ** 追加し、 **アプリケーションコードの変更はゼロ** で、 **トレースなし** の状態から **完全な分散トレーシング** へと移行します。
{{% /notice %}}
