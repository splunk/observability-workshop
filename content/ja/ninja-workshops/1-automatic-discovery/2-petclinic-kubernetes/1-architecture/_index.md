---
title: アーキテクチャ
linkTitle: 1. アーキテクチャ
weight: 2
time: 5 minutes
---

Spring PetClinic Java アプリケーションは、フロントエンドとバックエンドのサービスで構成されるシンプルなマイクロサービスアプリケーションです。フロントエンドサービスは、バックエンドサービスと対話するための Web インターフェースを提供する Spring Boot アプリケーションです。バックエンドサービスは、MySQL データベースと対話するための RESTful API を提供する Spring Boot アプリケーションです。

このワークショップを終えるころには、Kubernetes で実行される Java ベースのアプリケーション向けの**自動ディスカバリーおよび設定**を有効にする方法をより深く理解できるようになります。

以下の図は、Splunk OpenTelemetry Operator と自動ディスカバリーおよび設定を有効にした状態で Kubernetes 上で実行される Spring PetClinic Java アプリケーションのアーキテクチャを詳しく示しています。

![Splunk Otel Architecture](../images/auto-instrumentation-java-diagram.png)

---

**Josh Voravong** が作成した[**サンプル**](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/enable-operator-and-auto-instrumentation/spring-petclinic-java.md)に基づいています。
