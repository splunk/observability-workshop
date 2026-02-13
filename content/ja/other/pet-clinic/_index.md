---
title: Pet Clinic Java ワークショップ
alwaysopen: false
weight: 1
description: JavaアプリケーションをつかったSplunk Oservabilityのワークショップです
---

このワークショップでは、Splunk Observabilityプラットフォームの以下のコンポーネントを構成するための、基本的なステップを体験できます

* Splunk Infrastructure Monitoring (IM)
* Splunk APM
  * Endpoint Performance
  * Database Query Performance
  * AlwaysOn Profiling
* Splunk Real User Monitoring (RUM)
* Splunk LogObserver

ワークショップの中では、Javaのサンプルアプリケーション（Spring Pet Clinic）をクローン（ダウンロード）し、アプリケーションのコンパイル、パッケージ、実行していきます。

アプリケーションを起動すると、OpenTelemetry Javaエージェントを通じて、Splunk APMでメトリクスとトレースが即座に表示されるようになります。

その後、Splunk OpenTelemetry Javascript Libraries (RUM)を使用して、Pet Clinicのエンドユーザーインターフェース（アプリケーションによってレンダリングされるHTMLページ）を計装し、エンドユーザーが実行する個々のクリックとページロードのすべてについて、RUMトレースを生成していきます。

{{% notice title="前提条件" style="info" %}}
このワークショップは、ホスト/インスタンスが提供されるSplunk実行ワークショップ **または** 自前のホスト/[Multipassインスタンス](https://github.com/splunk/observability-workshop/tree/main/multipass) で行う、自己主導型のワークショップです。

ご自身のシステムには、以下のものがインストールされ、有効になっている必要があります

1. JDK 17
2. ポート `8083` が開いていること（インバウンド/アウトバウンド）
{{% /notice %}}

![PetClinic Exercise](images/petclinic-exercise.png)
