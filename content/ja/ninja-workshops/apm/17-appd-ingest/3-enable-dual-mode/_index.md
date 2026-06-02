---
title: "Phase 2: Enable Dual Signal Mode"
linkTitle: 3. デュアルモードの有効化
weight: 3
archetype: chapter
time: 15 minutes
description: OpenTelemetry Collector をインストールし、AppDynamics エージェントでデュアルシグナルモードを有効化して、AppDynamics と Splunk Observability Cloud の両方にトレースが表示されることを確認します。
---

このフェーズでは、Splunk Observability Cloud にデータを転送するための OpenTelemetry Collector をデプロイし、デュアルシグナルモードを有効化した状態でアプリケーションを再起動します。

これまで AppDynamics のみにデータを送信していた同じエージェントが、両方の宛先に同時に送信するようになります。
