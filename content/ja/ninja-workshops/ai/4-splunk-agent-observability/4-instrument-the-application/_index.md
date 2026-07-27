---
title: アプリケーションの計装
linkTitle: 4. アプリケーションの計装
weight: 4
time: 10 minutes
---

キャプチャしないものはオブザーバビリティを得られません。この章では、アシスタントに **Splunk Agent Observability (Galileo)** のトレーシングを追加し、すべてのユーザーターンがトレースとなり、各LLMおよびツール呼び出しにネストされたSpanが生成されるようにします。エージェントを書き換える必要はありません。

{{% notice title="ペルソナ" style="orange" icon="user" %}}

Careful Health Providerの **AIエンジニア** として、最小限のコード変更とメンテナンスでエージェントの意思決定をエンドツーエンドで可視化したいと考えています。すべてのステップを手動で計装する代わりに、グラフレベルで単一のLangChainコールバックをアタッチし、Splunk Agent Observabilityにツリー全体を自動的にキャプチャさせます。

{{% /notice %}}

> [!splunk] 計装は非常に軽量です。GalileoコールバックはLangChainの標準的なコールバックハンドラーです。LangGraphの実行にアタッチするだけで、プロンプト、レスポンス、モデル名、トークン使用量、タイミング、Spanのネストを自動的にキャプチャします。

{{% notice title="作業場所" style="info" %}}

この章では `~/workshop/healthcare-assistant/2-app-with-instrumentation` フォルダーで作業します。

{{% /notice %}}

サブセクションに進み、SDKの追加、コールバックのアタッチ、トラフィックの生成を行います。
