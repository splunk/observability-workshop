---
title: 3. FileLogのセットアップ
linkTitle: 3. FileLogのセットアップ
time: 10 minutes
weight: 5
---

OpenTelemetry Collectorの [**FileLog Receiver**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/filelogreceiver/README.md) は、ファイルからログを取り込むために使用されます。

指定されたファイルを監視して新しいログエントリを検出し、それらのログをCollectorにストリーミングして、さらなる処理やエクスポートを行います。テストや開発目的にも役立ちます。

ワークショップのこのパートでは、`loadgen`がランダムな引用文を使用してログを生成します。

```golang
lotrQuotes := []string{
    "One does not simply walk into Mordor.",
    "Even the smallest person can change the course of the future.",
    "All we have to decide is what to do with the time that is given us.",
    "There is some good in this world, and it's worth fighting for.",
}

starWarsQuotes := []string{
    "Do or do not, there is no try.",
    "The Force will be with you. Always.",
    "I find your lack of faith disturbing.",
    "In my experience, there is no such thing as luck.",
}
```

`agent` Collectorの **FileLog receiver** がこれらのログ行を読み取り、`gateway`に送信します。

{{% notice title="Exercise" style="green" icon="running" %}}

- **Logs terminal** ウィンドウで、`[WORKSHOP]`ディレクトリに移動し、`3-filelog`という名前の新しいサブディレクトリを作成します。
- 次に、`2-gateway`から`3-filelog`に`*.yaml`をコピーします。

> [!IMPORTANT]
> **すべてのターミナルウィンドウを `[WORKSHOP]/3-filelog` ディレクトリに変更してください。**

`loadgen`を起動すると、`quotes.log`というファイルに行の書き込みが開始されます。

{{% tabs %}}
{{% tab title="Log Load Generator" %}}

```bash
../loadgen -logs
```

{{% /tab %}}
{{% tab title="Log Load Generator Output" %}}

```text
Writing logs to quotes.log. Press Ctrl+C to stop.
```

{{% /tab %}}
{{% /tabs %}}

```text { title="Updated Directory Structure" }
.
├── agent.yaml
├── gateway.yaml
└── quotes.yaml
```

{{% /notice %}}
