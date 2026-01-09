---
title: ワークショップ環境への接続方法
linkTitle: 1.1 ワークショップ環境への接続方法
weight: 2
---

1. Splunk Enterprise Cloud インスタンスの URL を取得する方法
2. Splunk Observability Cloud ワークショップ組織にアクセスする方法

---

## 1. Splunk Cloud インスタンス

このワークショップ全体で使用される3つのインスタンスが、すでにプロビジョニングされています：

1. Splunk Enterprise Cloud
2. Splunk Ingest Processor (SCS Tenant)
3. Splunk Observability Cloud

Splunk Enterprise Cloud と Ingest Processor インスタンスは [Splunk Show](https://show.splunk.com) でホストされています。ワークショップに招待された場合、[Splunk Show](https://show.splunk.com) のイベントへの招待メールを受け取っているはずです。または、ワークショップの開始時にイベントへのリンクが提供されます。

[splunk.com](https://login.splunk.com/) の認証情報を使用して Splunk Show にログインしてください。このワークショップのイベントが表示されるはずです。イベントを開いて、Splunk Cloud および Ingest Processor インスタンスの詳細を確認してください。

{{% notice title="Note" style="primary" icon="lightbulb" %}}

Splunk Show イベントの詳細に記載されている `User Id` をメモしてください。この番号は、Kubernetes データの検索とフィルタリングに使用する `sourcetype` に含まれます。これは共有環境であるため、他の参加者のデータに影響を与えないよう、提供された参加者番号のみを使用してください。

{{% /notice %}}

![Splunk Show Instance Information](../../images/show_instance_information.png)

## 2. Splunk Observability Cloud インスタンス

Splunk Observability Cloud ワークショップ組織にアクセスするためのメールも受け取っているはずです（スパムフォルダを確認する必要があるかもしれません）。メールを受け取っていない場合は、ワークショップのインストラクターにお知らせください。環境にアクセスするには、**Join Now** ボタンをクリックしてください。

![Splunk Observability Cloud Invitation](../../images/workshop_invitation.png)

{{% notice title="Important" style="info" %}}
ワークショップ開始時刻前にイベントにアクセスした場合、インスタンスがまだ利用できない可能性があります。ご心配なく、ワークショップが始まると提供されます。
{{% /notice %}}

さらに、Splunk Observability Cloud ワークショップ組織に招待されています。招待には環境へのリンクが含まれています。まだ Splunk Observability Cloud アカウントをお持ちでない場合は、作成を求められます。すでにお持ちの場合は、インスタンスにログインすると、利用可能な組織にワークショップ組織が表示されます。
