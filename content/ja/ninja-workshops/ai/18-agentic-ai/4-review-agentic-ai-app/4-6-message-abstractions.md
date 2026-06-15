---
title: 4.6 Message Abstractions
linkTitle: 4.6 Message Abstractions
weight: 6
---

## LangChain メッセージ抽象化

このアプリケーションでは、1つの長いプロンプト文字列ではなく、LangChain のメッセージ抽象化を使用しています。

``` python
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
```

これが重要な理由は、各ノードが以下を分離できるためです

* システムロール
* ユーザータスク
* モデルのレスポンス

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

{{< details summary="ここをクリックして回答を表示" >}}
LangChain および LangGraph では、メッセージは通常、誰が話しているか、会話の中でどのような役割を果たしているかによって分類されます

* **System message**: AI の動作に関するルールとコンテキストを設定します。モデルがインタラクション全体を通じてどのように応答すべきかを導く指示、制約、トーン、目標を定義します。
* **Human message**: ユーザーからの入力です。AI が応答すべき質問、リクエスト、または情報が含まれます。
* **AI message**: モデルのレスポンスです。システムの指示とユーザー入力に基づいて生成されたアシスタントの出力を表します。
{{< /details >}}
