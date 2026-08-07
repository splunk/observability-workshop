---
title: Galileo Callbackの接続
linkTitle: 2. Galileo Callbackの接続
weight: 2
time: 3 minutes
---

エージェントはLangGraphワークフローを非同期で実行するため、Galileoの **async** callbackを接続します。callbackはグラフレベルで渡されるため、すべてのノードに自動的に伝播し、ツールごとの計装は不要です。

{{< exercise title="エージェントにcallbackを追加する" >}}

{{< step title="importの追加" >}}

`~/workshop/healthcare-assistant/2-app-with-instrumentation/agent.py` ファイルを編集用に開きます。importセクションの末尾、`class State(TypedDict)` の直前に以下を追加します。

```python
import os
from galileo import galileo_context
from galileo.handlers.langchain import GalileoAsyncCallback
```

{{< /step >}}

{{< step title="グラフの呼び出しをGalileoコンテキストでラップする" >}}

`_process_query_async` のベースバージョンはトレーシングなしでグラフを呼び出します。

```python
    async def _process_query_async(self, messages: List[Dict[str, str]]) -> str:
        if not self.tools:
            self.load_tools()
        self.graph = self._build_graph()

        langchain_messages: List[BaseMessage] = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        result = await self.graph.ainvoke(
            {"messages": langchain_messages},
            self.langgraph_config,
        )
        if result["messages"]:
            return result["messages"][-1].content
        return "No response generated"
```

これを更新して `galileo_context` を開き、エージェントの `session_id` をキーとしてセッションを開始し、新しい `GalileoAsyncCallback` をrun configに接続します。

```python
    async def _process_query_async(self, messages: List[Dict[str, str]]) -> str:
        if not self.tools:
            self.load_tools()
        self.graph = self._build_graph()

        langchain_messages: List[BaseMessage] = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))

        with galileo_context(
            project=os.getenv("GALILEO_PROJECT"),
            log_stream=os.getenv("GALILEO_LOG_STREAM"),
        ):
            galileo_context.start_session(external_id=self.session_id)

            # One callback per request keeps each user turn in its own trace.
            callback = GalileoAsyncCallback()
            run_config = {**self.langgraph_config, "callbacks": [callback]}

            result = await self.graph.ainvoke(
                {"messages": langchain_messages},
                run_config,
            )
        if result["messages"]:
            return result["messages"][-1].content
        return "No response generated"
```

{{< /step >}}

{{< /exercise >}}

{{% notice title="なぜリクエストごとに1つのcallbackなのか？" style="info" %}}

`_process_query_async` の呼び出しごとに1つの `GalileoAsyncCallback` を作成することで、各ユーザーターンが独自のTraceに保持されます。LangGraphのrun configに接続されているため、すべてのノードのLLMおよびツール呼び出しが同じTrace配下のネストされたSpanになり、切断されたSpanの山ではなく、ターンのエンドツーエンドビューが得られます。

{{% /notice %}}

{{% notice title="トラブルシューティング" style="tip" icon="exclamation-triangle" %}}

以下のコマンドを実行して、変更内容をリファレンスソリューションと比較します。

```bash
cd ~/workshop/healthcare-assistant/2-app-with-instrumentation/
diff agent.py agent-with-instrumentation.py
```

{{% /notice %}}

{{< checkpoint title="理解度チェック" >}}

このアプリが `GalileoCallback` ではなく `GalileoAsyncCallback` を使用するのはなぜですか？

{{< details summary="ここをクリックして回答を表示" >}}
エージェントがグラフを **非同期で** ストリーム/呼び出し（`self.graph.ainvoke(...)`）するためです。非同期callbackは非同期実行に対応します。`invoke(...)` を呼び出す同期アプリケーションの場合は、代わりに `GalileoCallback` を使用します。
{{< /details >}}
