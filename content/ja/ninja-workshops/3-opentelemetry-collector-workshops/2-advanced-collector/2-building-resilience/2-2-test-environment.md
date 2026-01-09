---
title: 2.2 耐障害性テスト用の環境セットアップ
linkTitle: 2.2 Setup environment
weight: 2
---

次に、**File Storage** 設定をテストする準備として環境を設定します。

{{% notice title="Exercise" style="green" icon="running" %}}

**Gateway の起動**: **Gateway ターミナル** ウィンドウで以下を実行します：

```bash { title="Start the Gateway" }
../otelcol --config=gateway.yaml
```

**Agent の起動**: **Agent ターミナル** ウィンドウで以下を実行します：

```bash { title="Start the Agent" }
../otelcol --config=agent.yaml
```

**5つのテストスパンを送信**: **Loadgen ターミナル** ウィンドウで以下を実行します：

```bash { title="Start Load Generator" }
../loadgen -count 5
```

**Agent** と **Gateway** の両方がデバッグログを表示し、**Gateway** が `./gateway-traces.out` ファイルを作成するはずです。

すべてが正常に機能している場合、システムの耐障害性のテストに進むことができます。
{{% /notice %}}
