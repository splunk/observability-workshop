---
title: OpenTelemetry Collector Contrib のインストール
linkTitle: 1. インストール
weight: 1
---

## OpenTelemetry Collector Contrib ディストリビューションのダウンロード

OpenTelemetry Collector をインストールする最初のステップは、ダウンロードです。このラボでは、`wget` コマンドを使用して OpenTelemetry の GitHub リポジトリから `.deb` パッケージをダウンロードします。

お使いのプラットフォーム用の `.deb` パッケージを [**OpenTelemetry Collector Contrib リリースページ**](https://github.com/open-telemetry/opentelemetry-collector-releases/releases) から取得します。

``` bash
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.111.0/otelcol-contrib_0.111.0_linux_amd64.deb
```

## OpenTelemetry Collector Contrib ディストリビューションのインストール

`dpkg` を使用して `.deb` パッケージをインストールします。インストールが成功した場合の出力例は、下の **dpkg Output** タブを確認してください：

{{< tabs >}}
{{% tab title="インストール" %}}

``` bash
sudo dpkg -i otelcol-contrib_0.111.0_linux_amd64.deb
```

{{% /tab %}}
{{% tab title="dpkg 出力" %}}

``` text
Selecting previously unselected package otelcol-contrib.
(Reading database ... 89232 files and directories currently installed.)
Preparing to unpack otelcol-contrib_0.111.0_linux_amd64.deb ...
Unpacking otelcol-contrib (0.111.0) ...
Setting up otelcol-contrib (0.111.0) ...
Created symlink /etc/systemd/system/multi-user.target.wants/otelcol-contrib.service → /lib/systemd/system/otelcol-contrib.service.
```

{{% /tab %}}
{{< /tabs >}}
