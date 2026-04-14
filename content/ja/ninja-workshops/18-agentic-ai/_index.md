---
title: Splunk Observability Cloud による Agentic AI アプリケーションの監視
linkTitle: Splunk Observability Cloud による Agentic AI アプリケーションの監視
weight: 18
archetype: chapter
time: 2 minutes
authors: ["Derek Mitchell"]
description: このハンズオンワークショップでは、Splunk Observability Cloud を使用して Agentic AI アプリケーションを監視する方法を説明します。OpenTelemetry Collector のデプロイ、LangChain を使用した Python アプリケーションの計装、品質問題やセキュリティリスクを特定するための LLM インタラクションの評価設定について学びます。
draft: false
hidden: true
---

**Splunk Observability for AI** は、AI アプリケーションスタックのパフォーマンス、品質、セキュリティ、コストを監視します。以下の機能が含まれています

* **AI Agent Monitoring** は、LLM およびエージェントアプリケーションのパフォーマンス、品質、セキュリティ、コストを監視します。
* **AI Infrastructure Monitoring** は、AI インフラストラクチャの健全性、可用性、消費量（または使用量）を監視します。

このワークショップでは、Splunk Observability Cloud でこれらの機能をデプロイして操作する実践的な経験を提供します。以下の内容が含まれます

* AI インフラストラクチャ関連のメトリクスを取得するために **Azure** アカウントを **Splunk Observability Cloud** に接続する方法を理解する。
* AI インフラストラクチャに関連する標準搭載の**ダッシュボード**と**ナビゲーター**を探索する。
* **LangChain** と **LangGraph** で構築された Agentic AI アプリケーションの**アーキテクチャ**を確認する。
* Agentic AI アプリケーションをデプロイし、**OpenTelemetry** で**計装**する練習をする。
* Splunk Observability Cloud で**メトリクス、トレース、ログ**を使用してエージェントのパフォーマンスを理解する方法を探索する。
* Agentic AI アプリケーションを変更して**ツールコール**と**エージェント**を使用する練習をする。
* アプリケーションに**品質問題**を追加し、**セマンティック品質評価**を使用して Splunk Observability Cloud で検出する練習をする。
* アプリケーションに **AI Defense 計装**と**セキュリティリスク**を追加し、Splunk Observability Cloud で検出する練習をする。

{{% notice title="Tip" style="primary"  icon="lightbulb" %}}
このワークショップを進める最も簡単な方法は以下を使用することです

* このページの右上にある左右の矢印（**<** | **>**）
* キーボードの左（◀️）と右（▶️）カーソルキー
  {{% /notice %}}
