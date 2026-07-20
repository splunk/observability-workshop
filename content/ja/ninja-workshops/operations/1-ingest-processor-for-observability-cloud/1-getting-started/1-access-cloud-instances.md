---
title: ワークショップ環境への接続方法
linkTitle: 1.1 ワークショップ環境への接続方法
weight: 2
---

1. Splunk Enterprise Cloudインスタンスの URLを取得する方法
2. Splunk Observability Cloudワークショップ組織にアクセスする方法

---

## 1. Splunk Cloudインスタンス

このワークショップでは、事前にプロビジョニングされた3つのインスタンスを使用します。

1. Splunk Enterprise Cloud
2. Splunk Ingest Processor (SCS Tenant)
3. Splunk Observability Cloud

Splunk Enterprise CloudとIngest Processorのインスタンスは [Splunk Show](https://show.splunk.com) でホストされています。ワークショップに招待された場合、[Splunk Show](https://show.splunk.com) のイベントへの招待メールを受け取っているか、ワークショップの冒頭でイベントへのリンクが提供されているはずです。

[splunk.com](https://login.splunk.com/) の認証情報を使用してSplunk Showにログインします。このワークショップのイベントが表示されます。イベントを開いて、Splunk CloudとIngest Processorインスタンスの詳細を確認します。

{{% notice title="注意" style="primary" icon="lightbulb" %}}

Splunk Showのイベント詳細に記載されている `User Id` を控えてください。この番号は、Kubernetesデータの検索とフィルタリングに使用する `sourcetype` に含まれます。これは共有環境のため、他の参加者のデータに影響を与えないよう、提供された参加者番号のみを使用してください。

{{% /notice %}}

![Splunk Show Instance Information](../../images/show_instance_information.png)

## 2. Splunk Observability Cloudインスタンス

Splunk Observability Cloudワークショップ組織にアクセスするためのメールも届いているはずです（迷惑メールフォルダの確認が必要な場合があります）。メールを受け取っていない場合は、ワークショップのインストラクターにお知らせください。環境にアクセスするには **Join Now** ボタンをクリックします。

![Splunk Observability Cloud Invitation](../../images/workshop_invitation.png)

{{% notice title="重要" style="info" %}}
ワークショップ開始時刻より前にイベントにアクセスした場合、インスタンスがまだ利用できない可能性があります。ワークショップが始まれば提供されますのでご安心ください。
{{% /notice %}}

また、Splunk Observability Cloudワークショップ組織への招待も届いています。招待には環境へのリンクが含まれています。Splunk Observability Cloudアカウントをまだお持ちでない場合は、アカウントの作成を求められます。既にアカウントをお持ちの場合は、インスタンスにログインすると、利用可能な組織一覧にワークショップ組織が表示されます。
