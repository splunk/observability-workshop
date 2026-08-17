---
title: "フェーズ 2: デュアルシグナルモードの有効化"
linkTitle: 3. デュアルモードの有効化
weight: 3
archetype: chapter
time: 15 minutes
description: OpenTelemetry Collector をインストールし、AppDynamics エージェントでデュアルシグナルモードを有効化して、AppDynamics と Splunk Observability Cloud の両方にトレースが表示されることを確認します。
---

このフェーズでは、Splunk Observability Cloudにデータを転送するためのOpenTelemetry Collectorをデプロイし、デュアルシグナルモードを有効にしてアプリケーションを再起動します。

これまでAppDynamicsにのみデータを送信していた同じエージェントが、両方の宛先に同時にデータを送信するようになります。
