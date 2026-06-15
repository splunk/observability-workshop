---
title: 実行とトレースの確認
linkTitle: 4. 実行とトレースの確認
weight: 4
time: 5 minutes
---

トラベルプランナーを実行し、リクエストを送信して、マルチエージェントのトレースが Galileo に記録されたことを確認します。

{{< exercise title="アプリの実行とトレースの確認" >}}

{{< step title="アプリの実行"  >}}
アプリを起動します:

{{< tabs id="run-app" >}}
{{% tab title="Script" %}}

```bash
python3 main.py
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```text
INFO:root:[INFO] Starting Flask server on http://0.0.0.0:8080
 * Serving Flask app 'main'
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
```

{{% /tab %}}
{{< /tabs >}}

{{< /step >}}

{{< step title="アプリにリクエストを送信"  >}}
2つ目のターミナルで、旅行計画のリクエストを送信します。計画された旅程が返されれば、コールバックが接続された状態でワークフローがエンドツーエンドで実行されていることが確認できます:

{{< tabs id="send-request" >}}
{{% tab title="Script" %}}

```bash
curl http://localhost:8080/travel/plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Philadelphia",
    "destination": "Florida",
    "user_request": "Planning a two day long trip from Philadelphia to Florida. Looking for a boutique hotel, business-class flights and unique experiences.",
    "travelers": 2
  }'
```

{{% /tab %}}
{{% tab title="Example Output" %}}

```json
{
  "activities_summary": "1. Everglades Airboat Tour – Explore unique wetlands and spot alligators.\n2. Kennedy Space Center Visit – Experience NASA exhibits and possibly a rocket launch.\n3. Miami Art Deco Walking Tour – Discover iconic architecture and vibrant street art.\n4. Key West Sunset Sail – Relax on a catamaran while watching a stunning sunset.\n5. Walt Disney World or Universal Studios – Enjoy world-class theme park attractions.\n6. Snorkeling at John Pennekamp Coral Reef – Dive into Florida's only living coral reef.\n7. St. Augustine Historic District Tour – Walk through America's oldest city with colonial charm.",
  "agent_steps": [
    {
      "agent": "coordinator",
      "status": "completed"
    },
    {
      "agent": "flight_specialist",
      "status": "completed"
    },
    {
      "agent": "hotel_specialist",
      "status": "completed"
    },
    {
      "agent": "activity_specialist",
      "status": "completed"
    },
    {
      "agent": "plan_synthesizer",
      "status": "completed"
    }
  ],
  "departure": "2026-07-09",
  "destination": "Florida",
  "final_itinerary": "**Two-Day Florida Trip Itinerary (July 9 - July 11, 2026)**  \n*Origin: Philadelphia (PHL) | Destination: Miami, Florida*\n\n---\n\n### Flights  \n- **Departure:** July 9, 2026  \n- **From:** Philadelphia International Airport (PHL)  \n- **To:** Miami International Airport (MIA)  \n- **Airline:** American Airlines (Business Class)  \n- **Departure Time:** 9:00 AM  \n- **Arrival Time:** 12:00 PM  \n- **Notes:** Non-stop flight, approx. $220 per person  \n\n---\n\n### Accommodation  \n**The Betsy – South Beach, Miami Beach**  \n- Stylish beachfront boutique hotel with an art-focused design  \n- Amenities: Pool, rooftop deck, spa, multiple dining options  \n- Location: Ideal for exploring Miami's vibrant culture and beach scene  \n\n---\n\n### Day 1: July 9, 2026  \n- **Afternoon:** Check-in at The Betsy and relax by the pool or rooftop deck  \n- **Evening:** Miami Art Deco Walking Tour – Discover iconic architecture and vibrant street art in South Beach  \n\n---\n\n### Day 2: July 10, 2026  \n- **Morning:** Everglades Airboat Tour – Explore unique wetlands and spot alligators on an exciting airboat ride  \n- **Afternoon:** Leisure time at the hotel or explore nearby Wynwood Arts District for its galleries and street art  \n- **Evening:** Dine at one of The Betsy's fine dining options or enjoy a sunset walk along the beach  \n\n---\n\n### Return Flight  \n- **Date:** July 11, 2026 (morning or afternoon, to be booked as per preference)  \n- **From:** Miami International Airport (MIA)  \n- **To:** Philadelphia International Airport (PHL)  \n- **Airline:** American Airlines (Business Class)  \n\n---\n\n**Summary:**  \nFly business class from Philadelphia to Miami, stay at the elegant Betsy boutique hotel on South Beach, and enjoy unique experiences including a Miami Art Deco walking tour and an Everglades airboat adventure. This itinerary blends comfort, culture, and nature for a memorable two-day Florida getaway.  \n\nWould you like assistance with booking flights, hotel reservations, or arranging the activities?",
  "flight_summary": "Here are some appealing flight options from Philadelphia (PHL) to Florida on 2026-07-09 for 2 travelers:\n\n1. Philadelphia (PHL) to Miami (MIA)\n   - Airline: American Airlines\n   - Departure: 09:00 AM\n   - Arrival: 12:00 PM\n   - Non-stop\n   - Approx. price: $220 per person\n\n2. Philadelphia (PHL) to Orlando (MCO)\n   - Airline: Delta Airlines\n   - Departure: 10:30 AM\n   - Arrival: 1:30 PM\n   - Non-stop\n   - Approx. price: $210 per person\n\n3. Philadelphia (PHL) to Tampa (TPA)\n   - Airline: Southwest Airlines\n   - Departure: 08:45 AM\n   - Arrival: 11:45 AM\n   - Non-stop\n   - Approx. price: $200 per person\n\nWould you like me to help you book any of these?",
  "hotel_summary": "Here are three boutique hotel options in Florida for 2 travelers from July 9 to July 16, 2026:\n\n1. **The Betsy – South Beach, Miami Beach**\n   - Stylish beachfront boutique hotel with art-focused design.\n   - Amenities: Pool, rooftop deck, spa, and multiple dining options.\n   \n2. **The Don CeSar – St. Pete Beach**\n   - Iconic pink historic hotel with a luxurious boutique feel.\n   - Amenities: Private beach, pool, spa, and fine dining.\n\n3. **The Vagabond Hotel – Miami**\n   - Retro-chic boutique hotel with a vibrant, artistic vibe.\n   - Amenities: Pool, bar, and close to Wynwood Arts District.\n\nWould you like pricing and availability details for any of these?",
  "origin": "Philadelphia",
  "return_date": "2026-07-16",
  "session_id": "2fa9ce38-0f1f-4015-8004-447b48b4546e",
  "travellers": 2
}
```

{{% /tab %}}
{{< /tabs >}}

{{< /step >}}

{{< step title="Galileo でトレースを確認" >}}

Galileo コンソール (<https://console.multitenant.galileocloud.io/splunkse>) で、`Workshop19Galileo` プロジェクトを開きます（`.env` ファイルで `GALILEO_PROJECT` 環境変数をコメントアウトした場合を除きます）。

次に、ログストリームを見つけるために、まず EC2 インスタンスで `INSTANCE` 環境変数を確認します:

```bash
echo $INSTANCE
```

`TravelPlanner-` の後にインスタンス名が続くログストリームを探します。例えば、`TravelPlanner-shw-9306` のようになります。

{{< /step >}}

{{< step title="トレースの検索" >}}
最新のトレースを開きます。コールバックはグラフレベルで接続されているため、リクエストに対して各エージェントノードのネストされた LLM スパンを含む単一のトレースが表示されるはずです:

* `coordinator`
* `flight_specialist`
* `hotel_specialist`
* `activity_specialist`
* `plan_synthesizer`

{{< /step >}}

{{< step title="スパンの検査" >}}
任意のスパンを展開し、**システムメッセージとヒューマンメッセージ**、**モデルのレスポンス**、**モデル名**、**トークン数**、および**レイテンシ**がキャプチャされていることを確認します。

{{% notice title="トレースが表示されない場合" style="tip" icon="exclamation-triangle" %}}

* アプリが実行されている環境で `GALILEO_API_KEY` が設定されていることを確認します（`load_dotenv()` 経由で `.env` を読み込みます）。
* 正しいプロジェクトとログストリームを表示していることを確認します: `GALILEO_PROJECT` / `GALILEO_LOG_STREAM` を設定した場合はその値、設定していない場合は `default` / `default` です。
* プロジェクトが表示されない場合は、正しい権限がない可能性があります。
* `python3 main.py` を実行しているターミナルで、Galileo のエラーがアプリログに出力されていないか確認します。
* Web ページの左上で `splunkse` 組織に所属していることを確認します。

{{% /notice %}}
{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="理解度チェック" >}}

1つの旅行計画リクエストで、5つの個別のトレースではなく、5つのネストされた LLM スパンを含む1つのトレースが生成されます。なぜでしょうか？

{{< details summary="ここをクリックして回答を表示" >}}
LangGraph ワークフロー全体がリクエストごとに**1つのルートラン**として実行され、コールバックはそのランの config に接続されているためです。LangGraph は5つのノード（coordinator、flight、hotel、activity、synthesizer）をその単一のラン内で実行するため、各ノードの `llm.invoke(...)` は同じトレースの下の子スパンになります。代わりに各ノードで新しいコールバックと新しいランを作成した場合、5つの切断されたトレース（およびセッション）が生成され、リクエストのエンドツーエンドのビューが失われます。
{{< /details >}}
