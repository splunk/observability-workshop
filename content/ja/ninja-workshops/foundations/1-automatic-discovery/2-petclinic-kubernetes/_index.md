---
title: Kubernetes 上の Spring PetClinic SpringBoot ベースのマイクロサービス
linkTitle: PetClinic Kubernetes ワークショップ
weight: 2
archetype: chapter
authors: ["Pieter Hagen"]
description: Kubernetes で実行される Java ベースのアプリケーション向けの自動ディスカバリーおよび設定を有効にする方法を学びます。リアルタイムモニタリングを体験し、エンドツーエンドの可視性でアプリケーションの動作を最大限に活用しましょう。
time: 90 minutes
---

このワークショップの目的は、Java向けのSplunk **自動ディスカバリーおよび設定**機能を紹介することです。

ワークショップのシナリオは、Kubernetesにシンプルな（**計装されていない**）Javaマイクロサービスアプリケーションをインストールすることで作成されます。

既存のJavaベースのデプロイメント向けに自動ディスカバリー機能付きのSplunk OpenTelemetry Collectorをインストールする簡単な手順に従うことで、メトリクス、トレース、ログを **Splunk Observability Cloud** に送信することがいかに簡単かを確認できます。

> [!SPLUNK]前提条件
>
> * ポート **2222** へのアウトバウンド SSH アクセス
> * ポート **81** へのアウトバウンド HTTP アクセス
> * Linux コマンドラインの基本的な知識

このワークショップでは、以下のコンポーネントをカバーします

* Splunk Infrastructure Monitoring (**IM**)
* Splunk automatic discovery and configuration for Java (**APM**)
  * Database Query Performance
  * AlwaysOn Profiling
* Splunk Log Observer (**LO**)
* Splunk Real User Monitoring (**RUM**)

_Splunk Synthetics は少し寂しそうですが、他のワークショップでカバーしています_ {{% icon icon="heart" %}}
