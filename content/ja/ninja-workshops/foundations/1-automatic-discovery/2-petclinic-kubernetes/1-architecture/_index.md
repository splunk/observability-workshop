---
title: アーキテクチャ
linkTitle: 1. アーキテクチャ
weight: 2
time: 5 minutes
---

Spring PetClinic Javaアプリケーションは、フロントエンドとバックエンドのサービスで構成されるシンプルなマイクロサービスアプリケーションです。フロントエンドサービスは、バックエンドサービスと対話するためのWebインターフェースを提供するSpring Bootアプリケーションです。バックエンドサービスは、MySQLデータベースと対話するためのRESTful APIを提供するSpring Bootアプリケーションです。

このワークショップを終えるころには、Kubernetesで実行されるJavaベースのアプリケーション向けの**自動ディスカバリーおよび設定**を有効にする方法をより深く理解できるようになります。

以下の図は、Splunk OpenTelemetry Operatorと自動ディスカバリーおよび設定を有効にした状態でKubernetes上で実行されるSpring PetClinic Javaアプリケーションのアーキテクチャを詳しく示しています。

![Splunk Otel Architecture](../images/auto-instrumentation-java-diagram.png)

---

**Josh Voravong** が作成した[**サンプル**](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/enable-operator-and-auto-instrumentation/spring-petclinic-java.md)に基づいています。
