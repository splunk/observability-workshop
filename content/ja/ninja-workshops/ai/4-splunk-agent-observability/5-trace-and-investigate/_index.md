---
title: エージェントの動作をトレースして調査する
linkTitle: 5. Trace and Investigate
weight: 5
time: 10 minutes
---

トレースが流れるようになったので、活用していきましょう。この章では、Splunk Agent Observabilityに移動し、各リクエストでエージェントが何を行ったかを正確に調査します。推論、ツール呼び出し、取得されたコンテキスト、トークン、レイテンシーのすべてを一箇所で確認できます。

{{% notice title="ペルソナ" style="orange" icon="user" %}}

Careful Health Providerの **AIエンジニア** として、アシスタントの動作を完全に可視化できるようになりました。患者が不正確な回答を報告した場合、推測する必要はもうありません。トレースを開いて、エージェントがその回答に至った正確な経路を確認できます。

{{% /notice %}}

> [!splunk] **即座に可視化。** Splunk Agent Observabilityは、複雑でマルチステップのエージェントワークフロー全体のエラーの根本原因を表示します。ログをつなぎ合わせる代わりに、リクエスト全体を展開・検査可能なSpanのツリーとして確認できます。

ここで調査するトレースは、`~/workshop/healthcare-assistant/2-app-with-instrumentation` の計装済みアプリから取得されたものです（前の章で生成したトラフィック）。

トレースの調査を続けましょう。
