---
title: "Phase 2: Enable Dual Signal Mode"
linkTitle: 3. Enable Dual Mode
weight: 3
archetype: chapter
time: 15 minutes
description: OpenTelemetry Collector をインストールし、AppDynamics エージェントでデュアルシグナルモードを有効にして、AppDynamics と Splunk Observability Cloud の両方にトレースが表示されることを確認します。
---

このフェーズでは、Splunk Observability Cloud にデータを転送するための OpenTelemetry Collector をデプロイし、デュアルシグナルモードを有効にしてアプリケーションを再起動します。  

これまで AppDynamics にのみデータを送信していたエージェントが、両方の宛先に同時にデータを送信するようになります。
