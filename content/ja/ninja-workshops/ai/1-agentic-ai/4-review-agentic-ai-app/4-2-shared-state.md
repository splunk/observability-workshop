---
title: 4.2 共有ステート
linkTitle: 4.2 共有ステート
weight: 2
---

## LangGraph における共有ステート

このアプリで最も重要な LangGraph のコンセプトは、共有ステートオブジェクトです

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

このステートは、グラフ内のノードからノードへと移動します。

各ノードは以下を行います

* ステートから値を読み取る
* 何らかの処理を実行する
* 新しい値をステートに書き戻す
* `current_agent` を設定して次の処理を制御する

これは LangGraph の重要なメンタルモデルです**ステートフルなワークフローオーケストレーション**。

### 知識チェック

`messages` フィールドに使用されている構文をどのように説明しますか？

```python
messages: Annotated[List[AnyMessage], add_messages]
```

<details>
  <summary><b>ここをクリックして回答を確認</b></summary>

`messages: Annotated[List[AnyMessage], add_messages]` は2つのことを行います。

* `List[AnyMessage]` はフィールドの**型**を定義します：LangChain のメッセージオブジェクト（system、human、または AI メッセージ）のリストです。
* `Annotated[..., add_messages]` は **LangGraph の動作**を追加し、**このフィールドの更新をどのように処理するか**をグラフに指示します。

具体的には、`add_messages` はノードが新しいメッセージを書き込んだ際に、LangGraph が**既存のリストを上書きするのではなく、追記する**ことを意味します。
そのため、各ノードがメッセージを追加するたびに、会話履歴が増えていきます。

</details>
