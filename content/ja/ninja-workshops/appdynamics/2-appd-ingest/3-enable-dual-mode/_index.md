---
title: "フェーズ2: デュアルシグナルモードの有効化"
linkTitle: 3. デュアルモードの有効化
weight: 3
archetype: chapter
time: 15 minutes
description: OpenTelemetry Collectorをインストールし、AppDynamicsエージェントでデュアルシグナルモードを有効にして、AppDynamicsとSplunk Observability Cloudの両方にトレースが表示されることを確認します。
---

このフェーズでは、Splunk Observability Cloudにデータを転送するためのOpenTelemetry Collectorをデプロイし、デュアルシグナルモードを有効にしてアプリケーションを再起動します。

これまでAppDynamicsにのみデータを送信していた同じエージェントが、両方の送信先に同時にデータを送信するようになります。
