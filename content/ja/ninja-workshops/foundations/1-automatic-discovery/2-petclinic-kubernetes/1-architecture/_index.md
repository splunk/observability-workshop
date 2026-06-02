---
title: Architecture
linkTitle: 1. アーキテクチャ
weight: 2
time: 5 minutes
---

Spring PetClinic Java アプリケーションは、フロントエンドサービスとバックエンドサービスで構成されるシンプルなマイクロサービスアプリケーションです。フロントエンドサービスは Spring Boot アプリケーションで、バックエンドサービスとやり取りするための Web インターフェイスを提供します。バックエンドサービスは Spring Boot アプリケーションで、MySQL データベースとやり取りするための RESTful API を提供します。

このワークショップを完了するころには、Kubernetes 上で動作する Java ベースのアプリケーションに対して **automatic discovery and configuration** を有効化する方法について、より深く理解できるようになります。

下図は、Splunk OpenTelemetry Operator と automatic discovery and configuration を有効化した状態で、Kubernetes 上で動作する Spring PetClinic Java アプリケーションのアーキテクチャを示しています。

![Splunk Otel Architecture](../images/auto-instrumentation-java-diagram.png)

---

**Josh Voravong** が作成した [**example**](https://github.com/signalfx/splunk-otel-collector-chart/blob/main/examples/enable-operator-and-auto-instrumentation/spring-petclinic-java.md) をベースにしています。
