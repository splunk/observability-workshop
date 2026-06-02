---
title: 3. FileLog Setup
linkTitle: 3. FileLog Setup
time: 10 minutes
weight: 5
---

OpenTelemetry Collector の [**FileLog Receiver**](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/filelogreceiver/README.md) は、ファイルからログを取り込むために使用します。

指定されたファイルを監視して新しいログエントリを検出し、それらのログを Collector にストリーミングして、後続の処理やエクスポートを行います。テストや開発の用途にも便利です。

ワークショップのこのパートでは、`loadgen` がランダムな名言を使ってログを生成します:

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

`agent` Collector の **FileLog receiver** は、これらのログ行を読み取って `gateway` に送信します。

{{% notice title="演習" style="green" icon="running" %}}

- **Logs ターミナル** ウィンドウで、`[WORKSHOP]` ディレクトリに移動し、`3-filelog` という新しいサブディレクトリを作成します。
- 次に、`2-gateway` から `*.yaml` を `3-filelog` にコピーします。

> [!IMPORTANT]
> **_すべての_ ターミナルウィンドウを `[WORKSHOP]/3-filelog` ディレクトリに変更してください。**

`loadgen` を起動すると、`quotes.log` というファイルに行の書き込みが始まります:

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
