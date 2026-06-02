---
title: 4.2 レジリエンステスト用の環境構築
linkTitle: 4.2 環境構築
weight: 2
---

次に、**File Storage** 設定をテストする準備として、環境を構成していきます。

{{% notice title="演習" style="green" icon="running" %}}

**Gateway を起動**: **Gateway terminal** ウィンドウで `[WORKSHOP]/4-resilience` ディレクトリに移動し、次のコマンドを実行します。

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent を起動**: **Agent terminal** ウィンドウで `[WORKSHOP]/4-resilience` ディレクトリに移動し、次のコマンドを実行します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**5 件のテスト span を送信**: **Spans terminal** ウィンドウで `[WORKSHOP]/4-resilience` ディレクトリに移動し、次のコマンドを実行します。

```bash { title="Start Load Generator" }
../loadgen -count 5
```

`agent` と `gateway` の両方でデバッグログが表示され、`gateway` 側には `./gateway-traces.out` ファイルが作成されているはずです。

{{% /notice %}}

すべて正常に動作していれば、システムのレジリエンステストに進めます。
