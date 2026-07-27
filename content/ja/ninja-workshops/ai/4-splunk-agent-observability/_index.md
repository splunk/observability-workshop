---
title: Splunk Agent Observability
linkTitle: Splunk Agent Observability
weight: 4
layout: chapter
time: 2 hours
authors: ["Derek Mitchell", "Sam Goldfield", "Tim Hard"]
description: エージェント型AIアプリケーションの内部を可視化します。計装を行い、エージェントの動作をトレース・評価し、新たな問題を検出し、Splunk Agent Observability（powered by Galileo）でランタイムガードレールを適用します。
draft: false
hidden: true
aliases:
  - /ninja-workshops/20-splunk-agent-observability/
product: "Observability Cloud"
---

エージェント型AIアプリケーションは、自ら考え、計画し、行動します。その自律性こそが強力さの源であり、同時に信頼性の確保を難しくする要因でもあります。エージェントが誤った回答に至る推論を行ったり、間違ったツールを呼び出したり、ハルシネーションを起こしたり、機密データを漏洩したりした場合、*どこを確認すればよいのでしょうか？*

**Splunk Agent Observability** はGalileoを基盤とし、このギャップを埋めます。開発から本番環境まで、エージェントのライフサイクル全体にわたるオブザーバビリティを提供し、エージェントが実際に何を行ったかを確認し、その品質を測定し、ユーザーより先に障害を検知し、ランタイムで安全な動作を強制できます。

> [!splunk] **シナリオ**
> **Careful Health Provider** は、患者からの薬に関する質問に回答し、患者記録を検索するエージェント型AIヘルスケアアシスタントをリリースしようとしています。インフラストラクチャとアプリケーションパフォーマンスについては既に強力なオブザーバビリティを備えていますが、エージェント型システムには新たなリスクが伴います。予測不可能な推論、ハルシネーション、コストの急増、機密データの漏洩です。患者に処方量の *2倍* を服用するよう伝えるような誤回答が1つあるだけで、ニュースの見出しになりかねません。このワークショップでは、*あなた* がCareful Health Providerのリスク対策を支援します。

このハンズオンワークショップでは、**Streamlit**、**LangGraph**、**PostgreSQL/pgvector** で構築されたヘルスケアアシスタントを使い、段階的にオブザーバビリティ、測定可能性、安全性を実現していきます。

{{< objectives title="学習内容" >}}

* アプリケーションを **計装** し、Traceをキャプチャして、各エージェントリクエストで何が起きたかを正確に把握します。
* エージェントの動作を **トレースして調査** し、複雑なマルチステップワークフローにおけるエラーの根本原因を特定します。
* **すぐに使える品質メトリクスを有効化** し、エージェントのインタラクションを評価して、ハルシネーションやツール選択エラーなどの異常を迅速に検出します。
* **Signalsで新たな問題を検出** し、評価や手動調査では発見しにくいエージェントの障害パターンを自動的に検知します。
* **ランタイムでガードレールを適用** し、ポリシー違反、機密データの漏洩、安全でないプロンプトやレスポンスを検出してブロック *または* 修正します。

{{< /objectives >}}

{{% notice title="Splunk Agent Observability, powered by Galileo" style="info" %}}

Splunk Agent Observabilityは、開発から本番環境まで、エージェントのライフサイクルにオブザーバビリティを提供します。

* **高精度な評価**: 高精度の評価機能と、すぐに使えるメトリクスおよびカスタムメトリクスの両方で、エージェント、出力、RAGの品質を評価します。
* **即座の可視化**: 複雑なマルチステップのエージェントワークフロー全体で、エラーの根本原因を確認できます。
* **ランタイムガードレール**: ハルシネーション、プロンプトインジェクション、安全性違反がユーザーに届く前にブロックします。

{{% /notice %}}

{{% notice style="info" title="主要リファレンス" %}}

* [Galileoドキュメント](https://docs.galileo.ai/)
* [Galileoクイックスタート](https://docs.galileo.ai/getting-started/quickstart)
* [Galileo LangChain統合](https://docs.galileo.ai/sdk-api/third-party-integrations/langchain/langchain)

{{% /notice %}}
