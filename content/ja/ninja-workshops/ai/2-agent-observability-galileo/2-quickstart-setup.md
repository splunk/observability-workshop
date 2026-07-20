---
title: クイックスタートセットアップ
linkTitle: 2. クイックスタートセットアップ
weight: 2
time: 5 minutes
---

Galileo SDKをトラベルプランナーの環境に追加し、Splunk Agent Observabilityのトレーシングを初期化します。

{{< exercise title="クイックスタートセットアップ" >}}

{{< step title="環境のアクティベート"  >}}

アプリケーションディレクトリに移動し、[Monitoring Agentic AI Applications](ninja-workshops/ai/18-agentic-ai/)で作成した仮想環境をアクティベートします（または新しく作成します）。

```bash
cd ~/workshop/agentic-ai/base-app
source .venv/bin/activate
```

{{< /step >}}

{{< step title="Galileo SDKのインストール"  >}}

アプリケーションの既存の依存関係と合わせてGalileo SDKをインストールします。

```bash
pip install galileo python-dotenv
```

アプリケーションは `requirements.txt` を通じて `langchain`、`langchain-openai`、`langgraph`、`flask` を既にインストールしています。Galileo LangChainコールバックは `galileo` パッケージに含まれています。

{{< /step >}}

{{< step title="Galileo認証情報の設定"  >}}

アプリケーションの `.env` ファイルに認証情報を追加します。

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

`GALILEO_PROJECT` と `GALILEO_LOG_STREAM` のコメントを外すと、ワークショップのトレースを見つけやすくなります。コメントアウトしたままでも問題ありません。その場合、トレースは `default` プロジェクトと `default` ログストリームに記録されます。

4. `main.py` の先頭付近、既存のimportと `load_dotenv()` 呼び出しの直後に、Splunk Agent Observabilityを初期化します。環境変数を渡すことで、`.env` に設定されている場合はそのプロジェクトとログストリームが使用され、設定されていない場合はSplunk Agent Observabilityの `default`/`default` にフォールバックします。

```python
import os
from galileo import galileo_context

galileo_context.init(project=os.getenv("GALILEO_PROJECT"),
                     log_stream=os.getenv("GALILEO_LOG_STREAM"))
```

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="知識チェック" >}}

`.env` で `GALILEO_PROJECT` と `GALILEO_LOG_STREAM` をコメントアウトしたままにした場合、Splunk Agent Observabilityのどこにトレースが表示されますか？

{{< details summary="ここをクリックして回答を表示" >}}
`default` という名前のプロジェクトと `default` という名前のログストリームに記録されます。`main.py` が `os.getenv("GALILEO_PROJECT")` と `os.getenv("GALILEO_LOG_STREAM")` を渡しているため、変数が未設定の場合はこれらの値が `None` になり、Galileo SDKは組み込みの `default` プロジェクトと `default` ログストリームにフォールバックします。
{{< /details >}}
