---
title: 2.2 レジリエンステスト環境のセットアップ
linkTitle: 2.2 環境のセットアップ
weight: 2
---

次に、**File Storage** 構成をテストする準備として、環境を設定していきます。

{{% exercise title="レジリエンステストのセットアップ" %}}

**Gateway を起動する**: **Gateway terminal** ウィンドウで以下を実行します。

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent を起動する**: **Agent terminal** ウィンドウで以下を実行します。

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**5 つのテストスパンを送信する**: **Loadgen terminal** ウィンドウで以下を実行します。

```bash { title="Start Load Generator" }
../loadgen -count 5
```

**Agent** と **Gateway** の両方でデバッグログが表示され、**Gateway** によって `./gateway-traces.out` ファイルが作成されます。

すべてが正しく動作していれば、システムのレジリエンステストに進むことができます。
{{% /exercise %}}
