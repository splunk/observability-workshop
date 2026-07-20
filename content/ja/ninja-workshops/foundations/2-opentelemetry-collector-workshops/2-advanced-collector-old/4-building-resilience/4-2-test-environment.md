---
title: 4.2 レジリエンステストの環境セットアップ
linkTitle: 4.2 環境セットアップ
weight: 2
---

次に、**File Storage** の設定をテストするための環境を準備します。

{{% notice title="Exercise" style="green" icon="running" %}}

**Gatewayの起動**: **Gatewayターミナル** ウィンドウで `[WORKSHOP]/4-resilience` ディレクトリに移動し、以下を実行します:

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agentの起動**: **Agentターミナル** ウィンドウで `[WORKSHOP]/4-resilience` ディレクトリに移動し、以下を実行します:

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**5つのテストSpanを送信**: **Spansターミナル** ウィンドウで `[WORKSHOP]/4-resilience` ディレクトリに移動し、以下を実行します:

```bash { title="Start Load Generator" }
../loadgen -count 5
```

`agent` と `gateway` の両方にデバッグログが表示され、`gateway` が `./gateway-traces.out` ファイルを作成するはずです。

{{% /notice %}}

すべてが正しく動作していれば、システムレジリエンスのテストに進むことができます。
