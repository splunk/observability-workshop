---
title: PetClinic モノリスワークショップ
weight: 1
description: Spring PetClinic サンプルアプリケーションを使用して、Java アプリケーション向けの Splunk Observability Cloud の自動ディスカバリーおよび設定機能をデモンストレーションするハンズオンワークショップです。
archetype: chapter
authors: ["Robert Castley"]
time: 30 minutes
---

このワークショップの目的は、**Splunk Observability Cloud** プラットフォームの以下のコンポーネントを設定するための基本的な手順を説明することです：

* Splunk Infrastructure Monitoring (IM)
* Splunk Automatic Discovery for Java (APM)
  * Database Query Performance
  * AlwaysOn Profiling
* Splunk Real User Monitoring (RUM)
* RUM から APM への相関 (Correlation)
* Splunk Log Observer (LO)

また、サンプル Java アプリケーション（Spring PetClinic）のクローン（ダウンロード）方法、およびアプリケーションのコンパイル、パッケージ化、実行方法についても説明します。

アプリケーションが起動して実行されると、**Splunk APM** 製品で使用される Java 2.x 向けの**自動ディスカバリーおよび設定**機能により、メトリクス、トレース、ログが即座に表示されるようになります。

その後、**Splunk OpenTelemetry Javascript Libraries (RUM)** を使用して PetClinic のエンドユーザーインターフェース（アプリケーションがレンダリングする HTML ページ）を計装します。これにより、エンドユーザーが実行するすべてのクリックやページ読み込みに対して RUM トレースが生成されます。

最後に、PetClinic アプリケーションログへのトレースメタデータの自動インジェクション (injection) によって生成されたログを確認します。

{{% notice title="前提条件" style="primary" icon="info" %}}

* ポート `2222` へのアウトバウンド SSH アクセス
* ポート `8083` へのアウトバウンド HTTP アクセス
* `bash` シェルおよび `vi/vim` エディタの基本的な知識

{{% /notice %}}

![PetClinic Exercise](images/petclinic-exercise.png)
