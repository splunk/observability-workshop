---
title: Login to Splunk Cloud
linkTitle: 3.1 Login to Splunk Cloud
weight: 2
---

このセクションでは、Kubernetes Audit Logs をメトリクスに変換し、Splunk Observability Cloud のワークショップ組織に送信する Ingest Pipeline を作成します。開始する前に、Splunk Show のイベント詳細で提供されている Splunk Cloud と Ingest Processor SCS Tenant 環境にアクセスする必要があります。

{{% notice title="前提条件: Splunk Enterprise Cloud へのログイン" style="green" icon="running" %}}

**1.** Splunk Show のイベント詳細で提供されている **Ingest Processor Cloud Stack** の URL を開きます。

![Splunk Cloud Instance Details](../../images/show_instances_sec.png)

**2.** Connection info で **Stack URL** リンクをクリックし、Splunk Cloud スタックを開きます。

![Splunk Cloud Connection Details](../../images/sec_connection_details.png)

**3.** `admin` のユーザー名とパスワードを使用して Splunk Cloud にログインします。

![Splunk Cloud Login](../../images/sec_login.png)

**4.** ログイン後、プロンプトが表示されたら Terms of Service を承諾し、**OK** をクリックします。

![Splunk Cloud Login](../../images/sec_terms.png)

**5.** Splunk Show のイベント詳細に戻り、Ingest Processor SCS Tenant を選択します。

![Ingest Processor Connection Details](../../images/show_instances_scs.png)

**6.** **Console URL** をクリックして **Ingest Processor SCS Tenant** にアクセスします。

{{% notice title="Note" style="primary" icon="lightbulb" %}}
**Single Sign-On (SSO)**
Splunk Data Management service ('SCS Tenant') と Splunk Cloud 環境の間では Single Sign-on (SSO) が構成されているため、すでに Splunk Cloud スタックにログインしている場合は、自動的に Splunk Data Management service にログインされるはずです。認証情報の入力を求められた場合は、Splunk Show イベントの Splunk Cloud Stack で提供されている認証情報（'Splunk Cloud Stack' セクションに記載）を使用してください。
{{% /notice %}}

{{% /notice %}}
