---
title: PetClinic モノリスワークショップ
weight: 1
description: Spring PetClinic サンプルアプリケーションを用いて、Java アプリケーション向けの Splunk Observability Cloud の自動検出・自動設定機能を体験するハンズオンワークショップです。
archetype: chapter
authors: ["Robert Castley"]
time: 30 minutes
---

このワークショップの目的は、**Splunk Observability Cloud** プラットフォームの以下のコンポーネントを設定する基本的な手順を一通り体験することです。

* Splunk Infrastructure Monitoring (IM)
* Splunk Automatic Discovery for Java (APM)
  * Database Query Performance
  * AlwaysOn Profiling
* Splunk Real User Monitoring (RUM)
* RUM to APM Correlation
* Splunk Log Observer (LO)

また、サンプルの Java アプリケーション (Spring PetClinic) のクローン (ダウンロード)、コンパイル、パッケージング、実行の手順も併せて確認します。

アプリケーションが起動すると、**Splunk APM** で利用される Java 2.x 向けの **自動検出と自動設定 (automatic discovery and configuration)** によって、メトリクス、トレース、ログがすぐに確認できるようになります。

その後、PetClinic のエンドユーザーインターフェース (アプリケーションがレンダリングする HTML ページ) を **Splunk OpenTelemetry Javascript Libraries (RUM)** で計装し、エンドユーザーが行うすべてのクリックやページロードに関する RUM トレースを生成します。

最後に、PetClinic アプリケーションログにトレースメタデータが自動的に注入されることで生成されるログを確認します。

{{% notice title="前提条件" style="primary" icon="info" %}}

* ポート `2222` へのアウトバウンド SSH アクセス。
* ポート `8083` へのアウトバウンド HTTP アクセス。
* `bash` シェルおよび `vi/vim` エディタの基本的な操作に慣れていること。

{{% /notice %}}

![PetClinic Exercise](images/petclinic-exercise.png)
