---
title: クイックスタートセットアップ
linkTitle: 2. クイックスタートセットアップ
weight: 2
time: 5 minutes
---

まず、Galileo SDK を旅行プランナーの環境に追加し、Galileo トレーシングを初期化します。

{{< exercise title="クイックスタートセットアップ" >}}

{{< step title="環境のアクティベート"  >}}

アプリディレクトリに移動し、新しい仮想環境を作成します

```bash
cd ~/workshop/agentic-ai/base-app
python3 -m venv .venv
source .venv/bin/activate
```

{{< /step >}}

{{< step title="Galileo SDK のインストール"  >}}

このアプリは `requirements.txt` を通じて `langchain`、`langchain-openai`、`langgraph`、`flask` を既にインストールしています。Galileo の LangChain コールバックは `galileo` パッケージに含まれているので、ここで追加しましょう。

`~/workshop/agentic-ai/base-app/requirements.txt` ファイルを開いて編集し、以下のパッケージを追加します

```bash
galileo
python-dotenv
```

次に、すべてのパッケージを仮想環境に追加します

```bash
pip install -r requirements.txt
```

{{< /step >}}

{{< step title="Galileo 認証情報の設定"  >}}

EC2 インスタンスには `OPENAI_API_KEY` と `OPENAI_BASE_URL` 環境変数が事前に設定されており、アプリケーションで使用されます。

追加の環境変数を定義するために、`~/workshop/agentic-ai/base-app/.env` という名前の新しいファイルを作成し、認証情報を追加します

```ini
GALILEO_API_KEY="your-galileo-api-key"
GALILEO_CONSOLE_URL="https://console.multitenant.galileocloud.io"
# If you comment out the next two uncommented lines, Galileo uses a project and log
# stream both named "default".
GALILEO_PROJECT="Workshop19Galileo"
GALILEO_LOG_STREAM="TravelPlanner-${INSTANCE}"
```

{{< /step >}}

{{< step title="アプリでの Galileo 初期化"  >}}
`~/workshop/agentic-ai/base-app/main.py` の先頭付近、`import logging` の直前で Galileo を初期化します。環境変数を渡すことで、`.env` に設定されている場合はそのプロジェクトとログストリームが使用され、設定されていない場合は Galileo のデフォルト値 `default`/`default` にフォールバックします

```python
import os
from dotenv import load_dotenv
from galileo import galileo_context

load_dotenv()

galileo_context.init(project=os.getenv("GALILEO_PROJECT"),
                     log_stream=os.getenv("GALILEO_LOG_STREAM"))
```

{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="確認テスト" >}}

`.env` で `GALILEO_PROJECT` と `GALILEO_LOG_STREAM` 変数をコメントアウトした場合、トレースは Galileo のどこに表示されますか？

{{< details summary="ここをクリックして回答を確認" >}}
`default` という名前のプロジェクトと `default` という名前のログストリームに記録されます。`main.py` が `os.getenv("GALILEO_PROJECT")` と `os.getenv("GALILEO_LOG_STREAM")` を渡しているため、変数が未設定の場合はこれらの値が `None` になり、Galileo SDK は組み込みの `default` プロジェクトと `default` ログストリームにフォールバックします。
{{< /details >}}
