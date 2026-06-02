---
title: Splunk Observability Cloud によるエージェント型 AI アプリケーションの監視
linkTitle: Splunk Observability Cloud によるエージェント型 AI アプリケーションの監視
weight: 18
archetype: chapter
time: 45 minutes
authors: ["Derek Mitchell"]
description: LangChain ベースのエージェント型 AI アプリケーションを OpenTelemetry で計装し、Splunk Observability Cloud を使って品質問題や AI セキュリティリスクを可視化します。
draft: false
hidden: false
aliases:
  - /ninja-workshops/18-agentic-ai/
---

**Splunk Observability for AI** は、AI アプリケーションスタックのパフォーマンス、品質、セキュリティ、コストを監視します。次の機能が含まれます。

* **AI Agent Monitoring**：LLM およびエージェント型アプリケーションのパフォーマンス、品質、セキュリティ、コストを監視します。
* **AI Infrastructure Monitoring**：AI インフラストラクチャの正常性、可用性、消費量（使用量）を監視します。

本ワークショップでは、Splunk Observability Cloud でこれらの機能をデプロイし、利用するハンズオン体験を提供します。具体的には次の内容を扱います。

* **Azure** アカウントを **Splunk Observability Cloud** に接続して、AI インフラストラクチャ関連メトリクスを取得する方法を理解します。
* AI インフラストラクチャに関する標準提供の **dashboards** および **navigators** を探索します。
* **LangChain** と **LangGraph** で構築されたエージェント型 AI アプリケーションの **architecture** を確認します。
* エージェント型 AI アプリケーションをデプロイし、**OpenTelemetry** で **instrumenting**（計装）する練習を行います。
* **metrics, traces, and logs** を Splunk Observability Cloud でどのように活用してエージェントのパフォーマンスを把握できるかを探索します。
* エージェント型 AI アプリケーションを修正して **tool calls** および **agents** を利用する練習を行います。
* アプリケーションに **quality issues** を追加し、**semantic quality evals** を使って Splunk Observability Cloud で検出する練習を行います。
* アプリケーションに **AI Defense instrumentation** と **security risks** を追加し、Splunk Observability Cloud で検出する練習を行います。
