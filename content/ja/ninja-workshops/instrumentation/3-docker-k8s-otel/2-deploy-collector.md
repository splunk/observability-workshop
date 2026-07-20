---
title: OpenTelemetry Collectorのデプロイ
linkTitle: 2. OpenTelemetry Collectorのデプロイ
weight: 2
time: 10 minutes
---

## OpenTelemetry Collectorのアンインストール

EC2インスタンスには、古いバージョンのSplunk Distribution of the OpenTelemetry Collectorがすでにインストールされている場合があります。先に進む前に、以下のコマンドを使用してアンインストールします。

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

## OpenTelemetry Collectorのデプロイ

Linux EC2インスタンスに最新バージョンのSplunk Distribution of the OpenTelemetry Collectorをデプロイします。

`curl` を使用してCollectorバイナリをダウンロードし、データを送信するRealm、使用するアクセストークン、レポートするデプロイメント環境を指定する引数を付けて実行します。

> Splunk Observability Cloudにおけるデプロイメント環境とは、同じアプリケーションの他のデプロイメントの設定と重複しない構成をセットアップできる、システムまたはアプリケーションの個別のデプロイメントです。

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

Collectorのインストールの詳細については、[Install the Collector for Linux with the installer script](https://docs.splunk.com/observability/en/gdi/opentelemetry/collector-linux/install-linux.html#otel-install-linux)を参照してください。

## Collectorの実行確認

Collectorがインスタンス上で正常に実行されていることを確認します。

> Ctrl + Cを押してステータスコマンドを終了します。

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

## Collectorのログを確認する方法

`journalctl` を使用してCollectorのログを確認できます。

> Ctrl + Cを押してログのテーリングを終了します。

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

## Collectorの設定

このCollectorが使用する設定はどこにあるでしょうか。

`/etc/otel/collector` ディレクトリにあります。Collectorを `agent` モードでインストールしたため、Collectorの設定は `agent_config.yaml` ファイルに記述されています。
