---
title: 4.6 Message Abstractions
linkTitle: 4.6 Message Abstractions
weight: 6
---

## LangChain Message Abstractions

このアプリケーションは、1つの長いプロンプト文字列ではなく、LangChainのメッセージ抽象化を使用しています。

``` python
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
```

これが重要なのは、各ノードが以下を分離できるためです。

* システムロール
* ユーザータスク
* モデルのレスポンス

例:

```python
messages = [
    SystemMessage(content="You are a flight booking specialist. Provide concise options."),
    HumanMessage(content=step),
]
result = llm.invoke(messages)
```

### 知識チェック

システムメッセージ、ヒューマンメッセージ、AIメッセージをどのように定義しますか？

{{< details summary="ここをクリックして回答を表示" >}}
LangChainとLangGraphでは、メッセージは通常、誰が話しているか、会話の中でどのような役割を果たしているかによって分類されます。

* **システムメッセージ**: AIの動作に関するルールとコンテキストを設定します。モデルがインタラクション全体を通じてどのように応答すべきかを指示、制約、トーン、目標で定義します。
* **ヒューマンメッセージ**: ユーザーからの入力です。AIが応答すべき質問、リクエスト、または情報が含まれます。
* **AIメッセージ**: モデルのレスポンスです。システムの指示とヒューマンの入力に基づいて生成されたアシスタントの出力を表します。
{{< /details >}}
