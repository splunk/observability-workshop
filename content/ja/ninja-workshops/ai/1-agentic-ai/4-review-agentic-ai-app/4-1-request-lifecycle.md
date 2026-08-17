---
title: 4.1 リクエストのライフサイクル
linkTitle: 4.1 リクエストのライフサイクル
weight: 1
---

## アプリケーションの動作

大まかに言うと、このアプリケーションはリクエストを受け取り、それを複数ステップのワークフローに変換します

* coordinator
* flight specialist
* hotel specialist
* activity specialist
* synthesizer

メインのフローは次のようになっています

```python
@app.route("/travel/plan", methods=["POST"])
def plan():
    data = request.get_json()

    origin = data.get("origin", "Seattle")
    destination = data.get("destination", "Paris")
    user_request = data.get(
        "user_request",
        f"Planning a week-long trip from {origin} to {destination}. "
        "Looking for boutique hotel, flights and unique experiences.",
    )
    travellers = int(data.get("travellers", 2))

    result = plan_travel_internal(
        origin=origin,
        destination=destination,
        user_request=user_request,
        travellers=travellers
    )

    return jsonify(result), 200
```

この流れを分かりやすく説明すると、次のようになります

1. Flask がリクエストを受信します
2. `plan_travel_internal()` がワークフローの状態を構築します
3. LangGraph がノードを実行します
4. 各ノードが状態を更新します
5. 最終的な旅程が JSON として返されます

### 知識チェック

この API フローにおいて、LangGraph のワークフローは実際にどこで実行が開始されますか？

<details>
  <summary><b>ここをクリックして回答を表示</b></summary>

`plan_travel_internal()` の内部で開始されます。Flask のルートはリクエストの受信と
パラメータの抽出のみを行います。`plan_travel_internal()` がワークフローの状態を初期化し、
LangGraph のグラフを呼び出します。その後、ノード（coordinator、specialist、synthesizer）が
状態を更新しながら実行され、最終的な旅程が生成されます。

</details>
