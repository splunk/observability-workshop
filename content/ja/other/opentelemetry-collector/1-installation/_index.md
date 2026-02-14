---
title: OpenTelemetry Collector Contrib をインストールする
linkTitle: 1. インストール
weight: 1
---

## OpenTelemetry Collector の Contrib ディストリビューションをダウンロードする

OpenTelemetry Collectorのインストールのために、まずはダウンロードするのが最初のステップです。このラボでは、 `wget` コマンドを使ってOpenTelemetryのGitHubリポジトリから `.deb` パッケージをダウンロードしていきます。

[OpenTelemetry Collector Contrib releases page](https://github.com/open-telemetry/opentelemetry-collector-releases/releases)
から、ご利用のプラットフォーム用の `.deb` パッケージを入手してください。

``` bash
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.80.0/otelcol-contrib_0.80.0_linux_amd64.deb
```

## OpenTelemetry Collector の Contrib ディストリビューションをインストールする

`dpkg` を使って、 `.deb` パッケージをインストールします。下記の **dpkg Output** のようになれば、インストールは成功です！

{{< tabs >}}
{{% tab title="Install" %}}

``` bash
sudo dpkg -i otelcol-contrib_0.80.0_linux_amd64.deb
```

{{% /tab %}}
{{% tab title="dpkg Output" %}}

``` text
Selecting previously unselected package otelcol-contrib.
(Reading database ... 64218 files and directories currently installed.)
Preparing to unpack otelcol-contrib_0.75.0_linux_amd64.deb ...
Unpacking otelcol-contrib (0.75.0) ...
Setting up otelcol-contrib (0.75.0) ...
Created symlink /etc/systemd/system/multi-user.target.wants/otelcol-contrib.service → /lib/systemd/system/otelcol-contrib.service.
```

{{% /tab %}}
{{< /tabs >}}
