---
title: クイックスタートセットアップ
linkTitle: 2. クイックスタートセットアップ
weight: 2
time: 5 minutes
---

旅行プランナーの環境にGalileo SDKを追加し、Splunk Agent Observabilityのトレーシングを初期化します。

{{< exercise title="クイックスタートセットアップ" >}}

{{< step title="環境のアクティベート"  >}}

アプリケーションディレクトリに移動し、[Monitoring Agentic AI Applications](ninja-workshops/ai/1-agentic-ai/)で作成した仮想環境をアクティベートします（または新しく作成します）。

```bash
cd ~/workshop/agentic-ai/base-app
python3 -m venv .venv
source .venv/bin/activate
```

{{< /step >}}

{{< step title="Galileo SDKのインストール"  >}}

`requirements.txt` にある既存の依存関係と一緒にGalileo SDKをインストールします。

```bash
pip install -r requirements.txt
pip install galileo python-dotenv
```

アプリケーションは `requirements.txt` を通じて `langchain`、`langchain-openai`、`langgraph`、`flask` を既にインストールしています。Galileo LangChainコールバックは `galileo` パッケージに含まれています。

{{< /step >}}

{{< step title="Galileo認証情報の設定"  >}}

EC2インスタンスには `OPENAI_API_KEY` と `OPENAI_BASE_URL` の環境変数が事前設定されており、アプリケーションで使用されます。

認証情報をアプリケーションの `.env` ファイルに追加します。

```ini
OPENAI_API_KEY="your-openai-api-key"
OPENAI_BASE_URL="https://lite-llm-proxy.splunko11y.com/v1"
GALILEO_API_KEY="your-galileo-api-key"
GALILEO_CONSOLE_URL="https://console.multitenant.galileocloud.io"
# Recommended: uncomment to group this workshop's traces under their own project
# and log stream. If you leave these commented out, Splunk Agent Observability uses a project and log
# stream both named "default".
# GALILEO_PROJECT="Workshop19"
# GALILEO_LOG_STREAM="TravelPlanner"
```

`GALILEO_PROJECT` と `GALILEO_LOG_STREAM` のコメントを外すと、ワークショップのトレースを見つけやすくなります。コメントアウトしたままでも問題ありません。その場合、トレースは `default` プロジェクトと `default` log streamに記録されます。

4. `main.py` の先頭付近、既存のimportと `load_dotenv()` 呼び出しの直後にGalileoを初期化します。環境変数を渡すことで、プロジェクトとlog streamは `.env` に設定されている場合はその値を使用し、設定されていない場合はSplunk Agent Observabilityの `default`/`default` にフォールバックします。

```python
from dotenv import load_dotenv
load_dotenv()

import os
from galileo import galileo_context

galileo_context.init(project=os.getenv("GALILEO_PROJECT"),
                     log_stream=os.getenv("GALILEO_LOG_STREAM"))
```

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="確認テスト" >}}

`.env` で `GALILEO_PROJECT` と `GALILEO_LOG_STREAM` をコメントアウトしたままにした場合、Splunk Agent Observabilityのどこにトレースが表示されますか？

{{< details summary="ここをクリックして回答を確認" >}}
`default` という名前のプロジェクトと `default` という名前のlog streamに記録されます。`main.py` は `os.getenv("GALILEO_PROJECT")` と `os.getenv("GALILEO_LOG_STREAM")` を渡しているため、変数が未設定の場合はこれらの値が `None` になり、Galileo SDKは組み込みの `default` プロジェクトと `default` log streamにフォールバックします。
{{< /details >}}
