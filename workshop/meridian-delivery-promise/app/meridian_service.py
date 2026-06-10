import html
import logging
import os
import random
import time
from pathlib import Path
from typing import Any

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("meridian-delivery-promise")

SERVICE_ROLE = os.getenv("SERVICE_ROLE", "patient-portal")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
STATE_FILE = Path(os.getenv("MERIDIAN_INCIDENT_MODE_FILE", "/state/incident-mode"))
DEFAULT_INCIDENT_MODE = os.getenv("MERIDIAN_INCIDENT_MODE", "healthy")
PORT = int(os.getenv("PORT", "8080"))

ROUTE_PLANNER_URL = os.getenv("ROUTE_PLANNER_URL", "http://route-planner-api:8080")
COURIER_API_URL = os.getenv("COURIER_API_URL", "http://courier-mobile-api:8080")
NOTIFICATION_URL = os.getenv("NOTIFICATION_URL", "http://notification-gateway:8080")
GEOCODING_URL = os.getenv("GEOCODING_URL", "http://geocoding-provider:8080")
PATIENT_PORTAL_URL = os.getenv("PATIENT_PORTAL_URL", "http://patient-portal:8080")

REGIONS = ["north-hub", "south-hub", "east-hub", "west-hub"]
PATIENTS = ["Avery", "Jordan", "Morgan", "Riley", "Taylor"]
WINDOWS = ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00"]
VALID_MODES = {"healthy", "geocode-latency", "queue-backlog", "patient-portal-slow"}

app = FastAPI(title=f"Meridian Delivery Promise - {SERVICE_ROLE}")
tracer = trace.get_tracer(__name__)


def incident_mode() -> str:
    if STATE_FILE.exists():
        mode = STATE_FILE.read_text(encoding="utf-8").strip()
        if mode in VALID_MODES:
            return mode
    return DEFAULT_INCIDENT_MODE if DEFAULT_INCIDENT_MODE in VALID_MODES else "healthy"


def set_incident_mode(mode: str) -> None:
    if mode not in VALID_MODES:
        raise HTTPException(
            status_code=400,
            detail=f"invalid mode {mode}; valid modes are {sorted(VALID_MODES)}",
        )
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(mode, encoding="utf-8")


def delivery_context(region: str | None = None) -> dict[str, Any]:
    return {
        "patient": random.choice(PATIENTS),
        "region": region or random.choice(REGIONS),
        "delivery_window": random.choice(WINDOWS),
        "priority": random.choice(["cold-chain", "cold-chain", "clinic-coordinated"]),
        "route_id": f"rx-{random.randint(1200, 9999)}",
    }


def add_business_attributes(span: trace.Span, context: dict[str, Any], capability: str) -> None:
    span.set_attribute("business.service", "Medication Delivery Promise")
    span.set_attribute("business.capability", capability)
    span.set_attribute("business.transaction", "patient-delivery-confirmation")
    span.set_attribute("business.criticality", "high")
    span.set_attribute("delivery.region", context.get("region", "unknown"))
    span.set_attribute("delivery.window", context.get("delivery_window", "unknown"))
    span.set_attribute("delivery.priority", context.get("priority", "unknown"))
    span.set_attribute("app.issue_mode", incident_mode())
    span.set_attribute("service.version", SERVICE_VERSION)


def request_json(method: str, url: str, **kwargs: Any) -> dict[str, Any]:
    try:
        response = requests.request(method, url, timeout=6, **kwargs)
    except requests.RequestException as exc:
        span = trace.get_current_span()
        span.record_exception(exc)
        span.set_status(Status(StatusCode.ERROR, str(exc)))
        raise HTTPException(status_code=502, detail=f"request failed: {url}") from exc

    if response.status_code >= 400:
        trace.get_current_span().set_status(
            Status(StatusCode.ERROR, f"{url} returned {response.status_code}")
        )
        raise HTTPException(status_code=502, detail=response.text[:200])

    return response.json()


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service_role": SERVICE_ROLE,
        "version": SERVICE_VERSION,
        "incident_mode": incident_mode(),
    }


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> str:
    if SERVICE_ROLE != "patient-portal":
        return f"<h1>{html.escape(SERVICE_ROLE)}</h1><p>status: ok</p>"

    mode = incident_mode()
    if mode == "patient-portal-slow":
        time.sleep(1.2)

    rum_script = rum_bootstrap()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Meridian Patient Delivery</title>
  {rum_script}
  <style>
    body {{ font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: #f6f8fb; color: #17202a; }}
    header {{ background: #ffffff; border-bottom: 1px solid #d9e1ea; padding: 24px 32px; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 28px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    h2 {{ margin-top: 0; font-size: 18px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }}
    .panel {{ background: #ffffff; border: 1px solid #d9e1ea; border-radius: 8px; padding: 18px; }}
    .metric {{ font-size: 32px; font-weight: 700; margin: 8px 0; }}
    .muted {{ color: #5c6b7a; }}
    .mode {{ display: inline-block; padding: 4px 8px; border-radius: 999px; background: #e8eef6; font-weight: 600; }}
    .buttons {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }}
    button {{ border: 1px solid #aab7c4; background: #ffffff; border-radius: 6px; padding: 10px 12px; cursor: pointer; font-weight: 600; }}
    button.primary {{ background: #0064d2; border-color: #0064d2; color: #ffffff; }}
    pre {{ background: #111827; color: #e5e7eb; border-radius: 8px; padding: 14px; overflow: auto; min-height: 110px; }}
  </style>
</head>
<body>
  <header>
    <h1 data-rum-allow-text>Meridian Specialty Pharmacy</h1>
    <div class="muted">Medication delivery promise control room</div>
  </header>
  <main>
    <section class="panel">
      <h2>Morning delivery risk</h2>
      <p>The operating promise is simple: every confirmed refrigerated medication delivery arrives inside the patient delivery window.</p>
      <p>Current incident mode: <span class="mode" id="mode" data-rum-allow-text>{html.escape(mode)}</span></p>
      <div class="buttons">
        <button class="primary" onclick="confirmDelivery()">Confirm patient delivery</button>
        <button onclick="loadSummary()">Refresh health summary</button>
        <button onclick="setMode('healthy')">Healthy</button>
        <button onclick="setMode('geocode-latency')">Geocode latency</button>
        <button onclick="setMode('queue-backlog')">Queue backlog</button>
        <button onclick="setMode('patient-portal-slow')">Slow portal</button>
      </div>
    </section>

    <section class="grid" style="margin-top: 16px;">
      <div class="panel">
        <h2>At-risk routes</h2>
        <div class="metric" id="risk" data-rum-allow-text>--</div>
        <div class="muted">Calculated from route planner and dispatch queue signals.</div>
      </div>
      <div class="panel">
        <h2>Oldest pending route</h2>
        <div class="metric" id="queue" data-rum-allow-text>--</div>
        <div class="muted">The KPI that should turn yellow before dispatch calls spike.</div>
      </div>
      <div class="panel">
        <h2>Route planner p95 proxy</h2>
        <div class="metric" id="latency" data-rum-allow-text>--</div>
        <div class="muted">Use this as the simple latency KPI in ITSI.</div>
      </div>
    </section>

    <section class="panel" style="margin-top: 16px;">
      <h2>Last action</h2>
      <pre id="output"></pre>
    </section>
  </main>
  <script>
    async function api(path, options) {{
      const response = await fetch(path, options || {{}});
      const json = await response.json();
      document.getElementById('output').textContent = JSON.stringify(json, null, 2);
      return json;
    }}
    async function loadSummary() {{
      const json = await api('/api/summary');
      document.getElementById('mode').textContent = json.incident_mode;
      document.getElementById('risk').textContent = json.at_risk_routes;
      document.getElementById('queue').textContent = json.oldest_pending_route_age_seconds + 's';
      document.getElementById('latency').textContent = json.route_planner_latency_ms + 'ms';
    }}
    async function confirmDelivery() {{
      await api('/api/confirm', {{ method: 'POST' }});
      await loadSummary();
    }}
    async function setMode(mode) {{
      await api('/workshop/incident/' + mode, {{ method: 'POST' }});
      await loadSummary();
    }}
    loadSummary();
  </script>
</body>
</html>"""


def rum_bootstrap() -> str:
    token = os.getenv("SPLUNK_RUM_ACCESS_TOKEN", "")
    if not token:
        return ""
    realm = os.getenv("SPLUNK_RUM_REALM", "us1")
    app_name = os.getenv("SPLUNK_RUM_APPLICATION_NAME", "meridian-patient-portal")
    environment = os.getenv("SPLUNK_RUM_ENVIRONMENT", "meridian-workshop")
    version = os.getenv("SPLUNK_RUM_APP_VERSION", SERVICE_VERSION)
    agent_version = os.getenv("SPLUNK_RUM_AGENT_VERSION", "v3")
    return f"""
  <script src="https://cdn.observability.splunkcloud.com/o11y-gdi-rum/{agent_version}/splunk-otel-web.js" crossorigin="anonymous"></script>
  <script>
    if (window.SplunkRum) {{
      window.SplunkRum.init({{
        realm: "{html.escape(realm)}",
        rumAccessToken: "{html.escape(token)}",
        applicationName: "{html.escape(app_name)}",
        version: "{html.escape(version)}",
        deploymentEnvironment: "{html.escape(environment)}",
        user: {{ trackingMode: "anonymousTracking" }},
        spaMetrics: true,
        instrumentations: {{ visibility: true, interactions: true }}
      }});
    }}
  </script>"""


@app.get("/api/summary")
def summary() -> dict[str, Any]:
    context = delivery_context()
    span = trace.get_current_span()
    add_business_attributes(span, context, "Patient Confirmation")

    if SERVICE_ROLE != "patient-portal":
        raise HTTPException(status_code=404, detail="summary is served by patient-portal")

    if incident_mode() == "patient-portal-slow":
        time.sleep(0.8)

    route_stats = request_json("GET", f"{ROUTE_PLANNER_URL}/stats")
    notification = request_json("GET", f"{NOTIFICATION_URL}/health")
    courier = request_json("GET", f"{COURIER_API_URL}/health")

    return {
        "incident_mode": incident_mode(),
        "service": "Medication Delivery Promise",
        "at_risk_routes": route_stats["at_risk_routes"],
        "oldest_pending_route_age_seconds": route_stats["oldest_pending_route_age_seconds"],
        "route_planner_latency_ms": route_stats["route_planner_latency_ms"],
        "notification_gateway": notification["status"],
        "courier_mobile_api": courier["status"],
    }


@app.post("/api/confirm")
def confirm_delivery(region: str | None = None) -> dict[str, Any]:
    if SERVICE_ROLE != "patient-portal":
        raise HTTPException(status_code=404, detail="confirmation is served by patient-portal")

    context = delivery_context(region)
    span = trace.get_current_span()
    add_business_attributes(span, context, "Patient Confirmation")
    start = time.time()

    route = request_json("POST", f"{ROUTE_PLANNER_URL}/plan", json=context)
    courier = request_json("POST", f"{COURIER_API_URL}/accept-route", json=route)
    notification = request_json(
        "POST",
        f"{NOTIFICATION_URL}/notify",
        json={
            "patient": context["patient"],
            "route_id": route["route_id"],
            "delivery_window": context["delivery_window"],
        },
    )

    duration_ms = round((time.time() - start) * 1000, 2)
    span.set_attribute("delivery.confirmation.duration_ms", duration_ms)
    logger.info(
        "Confirmed delivery route_id=%s region=%s duration_ms=%s mode=%s",
        route["route_id"],
        context["region"],
        duration_ms,
        incident_mode(),
    )
    return {
        "status": "confirmed",
        "duration_ms": duration_ms,
        "delivery": context,
        "route": route,
        "courier": courier,
        "notification": notification,
    }


@app.get("/workshop/incident")
def get_incident() -> dict[str, Any]:
    return {"incident_mode": incident_mode(), "valid_modes": sorted(VALID_MODES)}


@app.post("/workshop/incident/{mode}")
def update_incident(mode: str) -> dict[str, str]:
    set_incident_mode(mode)
    logger.warning("Incident mode changed mode=%s", mode)
    return {"incident_mode": mode}


@app.post("/plan")
def plan_route(payload: dict[str, Any]) -> dict[str, Any]:
    if SERVICE_ROLE != "route-planner-api":
        raise HTTPException(status_code=404, detail="route planning is served by route-planner-api")

    span = trace.get_current_span()
    add_business_attributes(span, payload, "Route Planning")
    start = time.time()

    geocode = request_json(
        "GET",
        f"{GEOCODING_URL}/geocode",
        params={"region": payload.get("region", "unknown")},
    )

    mode = incident_mode()
    if mode == "queue-backlog":
        time.sleep(0.7)
    elif mode == "geocode-latency":
        time.sleep(0.25)

    duration_ms = round((time.time() - start) * 1000, 2)
    queue_age = queue_age_seconds(mode)
    at_risk = at_risk_routes(mode)

    span.set_attribute("route_planner.duration_ms", duration_ms)
    span.set_attribute("dispatch.oldest_pending_route_age_seconds", queue_age)
    span.set_attribute("dispatch.at_risk_routes", at_risk)

    if mode in {"geocode-latency", "queue-backlog"}:
        logger.warning(
            "Route planning degraded mode=%s duration_ms=%s queue_age=%s at_risk=%s",
            mode,
            duration_ms,
            queue_age,
            at_risk,
        )

    return {
        "route_id": payload.get("route_id") or f"rx-{random.randint(1200, 9999)}",
        "region": payload.get("region", "unknown"),
        "delivery_window": payload.get("delivery_window", "unknown"),
        "geocode": geocode,
        "duration_ms": duration_ms,
        "oldest_pending_route_age_seconds": queue_age,
        "at_risk_routes": at_risk,
    }


@app.get("/stats")
def stats() -> dict[str, Any]:
    if SERVICE_ROLE != "route-planner-api":
        raise HTTPException(status_code=404, detail="stats are served by route-planner-api")
    mode = incident_mode()
    latency = {
        "healthy": random.randint(75, 160),
        "geocode-latency": random.randint(850, 1500),
        "queue-backlog": random.randint(350, 700),
        "patient-portal-slow": random.randint(80, 180),
    }[mode]
    return {
        "incident_mode": mode,
        "route_planner_latency_ms": latency,
        "oldest_pending_route_age_seconds": queue_age_seconds(mode),
        "at_risk_routes": at_risk_routes(mode),
    }


@app.get("/geocode")
def geocode(region: str = "unknown") -> dict[str, Any]:
    if SERVICE_ROLE != "geocoding-provider":
        raise HTTPException(status_code=404, detail="geocoding is served by geocoding-provider")

    mode = incident_mode()
    span = trace.get_current_span()
    span.set_attribute("business.capability", "Route Planning")
    span.set_attribute("delivery.region", region)
    span.set_attribute("app.issue_mode", mode)

    if mode == "geocode-latency":
        time.sleep(random.uniform(0.9, 1.6))
        if random.random() < 0.12:
            span.set_status(Status(StatusCode.ERROR, "geocoding provider timeout"))
            raise HTTPException(status_code=503, detail="geocoding provider timeout")

    return {
        "status": "matched",
        "region": region,
        "confidence": round(random.uniform(0.88, 0.99), 3),
    }


@app.post("/accept-route")
def accept_route(payload: dict[str, Any]) -> dict[str, Any]:
    if SERVICE_ROLE != "courier-mobile-api":
        raise HTTPException(status_code=404, detail="route acceptance is served by courier-mobile-api")
    span = trace.get_current_span()
    add_business_attributes(span, payload, "Courier Updates")
    time.sleep(random.uniform(0.04, 0.12))
    return {
        "status": "accepted",
        "route_id": payload.get("route_id", "unknown"),
        "courier_id": f"drv-{random.randint(200, 499)}",
    }


@app.post("/notify")
def notify(payload: dict[str, Any]) -> dict[str, Any]:
    if SERVICE_ROLE != "notification-gateway":
        raise HTTPException(status_code=404, detail="notification is served by notification-gateway")
    span = trace.get_current_span()
    span.set_attribute("business.capability", "Patient Notifications")
    span.set_attribute("notification.channel", "sms")
    span.set_attribute("app.issue_mode", incident_mode())
    time.sleep(random.uniform(0.03, 0.09))
    return {
        "status": "sent",
        "channel": "sms",
        "route_id": payload.get("route_id", "unknown"),
    }


def queue_age_seconds(mode: str) -> int:
    if mode == "healthy":
        return random.randint(12, 45)
    if mode == "geocode-latency":
        return random.randint(120, 260)
    if mode == "queue-backlog":
        return random.randint(360, 840)
    return random.randint(20, 60)


def at_risk_routes(mode: str) -> int:
    if mode == "healthy":
        return random.randint(0, 2)
    if mode == "geocode-latency":
        return random.randint(8, 17)
    if mode == "queue-backlog":
        return random.randint(18, 38)
    return random.randint(1, 4)


def run_loadgen() -> None:
    interval = float(os.getenv("MERIDIAN_LOAD_INTERVAL_SECONDS", "2.0"))
    logger.info("Starting Meridian loadgen target=%s interval=%s", PATIENT_PORTAL_URL, interval)
    while True:
        try:
            if random.random() < 0.75:
                response = requests.post(
                    f"{PATIENT_PORTAL_URL}/api/confirm",
                    params={"region": random.choice(REGIONS)},
                    timeout=8,
                )
            else:
                response = requests.get(f"{PATIENT_PORTAL_URL}/api/summary", timeout=8)
            logger.info("loadgen status=%s path=%s", response.status_code, response.url)
        except requests.RequestException as exc:
            logger.exception("loadgen request failed: %s", exc)
        time.sleep(interval)


if __name__ == "__main__":
    if SERVICE_ROLE == "loadgen":
        run_loadgen()
    else:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
