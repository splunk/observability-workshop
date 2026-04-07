from __future__ import annotations
import traceback
from flask import Flask, request, jsonify
from crew_runner import plan_travel_internal
import logging
import sys

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

print(f"app.py: name is {__name__}", flush=True)

@app.route("/travel/plan", methods=["POST"])
def plan():
    try:
        data = request.get_json() or {}

        origin = data.get("origin", "Seattle")
        destination = data.get("destination", "Paris")
        user_request = data.get(
            "user_request",
            f"Planning a week-long trip from {origin} to {destination}. "
            "Looking for boutique hotel, flights and unique experiences.",
        )
        travellers = int(data.get("travellers", 2))

        logging.info(f"[SERVER] Processing travel plan: {origin} -> {destination}")

        result = plan_travel_internal(
            origin=origin,
            destination=destination,
            user_request=user_request,
            travellers=travellers,
        )

        logging.info("[SERVER] Travel plan completed successfully")
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"[SERVER] Error processing travel plan: {e}")
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "service": "travel-planner-flask-crewai"}), 200

if __name__ == "__main__":
    logging.info("[INFO] Starting Flask server on http://0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080, debug=False)