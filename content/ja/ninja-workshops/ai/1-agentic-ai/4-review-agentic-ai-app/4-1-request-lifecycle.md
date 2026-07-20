---
title: 4.1 リクエストライフサイクル
linkTitle: 4.1 リクエストライフサイクル
weight: 1
---

## アプリケーションの動作

大まかに言うと、このアプリケーションはリクエストを受け取り、複数ステップのワークフローに変換します。

* coordinator
* flight specialist
* hotel specialist
* activity specialist
* synthesizer

メインフローは次のようになります。

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

この流れを分かりやすく説明すると次のようになります。

1. Flaskがリクエストを受信する
2. `plan_travel_internal()` がワークフローの状態を構築する
3. LangGraphがノードを実行する
4. 各ノードが状態を更新する
5. 最終的な旅程がJSONとして返される

### 理解度チェック

このAPIフローにおいて、LangGraphワークフローが実際に実行を開始するのはどこですか？

{{< details summary="ここをクリックして回答を表示" >}}
`plan_travel_internal()` の内部で開始されます。Flaskルートはリクエストを受信してパラメータを抽出するだけです。`plan_travel_internal()` がワークフローの状態を初期化し、LangGraphグラフを呼び出します。その後、ノード（coordinator、specialist、synthesizer）が状態を更新しながら実行され、最終的な旅程が生成されます。
{{< /details >}}
