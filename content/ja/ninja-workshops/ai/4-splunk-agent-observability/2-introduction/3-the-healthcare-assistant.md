---
title: Healthcare Assistantアプリケーション
linkTitle: 3. Healthcare Assistant
weight: 3
time: 3 minutes
---

このワークショップで観測するアプリケーションは、Careful Health Providerの **healthcare assistant** です。検索拡張生成（RAG）とText-to-SQLツールを使用したエンドツーエンドのチャット体験を提供しますが、ベースバージョンには **オブザーバビリティの計装が含まれていません** 。それをこれから追加していきます。

## 技術スタック

| レイヤー | テクノロジー |
|-------|------------|
| UI | Streamlit (`app.py`) |
| エージェントランタイム | LangGraph (`agent.py`) |
| LLM | OpenAI via LangChain (`ChatOpenAI`) |
| ベクトルストア | PostgreSQL + pgvector via LangChain `PGVector` |
| リレーショナルデータ | CSVから読み込まれたPostgreSQLテーブル |
| 設定 | `config.yaml`, `system_prompt.json`, `.streamlit/secrets.toml` |

## アーキテクチャ

Streamlit UIがユーザーメッセージを受け取り、会話を `HealthcareAgent` に渡します。エージェントは2つのノードを持つ **LangGraph** ステートグラフを実行します。LLMを呼び出す `chatbot` ノードと、LLMがリクエストしたツールを実行する `tools` ノードがあり、LLMが最終回答を生成するまでループします。

![Healthcare assistantアーキテクチャ](../../images/architecture.svg?width=750px)

### リクエストフロー

1. **Streamlit** がユーザー入力を収集し、セッションステートにチャット履歴を保持します。
2. **`HealthcareAgent.process_query()`** がメッセージをLangChain形式に変換し、LangGraphグラフを呼び出します。
3. **chatbotノード** がシステムプロンプトとバインドされたツールを使用してLLMを呼び出します。
4. LLMがツールをリクエストした場合、 **toolsノード** が該当する関数を実行し、chatbotノードに制御を戻します。
5. LLMがユーザーへの最終回答を生成するまでループが続きます。

## ツール

エージェントには3つのツールがあり、Traceで確認できるSpanに直接対応しています。

| ツール | 目的 | バックエンド |
|------|---------|---------|
| `search_medicine_qa` | 薬に関する質問に回答（用量、副作用、相互作用） | RAG over pgvector |
| `get_patient_info` | IDで患者を検索 | Text-to-SQL → `healthcare_patient` |
| `delete_patient_record` | IDで患者を削除 | Text-to-SQL → `healthcare_patient` |

2つのクエリ例が主要なパスを実行します。これらはワークショップ全体で使用するため、覚えておいてください。

* *"What is the dosage and common side effects of Lisinopril?"* はRAGツール（`search_medicine_qa`）を実行します。 **これは危険な「用量を2倍にする」回答の背後にあるパスです** 。検索やグラウンディングが失敗すると、エージェントは誤った用量を自信を持って回答する可能性があります。
* *"Can you look up information for patient P001?"* はText-to-SQLツール（`get_patient_info`）を実行します。

{{% notice title="留意すべき2つのリスク" style="info" %}}

* **ハルシネーションによる医療ガイダンス** : 薬のQ&Aパスでは、誤った用量や相互作用が通過する可能性があります。メトリクスとシグナルでこれを検出し、ガードレールで防止します。
* **機密性が高く不可逆なアクション** : `delete_patient_record` は患者を永久に削除できます。これはランタイムガードレールの典型的なケースです。両方については後のチャプターで取り上げます。

{{% /notice %}}

## ステージフォルダー

アプリケーションはインスタンス上の4つの段階的なフォルダーとして提供されます。各フォルダーはワークショップのステージに対応し、そのステージの完成版リファレンスとしても機能します。

```text
~/workshop/healthcare-assistant/
├── 1-base-app/                  # Deploy (Chapter 3): 計装なしの開始地点
├── 2-app-with-instrumentation/  # Instrument, trace, metrics, signals (Chapters 4–7)
├── 3-app-with-experiments/      # Experiments (このワークショップでは使用しません)
└── 4-app-with-controls/         # Guardrails / agent controls (Chapter 8)
```

{{% notice title="ステージフォルダーの使い方" style="info" %}}

各コードチャプターでは、あるステージを次のステージに変換するための具体的な変更手順を確認します。

{{% /notice %}}
