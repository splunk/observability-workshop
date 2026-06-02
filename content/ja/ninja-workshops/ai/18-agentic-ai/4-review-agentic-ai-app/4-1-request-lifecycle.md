---
title: 4.1 Request Lifecycle
linkTitle: 4.1 Request Lifecycle
weight: 1
---

## アプリケーションの動作内容

このアプリケーションは大まかに、リクエストを受け取り、それを複数ステップのワークフローに変換します。

* coordinator
* flight specialist
* hotel specialist
* activity specialist
* synthesizer

メインのフローは次のようになっています。

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

これを分かりやすく説明すると、次のとおりです。

1. Flask がリクエストを受け取ります
2. `plan_travel_internal()` がワークフローの状態を構築します
3. LangGraph がノードを実行します
4. 各ノードが状態を更新します
5. 最終的な旅程が JSON として返されます

### 理解度チェック

この API フローの中で、LangGraph のワークフローは実際にどこで実行が始まるでしょうか？

<details>
  <summary><b>クリックして回答を表示</b></summary>

実行は `plan_travel_internal()` の内部で始まります。Flask のルートはリクエストを受け取ってパラメータを抽出するだけです。`plan_travel_internal()` がワークフローの状態を初期化して LangGraph のグラフを呼び出し、その後、ノード（coordinator、specialist 群、synthesizer）が状態を更新しながら実行され、最終的な旅程が生成されます。

</details>
