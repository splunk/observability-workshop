---
title: OpenTelemetry Collector エクステンション
linkTitle: 2.1 Health Check
weight: 1
---

## Health Check エクステンション

他のコンポーネントと同様に、エクステンションは `config.yaml` ファイルで設定できます。ここでは実際に `config.yaml` ファイルを編集して、エクステンションを設定していきましょう。デフォルトの `config.yaml` では、すでに **pprof** エクステンションと **zpages** エクステンションが設定されていることを確認してみてください。このワークショップでは、設定ファイルをアップデートして **health_check** エクステンションを追加し、ポートを解放し、外部ネットワークからコレクターのヘルスチェックにアクセスできるようにしていきます。

{{% tab title="Command" %}}

```bash
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

コレクターを起動します:

{{% tab title="Command" %}}

```bash
sudo systemctl restart otelcol-contrib
```

{{% /tab %}}

このエクステンションは HTTP の URL を公開し、OpenTelemetry Collector の稼働状況をチェックするプローブを提供します。このエクステンションは Kubernetes 環境での Liveness/Readiness プローブとしても使われています。 `curl` コマンドの使い方は、[curl man page](https://curl.se/docs/manpage.html) を参照してください。

次のコマンドを実行します:

{{< tabs >}}
{{% tab title="curl Command" %}}

```bash
curl http://localhost:13133
```

{{% /tab %}}
{{% tab title="curl Output" %}}

```text
{"status":"Server available","upSince":"2023-04-27T10:11:22.153295874+01:00","uptime":"16m24.684476004s"}
```

{{% /tab %}}
{{< /tabs >}}
