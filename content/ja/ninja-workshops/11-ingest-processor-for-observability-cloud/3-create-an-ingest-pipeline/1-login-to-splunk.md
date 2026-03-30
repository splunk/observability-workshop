---
title: Splunk Cloud へのログイン
linkTitle: 3.1 Splunk Cloud へのログイン
weight: 2
---

このセクションでは、Kubernetes AuditログをSplunk Observability Cloudワークショップ組織に送信されるメトリクスに変換するIngest Pipelineを作成します。開始する前に、Splunk Showイベントの詳細に記載されているSplunk CloudおよびIngest Processor SCS Tenant環境にアクセスする必要があります。

{{% notice title="前提条件: Splunk Enterprise Cloudへのログイン" style="green" icon="running" %}}

**1.** Splunk Showイベントの詳細に記載されている **Ingest Processor Cloud Stack** URLを開きます。

![Splunk Cloud Instance Details](../../images/show_instances_sec.png)

**2.** Connection infoで **Stack URL** リンクをクリックして、Splunk Cloudスタックを開きます。

![Splunk Cloud Connection Details](../../images/sec_connection_details.png)

**3.** `admin` ユーザー名とパスワードを使用してSplunk Cloudにログインします。

![Splunk Cloud Login](../../images/sec_login.png)

**4.** ログイン後、プロンプトが表示されたら、利用規約に同意して **OK** をクリックします。

![Splunk Cloud Login](../../images/sec_terms.png)

**5.** Splunk Showイベントの詳細に戻り、Ingest Processor SCS Tenantを選択します。

![Ingest Processor Connection Details](../../images/show_instances_scs.png)

**6.** **Console URL** をクリックして **Ingest Processor SCS Tenant** にアクセスします。

{{% notice title="Note" style="primary" icon="lightbulb" %}}
**Single Sign-On (SSO)**
Splunk Data Managementサービス（'SCS Tenant'）とSplunk Cloud環境の間でSingle Sign-on (SSO) が設定されているため、すでにSplunk Cloudスタックにログインしている場合は、Splunk Data Managementサービスにも自動的にログインされます。認証情報の入力を求められた場合は、Splunk ShowイベントのSplunk Cloud Stackに記載されている認証情報を使用してください（'Splunk Cloud Stack' セクションに記載されています）。
{{% /notice %}}

{{% /notice %}}
