---
title: 4.6 Message Abstractions
linkTitle: 4.6 Message Abstractions
weight: 6
---

## LangChain Message Abstractions

このアプリケーションは、1つの長いプロンプト文字列ではなく、LangChain のメッセージ抽象化を使用しています。

``` python
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
```

これは、各ノードで以下を分離できるため重要です

* システムロール
* ユーザータスク
* モデルの応答

例

```python
messages = [
    SystemMessage(content="You are a flight booking specialist. Provide concise options."),
    HumanMessage(content=step),
]
result = llm.invoke(messages)
```

### 理解度チェック

system、human、AI メッセージをどのように定義しますか？

<details>
  <summary><b>ここをクリックして回答を表示</b></summary>

LangChain と LangGraph では、メッセージは通常、誰が話しているか、および会話を導く上でどのような役割を果たしているかによって分類されます

* **System message**: AI の動作に関するルールとコンテキストを設定します。インタラクション全体を通じてモデルがどのように応答すべきかを導く指示、制約、トーン、および目標を定義します。
* **Human message**: ユーザーからの入力です。AI が応答すべき質問、リクエスト、または情報を含みます。
* **AI message**: モデルの応答です。システムの指示とユーザーの入力に基づいて、アシスタントが生成した出力を表します。

</details>
