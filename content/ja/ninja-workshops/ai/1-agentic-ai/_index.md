---
title: Agentic AIアプリケーションのモニタリング
linkTitle: Agentic AIアプリケーションのモニタリング
weight: 1
layout: chapter
time: 45 minutes
authors: ["Derek Mitchell"]
description: LangChainベースのAgentic AIアプリケーションをOpenTelemetryで計装し、Splunk Observability Cloudを使用して品質の問題やAIセキュリティリスクを可視化します。
aliases:
  - /ninja-workshops/18-agentic-ai/
product: "Observability Cloud"
---

**Splunk Observability for AI** は、AIアプリケーションスタックのパフォーマンス、品質、セキュリティ、コストをモニタリングします。以下が含まれます。

* **AI Agent Monitoring** は、LLMおよびAgentic AIアプリケーションのパフォーマンス、品質、セキュリティ、コストをモニタリングします。
* **AI Infrastructure Monitoring** は、AIインフラストラクチャの正常性、可用性、消費量（使用量）をモニタリングします。

このワークショップでは、Splunk Observability Cloudのこれらの機能をデプロイし、操作するハンズオン体験を提供します。以下の内容が含まれます。

* **Azure** アカウントを **Splunk Observability Cloud** に接続し、AIインフラストラクチャ関連のメトリクスを取得する方法を理解します。
* AIインフラストラクチャに関連するすぐに使えるダッシュボードとナビゲーターを探索します。
* **LangChain** と **LangGraph** で構築されたAgentic AIアプリケーションのアーキテクチャを確認します。
* Agentic AIアプリケーションをデプロイし、**OpenTelemetry** で計装する練習を行います。
* Splunk Observability Cloudで **metrics、traces、logs** を使用してエージェントのパフォーマンスを理解する方法を探索します。
* Agentic AIアプリケーションを変更して **tool calls** と **agents** を使用する練習を行います。
* アプリケーションに品質の問題を追加し、Splunk Observability Cloudで **semantic quality evals** を使用して検出する練習を行います。
* アプリケーションに **AI Defense instrumentation** とセキュリティリスクを追加し、Splunk Observability Cloudで検出する練習を行います。
