---
title: 4.1 リクエストライフサイクル
linkTitle: 4.1 リクエストライフサイクル
weight: 1
---

## アプリケーションの動作

大まかに言うと、このアプリケーションはリクエストを受け取り、それを複数ステップのワークフローに変換します

* coordinator
* flight specialist
* hotel specialist
* activity specialist
* synthesizer

メインフローは以下のようになります

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

この流れを分かりやすく説明すると

1. Flask がリクエストを受信します
2. `plan_travel_internal()` がワークフローの状態を構築します
3. LangGraph がノードを実行します
4. 各ノードが状態を更新します
5. 最終的な旅程が JSON として返されます

### 理解度チェック

この API フローにおいて、LangGraph ワークフローは実際にどこで実行を開始しますか？

{{< details summary="ここをクリックして回答を確認" >}}
`plan_travel_internal()` の内部で開始されます。Flask ルートはリクエストを受信し、
パラメータを抽出するだけです。`plan_travel_internal()` がワークフローの状態を初期化し、
LangGraph グラフを呼び出します。その後、ノード（coordinator、specialists、synthesizer）が
実行され、最終的な旅程が生成されるまで状態を更新し続けます。
{{< /details >}}
