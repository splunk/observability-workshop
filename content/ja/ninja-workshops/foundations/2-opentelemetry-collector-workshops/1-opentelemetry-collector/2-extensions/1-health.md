---
title: OpenTelemetry Collector Extensions
linkTitle: 2.1 Health Check
weight: 1
---

## Health Check

Extensions はインストール手順で参照した `config.yaml` ファイルで設定します。`config.yaml` ファイルを編集して Extensions を設定しましょう。**pprof** と **zpages** Extensions はデフォルトの `config.yaml` ファイルに既に設定されています。このワークショップでは、Collectorの健全性にアクセスできるようにすべてのネットワークインターフェースでポートを公開するために **health_check** Extension のみを更新します。

{{% tab title="コマンド" %}}

``` bash
sudo vi /etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

{{% tab title="Extensions の設定" %}}

```yaml {hl_lines="3"}
extensions:
  health_check:
    endpoint: 0.0.0.0:13133
```

{{% /tab %}}

Collectorを起動します。

{{% tab title="コマンド" %}}

``` bash
otelcol-contrib --config=file:/etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

この Extension は、OpenTelemetry Collectorのステータスを確認するためにプローブできるHTTP URLを有効にします。この Extension はKubernetesのlivenessプローブやreadinessプローブとして使用できます。`curl` コマンドの詳細については、[curlマニュアルページ](https://curl.se/docs/manpage.html)を参照してください。

新しいターミナルセッションを開き、インスタンスにSSH接続して以下のコマンドを実行します。

{{< tabs >}}
{{% tab title="curl コマンド" %}}

```bash
curl http://localhost:13133
```

{{% /tab %}}
{{% tab title="curl 出力" %}}

``` text
{"status":"Server available","upSince":"2024-10-07T11:00:08.004685295+01:00","uptime":"12.56420005s"}
```

{{% /tab %}}
{{< /tabs >}}
