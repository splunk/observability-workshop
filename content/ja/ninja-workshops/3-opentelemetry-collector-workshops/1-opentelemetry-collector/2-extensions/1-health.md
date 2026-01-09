---
title: OpenTelemetry Collector Extensions
linkTitle: 2.1 Health Check
weight: 1
---

## Health Check

拡張機能は、インストール手順で参照した同じ `config.yaml` ファイルで設定します。`config.yaml` ファイルを編集して拡張機能を設定しましょう。**pprof** と **zpages** 拡張機能はデフォルトの `config.yaml` ファイルに既に設定されていることに注意してください。このワークショップでは、Collector のヘルス状態にアクセスできるよう、すべてのネットワークインターフェースでポートを公開するように **health_check** 拡張機能のみを更新します。

{{% tab title="Command" %}}

``` bash
sudo vi /etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

{{% tab title="Extensions Configuration" %}}

```yaml {hl_lines="3"}
extensions:
  health_check:
    endpoint: 0.0.0.0:13133
```

{{% /tab %}}

Collector を起動します：

{{% tab title="Command" %}}

``` bash
otelcol-contrib --config=file:/etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

この拡張機能により、OpenTelemetry Collector のステータスを確認するためにプローブできる HTTP URL が有効になります。この拡張機能は、Kubernetes で liveness プローブや readiness プローブとして使用できます。`curl` コマンドについて詳しく知るには、[curl man page](https://curl.se/docs/manpage.html) を確認してください。

新しいターミナルセッションを開き、インスタンスに SSH 接続して以下のコマンドを実行します：

{{< tabs >}}
{{% tab title="curl Command" %}}

```bash
curl http://localhost:13133
```

{{% /tab %}}
{{% tab title="curl Output" %}}

``` text
{"status":"Server available","upSince":"2024-10-07T11:00:08.004685295+01:00","uptime":"12.56420005s"}
```

{{% /tab %}}
{{< /tabs >}}
