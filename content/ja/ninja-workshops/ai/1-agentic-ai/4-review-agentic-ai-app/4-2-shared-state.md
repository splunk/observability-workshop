---
title: 4.2 共有ステート
linkTitle: 4.2 Shared State
weight: 2
---

## LangGraphにおける共有ステート

このアプリで最も重要なLangGraphの概念は、共有ステートオブジェクトです。

```python
class PlannerState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    user_request: str
    session_id: str
    origin: str
    destination: str
    departure: str
    return_date: str
    travellers: int
    flight_summary: Optional[str]
    hotel_summary: Optional[str]
    activities_summary: Optional[str]
    final_itinerary: Optional[str]
    current_agent: str
```

このステートはグラフ内をノードからノードへと移動します。

各ノードは以下を行います。

* ステートから値を読み取る
* 何らかの処理を行う
* 新しい値をステートに書き戻す
* `current_agent` を設定して次に何が起こるかを制御する

これはLangGraphの重要なメンタルモデルである **ステートフルなワークフローオーケストレーション** です。

### 知識チェック

`messages` フィールドに使われている構文をどのように説明しますか？

```python
messages: Annotated[List[AnyMessage], add_messages]
```

{{< details summary="ここをクリックして回答を確認" >}}
`messages: Annotated[List[AnyMessage], add_messages]` は2つのことを行います。

* `List[AnyMessage]` はフィールドの **型** を定義します。これはLangChainメッセージオブジェクト（system、human、またはAIメッセージ）のリストです。
* `Annotated[..., add_messages]` は **LangGraphの動作** を追加し、 **このフィールドの更新がどのように処理されるか** をグラフに伝えます。

具体的には、`add_messages` はノードが新しいメッセージを書き込んだとき、LangGraphが **既存のリストを上書きするのではなく、追記する** ことを意味します。
そのため、各ノードがメッセージを追加するたびに会話履歴が増えていきます。
{{< /details >}}
