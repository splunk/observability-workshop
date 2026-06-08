---
title: 4.2 共有ステート
linkTitle: 4.2 共有ステート
weight: 2
---

## LangGraph の共有ステート

このアプリにおける最も重要な LangGraph のコンセプトは、共有ステートオブジェクトです

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

このステートはグラフ内のノードからノードへと移動します。

各ノードは

* ステートから値を読み取ります
* 何らかの処理を実行します
* 新しい値をステートに書き戻します
* `current_agent` を設定して次に何が起こるかを制御します

これは LangGraph の重要なメンタルモデルです**ステートフルなワークフローオーケストレーション**。

### 理解度チェック

`messages` フィールドに使用されている構文をどのように説明しますか？

```python
messages: Annotated[List[AnyMessage], add_messages]
```

{{< details summary="ここをクリックして回答を表示" >}}
`messages: Annotated[List[AnyMessage], add_messages]` は2つのことを行います。

* `List[AnyMessage]` はフィールドの**型**を定義します：LangChain のメッセージオブジェクト（system、human、または AI メッセージ）のリストです。
* `Annotated[..., add_messages]` は **LangGraph の動作**を追加し、**このフィールドへの更新がどのように処理されるべきか**をグラフに伝えます。

具体的には、`add_messages` はノードが新しいメッセージを書き込んだとき、LangGraph が**既存のリストを上書きするのではなく、追加する**ことを意味します。
そのため、各ノードがメッセージを追加するにつれて会話履歴が増えていきます。
{{< /details >}}
