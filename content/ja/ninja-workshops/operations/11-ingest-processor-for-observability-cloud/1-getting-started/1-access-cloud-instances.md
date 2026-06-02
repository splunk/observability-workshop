---
title: ワークショップ環境への接続方法
linkTitle: 1.1 ワークショップ環境への接続方法
weight: 2
---

1. Splunk Enterprise Cloud インスタンスの URL を取得する方法。
2. Splunk Observability Cloud ワークショップ組織へのアクセス方法。

---

## 1. Splunk Cloud Instances

このワークショップを通じて使用する 3 つのインスタンスが、すでにプロビジョニングされています。

1. Splunk Enterprise Cloud
2. Splunk Ingest Processor (SCS Tenant)
3. Splunk Observability Cloud

Splunk Enterprise Cloud および Ingest Processor のインスタンスは [Splunk Show](https://show.splunk.com) でホストされています。ワークショップに招待された場合、[Splunk Show](https://show.splunk.com) のイベントへの招待メールを受け取っているか、ワークショップ開始時にイベントへのリンクが提供されているはずです。

[splunk.com](https://login.splunk.com/) の認証情報を使用して Splunk Show にログインしてください。このワークショップのイベントが表示されるはずです。イベントを開くと、Splunk Cloud および Ingest Processor インスタンスの詳細情報を確認できます。

{{% notice title="Note" style="primary" icon="lightbulb" %}}

Splunk Show のイベント詳細に記載されている `User Id` を控えておいてください。この番号は、Kubernetes データを検索およびフィルタリングする際に使用する `sourcetype` に含まれます。これは共有環境であるため、他の参加者のデータに影響を与えないよう、提供された参加者番号のみを使用してください。

{{% /notice %}}

![Splunk Show Instance Information](../../images/show_instance_information.png)

## 2. Splunk Observability Cloud Instances

Splunk Observability Cloud ワークショップ組織にアクセスするためのメールも届いているはずです（迷惑メールフォルダを確認する必要がある場合があります）。メールが届いていない場合は、ワークショップのインストラクターにお知らせください。環境にアクセスするには、**Join Now** ボタンをクリックします。

![Splunk Observability Cloud Invitation](../../images/workshop_invitation.png)

{{% notice title="Important" style="info" %}}
ワークショップ開始時刻より前にイベントにアクセスした場合、インスタンスがまだ利用できない可能性があります。ご心配なく、ワークショップ開始時に提供されます。
{{% /notice %}}

さらに、Splunk Observability Cloud ワークショップ組織への招待が送られています。招待には環境へのリンクが含まれています。Splunk Observability Cloud アカウントをまだお持ちでない場合は、作成するよう求められます。すでにアカウントをお持ちの場合は、インスタンスにログインすると、利用可能な組織の中にワークショップ組織が表示されます。
