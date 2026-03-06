---
title: OpenTelemetry Collector レシーバー
linkTitle: 1. Host Metrics
weight: 1
---

## Host Metrics レシーバー

[**Host Metrics レシーバー**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/hostmetricsreceiver/README.md) は、さまざまなソースからスクレイピングされたホストシステムに関するメトリクスを生成します。これは、コレクターがエージェントとしてデプロイされるときに使用さます。

`etc/otel-contrib/config.yaml` ファイルを更新して、**hostmetrics** レシーバーを設定してみましょう。以下のYAMLを **receivers** セクションの下に挿入します。

``` bash
sudo vi /etc/otelcol-contrib/config.yaml
```

{{% notice title="Tips: vi or nano" style="info" %}}
vi/vimの操作に慣れていない場合は、[nano](https://www.nano-editor.org/) もお試しいただくと良いかもしれません。nanoはLinux環境でよく使われる、シンプルなエディタの一つです。

``` bash
sudo nano /etc/otelcol-contrib/config.yaml
```

* `Alt-U` で、アンドゥができます。Macの場合は `Esc` キーを押したあとに `U` を押してください！
* `ctrl-_` のあとに数字を入力すると、指定した行数にジャンプします。
* `ctrl-O` のあとに `Enter` で、ファイルを保存します。
* `ctrl-X` で、nanoを終了します。

{{% /notice %}}

{{% tab title="Host Metrics Receiver Configuration" %}}

```yaml {hl_lines="2-22"}
receivers:
  hostmetrics:
    collection_interval: 10s
    scrapers:
      # CPU utilization metrics
      cpu:
      # Disk I/O metrics
      disk:
      # File System utilization metrics
      filesystem:
      # Memory utilization metrics
      memory:
      # Network interface I/O metrics & TCP connection metrics
      network:
      # CPU load metrics
      load:
      # Paging/Swap space utilization and I/O metrics
      paging:
      # Process count metrics
      processes:
      # Per process CPU, Memory and Disk I/O metrics. Disabled by default.
      # process:
```

{{% /tab %}}
