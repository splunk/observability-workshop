---
title: その他のビューを探索する
linkTitle: 2. その他のビューを探索する
weight: 2
time: 5 minutes
---

先ほど生成したトラフィックを使って、Splunk Agent Observabilityの他のビューを探索しましょう。

{{< exercise title="エージェントの動作を調査する" >}}

{{< step title="プロジェクトとログストリームを開く" >}}

Splunk Agent Observabilityのプロジェクトと `default` ログストリームに戻ります。

{{< /step >}}

{{< step title="Agent Graphを表示する" >}}

**`Agent graph`** タブをクリックします。このタブはログストリーム内のすべてのTraceにわたるエージェントの動作を集約して表示します。最も一般的な実行パス、レイテンシーと頻度のパターンが表示されるため、実際のユーザーに対してエージェントがどのように動作しているかを素早く確認できます。

![Agent Graph](../../images/galileo-agent-graph.png?width=750px)

{{< /step >}}

{{< step title="Trendsを表示する" >}}

**`Trends`** タブに切り替えて、システムのパフォーマンスが時間経過とともにどのように変化しているかを確認することもできます。例えば、リクエスト全体の全体的なレイテンシーとトークン使用量のトレンドを確認できます。

![Trends](../../images/galileo-trends.png?width=750px)

{{< /step >}}

{{< /exercise >}}

{{% notice title="調査から自動化へ" style="info" %}}

個々のTraceを読むことは単一のインシデントには有効ですが、何百万ものTraceを手動で検査することはできません。次の章では、すべてのTraceを自動的にスコアリングする **metrics** を有効にし、根拠のない医療アドバイスなどの問題が自動的に浮上するようにします。

{{% /notice %}}

{{< checkpoint title="知識チェック" >}}

{{< details summary="回答を表示するにはここをクリック" >}}

{{< /details >}}
