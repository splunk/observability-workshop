---
title: OpenTelemetry Collector Extensions
linkTitle: 2.1 Health Check
weight: 1
---

## Health Check

Extensions は、インストール手順で参照したのと同じ `config.yaml` ファイル内で構成します。`config.yaml` ファイルを編集して Extensions を構成しましょう。なお、**pprof** および **zpages** Extension はデフォルトの `config.yaml` ファイルですでに構成されています。このワークショップでは、Collector のヘルス状態にアクセスできるポートをすべてのネットワークインターフェースで公開するため、**health_check** Extension のみを更新します。

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

Collector を起動します:

{{% tab title="Command" %}}

``` bash
otelcol-contrib --config=file:/etc/otelcol-contrib/config.yaml
```

{{% /tab %}}

この Extension は、OpenTelemetry Collector のステータスをチェックするためにプローブできる HTTP URL を有効化します。この Extension は、Kubernetes の liveness プローブや readiness プローブとしても使用できます。`curl` コマンドの詳細については、[curl man page](https://curl.se/docs/manpage.html) を参照してください。

新しいターミナルセッションを開いてインスタンスに SSH 接続し、次のコマンドを実行します:

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
