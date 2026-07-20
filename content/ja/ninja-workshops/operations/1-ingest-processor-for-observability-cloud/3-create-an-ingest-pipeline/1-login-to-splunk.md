---
title: Splunk Cloudへのログイン
linkTitle: 3.1 Splunk Cloudへのログイン
weight: 2
---

このセクションでは、Kubernetes監査ログをメトリクスに変換してSplunk Observability Cloudワークショップ組織に送信するIngest Pipelineを作成します。開始する前に、Splunk ShowイベントのDetailsで提供されているSplunk CloudおよびIngest Processor SCS Tenant環境にアクセスする必要があります。

{{% notice title="前提条件: Splunk Enterprise Cloudへのログイン" style="green" icon="running" %}}

**1.** Splunk ShowイベントのDetailsで提供されている **Ingest Processor Cloud Stack** のURLを開きます。

![Splunk Cloudインスタンスの詳細](../../images/show_instances_sec.png)

**2.** Connection infoで **Stack URL** リンクをクリックして、Splunk Cloudスタックを開きます。

![Splunk Cloud接続の詳細](../../images/sec_connection_details.png)

**3.** `admin` ユーザー名とパスワードを使用してSplunk Cloudにログインします。

![Splunk Cloudログイン](../../images/sec_login.png)

**4.** ログイン後、プロンプトが表示された場合は利用規約に同意し、**OK** をクリックします。

![Splunk Cloudログイン](../../images/sec_terms.png)

**5.** Splunk ShowイベントのDetailsに戻り、Ingest Processor SCS Tenantを選択します。

![Ingest Processor接続の詳細](../../images/show_instances_scs.png)

**6.** **Console URL** をクリックして **Ingest Processor SCS Tenant** にアクセスします。

{{% notice title="注意" style="primary" icon="lightbulb" %}}
**Single Sign-On (SSO)**
Splunk Data Managementサービス（「SCS Tenant」）とSplunk Cloud環境の間にはシングルサインオン（SSO）が設定されているため、すでにSplunk Cloudスタックにログインしている場合は、Splunk Data Managementサービスにも自動的にログインされます。認証情報の入力を求められた場合は、Splunk ShowイベントのSplunk Cloud Stackセクションに記載されている認証情報を使用してください。
{{% /notice %}}

{{% /notice %}}
