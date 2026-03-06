import json
import os
import urllib.request

from flask import Flask, jsonify

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", " ")
REALM = os.environ.get("REALM", " ")
INSTANCE = os.environ.get("INSTANCE", " ")


@app.route("/hello")
def hello():
    return jsonify({
        "message": "Hello from the OBI Workshop warm-up!",
        "host": INSTANCE,
    })


def send_heartbeat():
    """Send a single app.heartbeat gauge to the Splunk Ingest API."""
    url = f"https://ingest.{REALM}.signalfx.com/v2/datapoint"
    payload = json.dumps({
        "gauge": [{
            "metric": "app.heartbeat",
            "value": 1,
            "dimensions": {
                "service.name": f"bare-app-{INSTANCE}",
                "host.name": INSTANCE,
                "deployment.environment": "ebpf-bare-app",
            },
        }],
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-SF-Token": ACCESS_TOKEN,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Heartbeat sent to Splunk ({resp.status})")
    except Exception as exc:
        print(f"Heartbeat failed: {exc}")


if __name__ == "__main__":
    send_heartbeat()
    app.run(host="0.0.0.0", port=5150)
