---
title: 4.2 共有状態
linkTitle: 4.2 共有状態
weight: 2
---

## LangGraph における共有状態

このアプリで最も重要な LangGraph の概念は、共有状態オブジェクトです。

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

この状態は、グラフ内をノードからノードへと受け渡されていきます。

各ノードでは以下のことを行います。

* 状態から値を読み取る
* 何らかの処理を実行する
* 新しい値を状態に書き戻す
* current_agent を設定して次に何が起こるかを制御する

これは LangGraph の重要なメンタルモデルである **ステートフルなワークフローオーケストレーション** です。

### 理解度チェック

`messages` フィールドで使われている構文をどのように説明しますか？

```python
messages: Annotated[List[AnyMessage], add_messages]
```

<details>
  <summary><b>クリックして回答を表示</b></summary>

`messages: Annotated[List[AnyMessage], add_messages]` は2つのことを行っています。

* `List[AnyMessage]` はフィールドの **型** を定義しています。これは LangChain のメッセージオブジェクト（system、human、AI メッセージ）のリストです。
* `Annotated[..., add_messages]` は **LangGraph の動作** を追加し、**このフィールドへの更新がどのように扱われるべきか** をグラフに伝えます。

具体的には、`add_messages` は、ノードが新しいメッセージを書き込んだときに、LangGraph が **既存のリストを上書きするのではなく追加する** ことを意味します。
そのため、各ノードがメッセージを追加するたびに会話履歴が増えていきます。

</details>
