---
title: OpenTelemetry Collector のデプロイ
linkTitle: 2. OpenTelemetry Collector のデプロイ
weight: 2
time: 10 minutes
---

## OpenTelemetry Collector のアンインストール

EC2 インスタンスには、古いバージョンの Splunk Distribution of the OpenTelemetry Collector がすでにインストールされている場合があります。先に進む前に、以下のコマンドを使用してアンインストールしましょう

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh;
sudo sh /tmp/splunk-otel-collector.sh --uninstall
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages will be REMOVED:
  splunk-otel-collector*
0 upgraded, 0 newly installed, 1 to remove and 167 not upgraded.
After this operation, 766 MB disk space will be freed.
(Reading database ... 157441 files and directories currently installed.)
Removing splunk-otel-collector (0.92.0) ...
(Reading database ... 147373 files and directories currently installed.)
Purging configuration files for splunk-otel-collector (0.92.0) ...
Scanning processes...                                                                                                                                                                                              
Scanning candidates...                                                                                                                                                                                             
Scanning linux images...                                                                                                                                                                                           

Running kernel seems to be up-to-date.

Restarting services...
 systemctl restart fail2ban.service falcon-sensor.service
Service restarts being deferred:
 systemctl restart networkd-dispatcher.service
 systemctl restart unattended-upgrades.service

No containers need to be restarted.

No user sessions are running outdated binaries.

No VM guests are running outdated hypervisor (qemu) binaries on this host.
Successfully removed the splunk-otel-collector package
```

{{% /tab %}}
{{< /tabs >}}

## OpenTelemetry Collector のデプロイ

Linux EC2 インスタンスに最新バージョンの Splunk Distribution of the OpenTelemetry Collector をデプロイしましょう。

`curl` を使用して Collector バイナリをダウンロードし、データを送信する Realm、使用するアクセストークン、レポート先のデプロイメント環境を指定する引数を付けて実行します。

> Splunk Observability Cloud におけるデプロイメント環境とは、同じアプリケーションの他のデプロイメントの設定と重複しない設定を構成できる、システムまたはアプリケーションの個別のデプロイメントです。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh; \
sudo sh /tmp/splunk-otel-collector.sh \
--realm $REALM \
--mode agent \
--without-instrumentation \
--deployment-environment otel-$INSTANCE \
-- $ACCESS_TOKEN
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Splunk OpenTelemetry Collector Version: latest
Memory Size in MIB: 512
Realm: us1
Ingest Endpoint: https://ingest.us1.signalfx.com
API Endpoint: https://api.us1.signalfx.com
HEC Endpoint: https://ingest.us1.signalfx.com/v1/log
etc. 
```

{{% /tab %}}
{{< /tabs >}}

Collector のインストールの詳細については、[Install the Collector for Linux with the installer script](https://docs.splunk.com/observability/en/gdi/opentelemetry/collector-linux/install-linux.html#otel-install-linux) を参照してください。

## Collector の動作確認

インスタンス上で Collector が正常に動作していることを確認しましょう。

> Ctrl + C を押してステータスコマンドを終了します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
sudo systemctl status splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
● splunk-otel-collector.service - Splunk OpenTelemetry Collector
     Loaded: loaded (/lib/systemd/system/splunk-otel-collector.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/splunk-otel-collector.service.d
             └─service-owner.conf
     Active: active (running) since Fri 2024-12-20 00:13:14 UTC; 45s ago
   Main PID: 14465 (otelcol)
      Tasks: 9 (limit: 19170)
     Memory: 117.4M
        CPU: 681ms
     CGroup: /system.slice/splunk-otel-collector.service
             └─14465 /usr/bin/otelcol

```

{{% /tab %}}
{{< /tabs >}}

## Collector のログを確認するには？

`journalctl` を使用して Collector のログを確認できます

> Ctrl + C を押してログのテーリングを終了します。

{{< tabs >}}
{{% tab title="Script" %}}

``` bash
sudo journalctl -u splunk-otel-collector -f -n 100
```

{{% /tab %}}
{{% tab title="Example Output" %}}

``` bash
Dec 20 00:13:14 derek-1 systemd[1]: Started Splunk OpenTelemetry Collector.
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:483: Set config to /etc/otel/collector/agent_config.yaml
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:539: Set memory limit to 460 MiB
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:524: Set soft memory limit set to 460 MiB
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:373: Set garbage collection target percentage (GOGC) to 400
Dec 20 00:13:14 derek-1 otelcol[14465]: 2024/12/20 00:13:14 settings.go:414: set "SPLUNK_LISTEN_INTERFACE" to "127.0.0.1"
etc. 
```

{{% /tab %}}
{{< /tabs >}}

## Collector の設定

この Collector が使用する設定ファイルはどこにあるのでしょうか？

`/etc/otel/collector` ディレクトリにあります。Collector を `agent` モードでインストールしたため、Collector の設定は `agent_config.yaml` ファイルに記載されています。
