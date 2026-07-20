---
title: 2.2 耐障害性テストの環境セットアップ
linkTitle: 2.2 環境セットアップ
weight: 2
---

次に、**File Storage** の設定をテストするための環境を準備します。

{{% exercise title="耐障害性テストのセットアップ" %}}

**Gateway の起動**: **Gateway ターミナル** ウィンドウで以下を実行します

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent の起動**: **Agent ターミナル** ウィンドウで以下を実行します

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**5つのテストSpanを送信**: **Loadgen ターミナル** ウィンドウで以下を実行します

```bash { title="Start Load Generator" }
../loadgen -count 5
```

**Agent** と **Gateway** の両方にデバッグログが表示され、**Gateway** が `./gateway-traces.out` ファイルを作成します。

すべてが正常に動作していれば、システムの耐障害性テストに進むことができます。
{{% /exercise %}}
