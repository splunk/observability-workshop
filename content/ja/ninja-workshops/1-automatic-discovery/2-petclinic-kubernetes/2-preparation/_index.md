---
title: ワークショップインスタンスの準備
linkTitle: 2. 準備
weight: 3
archetype: chapter
time: 15 minutes
---

インストラクターが、このワークショップで使用するインスタンスのログイン情報を提供します。

インスタンスに初めてログインすると、以下のようなSplunkロゴが表示されます。ワークショップインスタンスへの接続に問題がある場合は、インストラクターにお問い合わせください。

``` text
$ ssh -p 2222 splunk@<IP-ADDRESS>

███████╗██████╗ ██╗     ██╗   ██╗███╗   ██╗██╗  ██╗    ██╗
██╔════╝██╔══██╗██║     ██║   ██║████╗  ██║██║ ██╔╝    ╚██╗
███████╗██████╔╝██║     ██║   ██║██╔██╗ ██║█████╔╝      ╚██╗
╚════██║██╔═══╝ ██║     ██║   ██║██║╚██╗██║██╔═██╗      ██╔╝
███████║██║     ███████╗╚██████╔╝██║ ╚████║██║  ██╗    ██╔╝
╚══════╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝    ╚═╝
Last login: Mon Feb  5 11:04:54 2024 from [Redacted]
splunk@show-no-config-i-0d1b29d967cb2e6ff ~ $
```

インスタンスが正しく設定されていることを確認するために、このワークショップに必要な環境変数が正しく設定されているか確認する必要があります。ターミナルで以下のスクリプトを実行し、環境変数が存在し、実際の有効な値が設定されていることを確認してください：

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
. ~/workshop/petclinic/scripts/check_env.sh
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
ACCESS_TOKEN = <redacted>
REALM = <e.g. eu0, us1, us2, jp0, au0 etc.>
RUM_TOKEN = <redacted>
HEC_TOKEN = <redacted>
HEC_URL = https://<...>/services/collector/event
INSTANCE = <instance_name>
```

{{% /tab %}}
{{< /tabs >}}

`INSTANCE` 環境変数の値をメモしておいてください。後で **Splunk Observability Cloud** でデータをフィルタリングする際に使用します。

このワークショップでは、上記の環境変数が**すべて**必要です。値が不足しているものがある場合は、インストラクターに連絡してください。

> [!SPLUNK] 既存の OpenTelemetry Collector の削除
>この EC2 インスタンスを使用して以前に Splunk Observability ワークショップを完了している場合は、
>既存の Splunk OpenTelemetry Collector のインストールが削除されていることを確認する必要があります。
>これは以下のコマンドを実行することで行えます：
>
>``` bash
>helm delete splunk-otel-collector
>```
