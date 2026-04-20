---
title: Agentic AI アプリケーションアーキテクチャ
linkTitle: 4. Agentic AI アプリケーションアーキテクチャ
weight: 4
time: 15 minutes
---

## アプリケーション概要

このワークショップでは、旅行予約のための **Agentic AI** アプリケーションを使用します。
**OpenTelemetry** でアプリケーションを計装する前に、アプリケーションの仕組みを理解しておくと役立ちます。

![Application Architecture](../images/travel-planner-app-architecture.png)

このアプリケーションは、旅行プランニングリクエストを受け付け、LangChain を活用した複数の LLM ノードで構成される **LangGraph** ワークフローを通じて処理する **Flask API** です。各ノードは特定の役割を持ち、共有ステートを更新して次のステップに引き渡します。

このパートでは、以下の内容を確認します

* リクエストのライフサイクル
* 共有ステートモデル
* LangGraph ノードの動作方法
* コード内で使用されている LangChain の抽象化
* 後でオブザーバビリティが重要になる箇所

アプリケーションのアーキテクチャと実装の詳細については、サブセクションに移動してください。
