---
title: Splunk Cloud へのログイン
linkTitle: 3.1 Splunk Cloud へのログイン
weight: 2
---

このセクションでは、Kubernetes Audit ログを Splunk Observability Cloud ワークショップ組織に送信されるメトリクスに変換する Ingest Pipeline を作成します。開始する前に、Splunk Show イベントの詳細に記載されている Splunk Cloud および Ingest Processor SCS Tenant 環境にアクセスする必要があります。

{{% notice title="前提条件: Splunk Enterprise Cloud へのログイン" style="green" icon="running" %}}

**1.** Splunk Show イベントの詳細に記載されている **Ingest Processor Cloud Stack** URL を開きます。

![Splunk Cloud Instance Details](../../images/show_instances_sec.png)

**2.** Connection info で **Stack URL** リンクをクリックして、Splunk Cloud スタックを開きます。

![Splunk Cloud Connection Details](../../images/sec_connection_details.png)

**3.** `admin` ユーザー名とパスワードを使用して Splunk Cloud にログインします。

![Splunk Cloud Login](../../images/sec_login.png)

**4.** ログイン後、プロンプトが表示されたら、利用規約に同意して **OK** をクリックします。

![Splunk Cloud Login](../../images/sec_terms.png)

**5.** Splunk Show イベントの詳細に戻り、Ingest Processor SCS Tenant を選択します。

![Ingest Processor Connection Details](../../images/show_instances_scs.png)

**6.** **Console URL** をクリックして **Ingest Processor SCS Tenant** にアクセスします。

{{% notice title="Note" style="primary" icon="lightbulb" %}}
**Single Sign-On (SSO)**
Splunk Data Management サービス（'SCS Tenant'）と Splunk Cloud 環境の間で Single Sign-on (SSO) が設定されているため、すでに Splunk Cloud スタックにログインしている場合は、Splunk Data Management サービスにも自動的にログインされます。認証情報の入力を求められた場合は、Splunk Show イベントの Splunk Cloud Stack に記載されている認証情報を使用してください（'Splunk Cloud Stack' セクションに記載されています）。
{{% /notice %}}

{{% /notice %}}
