---
title: 4.6 Message Abstractions
linkTitle: 4.6 Message Abstractions
weight: 6
---

## LangChain Message Abstractions

このアプリケーションでは、長いプロンプト文字列を 1 つだけ使うのではなく、LangChain のメッセージ抽象化を利用しています。

``` python
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)
```

これは、各ノードが次の要素を分離できるという点で重要です。

* system ロール
* ユーザータスク
* モデルのレスポンス

例えば、次のようになります。

```python
messages = [
    SystemMessage(content="You are a flight booking specialist. Provide concise options."),
    HumanMessage(content=step),
]
result = llm.invoke(messages)
```

### Knowledge Check

system、human、AI メッセージをどのように定義しますか？

<details>
  <summary><b>クリックすると回答が表示されます</b></summary>

LangChain と LangGraph では、メッセージは通常、誰が発言しているか、そして会話を導くうえでどのような役割を担うかによって分類されます。

* **System message**: AI の振る舞いに関するルールとコンテキストを設定します。やり取り全体を通じてモデルがどのように応答すべきかを導く、指示・制約・トーン・ゴールを定義します。
* **Human message**: ユーザーからの入力です。AI が応答すべき質問・要求・情報を含みます。
* **AI message**: モデルからのレスポンスです。system の指示と human の入力に基づいてアシスタントが生成した出力を表します。

</details>
