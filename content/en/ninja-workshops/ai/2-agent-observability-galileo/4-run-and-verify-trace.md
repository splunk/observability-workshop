---
title: Run and Verify the Trace
linkTitle: 4. Run and Verify the Trace
weight: 4
time: 5 minutes
---

Run the travel planner, send a request through it, then confirm the multi-agent trace landed in
Splunk Agent Observability.

{{< exercise title="Run the app and verify the trace" >}}

{{< step title="Active Environment" >}}
Navigate to the base-app directory:

```bash
cd ~/workshop/agentic-ai/base-app
```

{{< /step >}}

{{< step title="Run the app"  >}}
Start the app:

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

In a second terminal, which is signed in to the same environment, send a travel-planning request. You should get the planned itinerary back,
confirming the workflow still runs end-to-end with the callback attached:

{{< step title="Send a request to the app"  >}}
In a second terminal, send a travel-planning request. You should get the planned itinerary back, confirming the workflow still runs end-to-end with the callback attached:

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
  "activities_summary": "1. Everglades Airboat Tour – Explore unique wetlands and spot alligators.\n2. Kennedy Space Center Visit – Experience NASA exhibits and possibly a rocket launch.\n3. Miami Art Deco Walking Tour – Discover iconic architecture and vibrant street art.\n4. Key West Sunset Sail – Relax on a catamaran while watching a stunning sunset.\n5. Walt Disney World or Universal Studios – Enjoy world-class theme park attractions.\n6. Snorkeling at John Pennekamp Coral Reef – Dive into Florida’s only living coral reef.\n7. St. Augustine Historic District Tour – Walk through America’s oldest city with colonial charm.",
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
  "final_itinerary": "**Two-Day Florida Trip Itinerary (July 9 - July 11, 2026)**  \n*Origin: Philadelphia (PHL) | Destination: Miami, Florida*\n\n---\n\n### Flights  \n- **Departure:** July 9, 2026  \n- **From:** Philadelphia International Airport (PHL)  \n- **To:** Miami International Airport (MIA)  \n- **Airline:** American Airlines (Business Class)  \n- **Departure Time:** 9:00 AM  \n- **Arrival Time:** 12:00 PM  \n- **Notes:** Non-stop flight, approx. $220 per person  \n\n---\n\n### Accommodation  \n**The Betsy – South Beach, Miami Beach**  \n- Stylish beachfront boutique hotel with an art-focused design  \n- Amenities: Pool, rooftop deck, spa, multiple dining options  \n- Location: Ideal for exploring Miami’s vibrant culture and beach scene  \n\n---\n\n### Day 1: July 9, 2026  \n- **Afternoon:** Check-in at The Betsy and relax by the pool or rooftop deck  \n- **Evening:** Miami Art Deco Walking Tour – Discover iconic architecture and vibrant street art in South Beach  \n\n---\n\n### Day 2: July 10, 2026  \n- **Morning:** Everglades Airboat Tour – Explore unique wetlands and spot alligators on an exciting airboat ride  \n- **Afternoon:** Leisure time at the hotel or explore nearby Wynwood Arts District for its galleries and street art  \n- **Evening:** Dine at one of The Betsy’s fine dining options or enjoy a sunset walk along the beach  \n\n---\n\n### Return Flight  \n- **Date:** July 11, 2026 (morning or afternoon, to be booked as per preference)  \n- **From:** Miami International Airport (MIA)  \n- **To:** Philadelphia International Airport (PHL)  \n- **Airline:** American Airlines (Business Class)  \n\n---\n\n**Summary:**  \nFly business class from Philadelphia to Miami, stay at the elegant Betsy boutique hotel on South Beach, and enjoy unique experiences including a Miami Art Deco walking tour and an Everglades airboat adventure. This itinerary blends comfort, culture, and nature for a memorable two-day Florida getaway.  \n\nWould you like assistance with booking flights, hotel reservations, or arranging the activities?",
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

In the Splunk Agent Observability console (https://console.multitenant.galileocloud.io/splunkse), open the project and log stream your traces landed in. If you uncommented
`GALILEO_PROJECT` and `GALILEO_LOG_STREAM` in your `.env`, that's `Workshop19` /
`TravelPlanner`; otherwise it's the `default` project and `default` log stream.
{{< /step >}}

{{< step title="Find the trace" >}}
Open the most recent trace. Because the callback was attached at the graph level, you should see a
   single trace for the request containing a nested LLM span for each agent node:

* `coordinator`
* `flight_specialist`
* `hotel_specialist`
* `activity_specialist`
* `plan_synthesizer`

{{< /step >}}

{{< step title="Inspect the spans" >}}
Expand any span and verify it captured the **system and human messages**, the **model response**, the **model name**, **token counts**, and **latency**.

{{% notice title="No trace showing up?" style="tip" icon="exclamation-triangle" %}}

* Confirm you were able to log-in to the same environment before sending the request payload, by using a separate terminal session.
* Confirm `GALILEO_API_KEY` is set in the environment the app runs in (it loads `.env` via
  `load_dotenv()`).
* Confirm you're viewing the right project and log stream: the values from `GALILEO_PROJECT` /
  `GALILEO_LOG_STREAM` if you set them, or `default` / `default` if you didn't.
* If you don't see the project, you likely don't have the correct permissions.
* Check the app logs for Splunk Agent Observability errors in the bash where `python3 main.py` is running.
* Confirm that you are in the correct organization in the top left of the web page.

{{% /notice %}}
{{< /step >}}

{{< /exercise >}}

{{< checkpoint title="Knowledge Check" >}}

A single travel-planning request produces one trace containing five nested LLM spans, rather
than five separate traces. Why?

{{< details summary="Click here to see the answer" >}}
Because the whole LangGraph workflow runs as one root run per request, and the callback was
attached to that run's config. LangGraph executes the five nodes (coordinator, flight, hotel,
activity, synthesizer) within that single run, so each node's `llm.invoke(...)` becomes a child
span under the same trace. If you instead created a new callback and a new run for each node, you'd
get five disconnected traces (and sessions) and lose the end-to-end view of the request.
{{< /details >}}
