---
title: Spring PetClinic SpringBoot Based Microservices On Kubernetes
linkTitle: PetClinic Kubernetes Workshop
weight: 2
archetype: chapter
authors: ["Pieter Hagen"]
description: Kubernetes 上で稼働する Java ベースのアプリケーションに対して、自動検出と自動設定を有効化する方法を学びます。エンドツーエンドの可視性によりアプリケーションの動作を最大限に把握できる、リアルタイム監視を体験してください。
time: 90 minutes
---

このワークショップの目的は、Java 向けの Splunk の **automatic discovery and configuration**（自動検出と自動設定）の機能を紹介することです。

ワークショップのシナリオは、シンプルな（**計装されていない**）Java マイクロサービスアプリケーションを Kubernetes にインストールして構築します。

既存の Java ベースのデプロイメントに対して自動検出機能付きの Splunk OpenTelemetry Collector をインストールするシンプルな手順に従うことで、メトリクス、トレース、ログを **Splunk Observability Cloud** へ送信することがいかに簡単であるかを確認します。

> [!SPLUNK]前提条件
>
> * ポート **2222** へのアウトバウンド SSH アクセス。
> * ポート **81** へのアウトバウンド HTTP アクセス。
> * Linux コマンドラインの基本的な知識。

このワークショップでは、以下のコンポーネントを取り上げます。

* Splunk Infrastructure Monitoring (**IM**)
* Splunk automatic discovery and configuration for Java (**APM**)
  * Database Query Performance
  * AlwaysOn Profiling
* Splunk Log Observer (**LO**)
* Splunk Real User Monitoring (**RUM**)

_Splunk Synthetics は今回少し蚊帳の外ですが、他のワークショップでカバーしています_ {{% icon icon="heart" %}}
