---
title: OpenTelemetryコレクターのデプロイ
linkTitle: OpenTelemetryコレクターのデプロイ
weight: 2
time: 10 minutes
---

## OpenTelemetry コレクターのアンインストール

EC2 インスタンスには、すでに Splunk Distribution の OpenTelemetry コレクターの古いバージョンが
インストールされている可能性があります。先に進む前に、次のコマンドを使用してアンインストールしましょう：

{{< tabs >}}
{{% tab title="Script" %}}

```bash
curl -sSL https://dl.signalfx.com/splunk-otel-collector.sh > /tmp/splunk-otel-collector.sh;
sudo sh /tmp/splunk-otel-collector.sh --uninstall
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
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

## OpenTelemetry collector のデプロイ

Linux EC2 インスタンスに、Splunk Distribution の OpenTelemetry コレクターの最新バージョンをデプロイしましょう。

これは`curl`を使用してコレクターバイナリをダウンロードし、特定の引数を指定して実行することで可能です。
これらの引数は、データを送信する realm、使用するアクセストークン、
およびデータを送信するデプロイメント環境をコレクターに指示します。

> Splunk Observability Cloud におけるデプロイメント環境とは、システムまたはアプリケーションの個別のデプロイメントであり、同じアプリケーションの他のデプロイメントの設定と重複しない設定を行うことができます。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
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

```bash
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

詳細については、[インストーラースクリプトを使用した Linux 用コレクターのインストール](https://docs.splunk.com/observability/en/gdi/opentelemetry/collector-linux/install-linux.html#otel-install-linux)
を参照してください。

## コレクターが実行中であることを確認

インスタンスでコレクターが正常に実行されていることを確認しましょう。

> ステータスコマンドを終了するには、Ctrl + C を押します。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
sudo systemctl status splunk-otel-collector
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
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

## コレクターログの確認方法

`journalctl`を使用してコレクターログを表示できます：

> ログの監視を終了するには、Ctrl + C を押します。

{{< tabs >}}
{{% tab title="Script" %}}

```bash
sudo journalctl -u splunk-otel-collector -f -n 100
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```bash
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

## コレクターの設定

このコレクターが使用している設定はどこで見つけられるでしょうか？

その設定は`/etc/otel/collector`ディレクトリにあります。コレクターを`agent`モードで
インストールしたため、コレクター設定は`agent_config.yaml`ファイルにあります。
