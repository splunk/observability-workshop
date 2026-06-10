import logging
import os
import random
import time

import requests
from fastapi import FastAPI, HTTPException, Query
from opentelemetry import metrics, trace
from opentelemetry.trace import Status, StatusCode


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("checkout-service")

app = FastAPI(title="On-Call Workshop Checkout Service")
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter("on-call-workshop.checkout")

request_counter = meter.create_counter(
    "workshop.checkout.requests",
    unit="{request}",
    description="Checkout requests handled by the workshop app.",
)
error_counter = meter.create_counter(
    "workshop.checkout.errors",
    unit="{error}",
    description="Checkout requests that failed because of downstream inventory issues.",
)
latency_histogram = meter.create_histogram(
    "workshop.checkout.latency_ms",
    unit="ms",
    description="End-to-end checkout latency in milliseconds.",
)

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://inventory-service:8081")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
CARTS = ["standard", "express", "enterprise", "bulk"]
SKUS = ["camera", "headphones", "speaker", "laptop", "tablet", "watch"]


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "checkout-service",
        "version": SERVICE_VERSION,
        "inventory_url": INVENTORY_URL,
    }


@app.get("/scenario")
def scenario():
    inventory = requests.get(f"{INVENTORY_URL}/mode", timeout=3).json()
    return {
        "workshop": "on-call-incident-response",
        "service": "checkout-service",
        "detector_metrics": [
            "workshop.checkout.requests",
            "workshop.checkout.errors",
            "workshop.checkout.latency_ms",
        ],
        "inventory": inventory,
    }


@app.post("/admin/issue-mode")
def set_issue_mode(mode: str = Query(..., description="healthy, latency, errors, or latency-errors")):
    try:
        response = requests.post(f"{INVENTORY_URL}/mode", params={"mode": mode}, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("Could not update inventory issue mode")
        raise HTTPException(status_code=502, detail="could not update inventory issue mode") from exc
    return response.json()


@app.get("/checkout")
def checkout(cart: str | None = None):
    start = time.perf_counter()
    span = trace.get_current_span()
    selected_cart = cart or random.choice(CARTS)
    sku = random.choice(SKUS)
    quantity = random.choice([1, 1, 1, 2, 3])
    cart_value = random.choice([49, 79, 149, 299, 499, 799])
    status = "success"
    issue_mode = "unknown"
    http_status = 200

    span.set_attribute("app.cart.type", selected_cart)
    span.set_attribute("app.cart.value", cart_value)
    span.set_attribute("app.sku", sku)
    span.set_attribute("app.quantity", quantity)
    span.set_attribute("service.version", SERVICE_VERSION)

    try:
        with tracer.start_as_current_span("checkout.reserve_inventory") as reserve_span:
            reserve_span.set_attribute("app.sku", sku)
            reserve_span.set_attribute("app.quantity", quantity)
            reserve_span.set_attribute("app.cart.type", selected_cart)
            response = requests.get(
                f"{INVENTORY_URL}/reserve",
                params={"sku": sku, "quantity": quantity, "cart": selected_cart},
                timeout=8,
            )
            http_status = response.status_code
            reserve_span.set_attribute("http.response.status_code", http_status)

            if response.status_code >= 400:
                status = "error"
                reserve_span.set_status(Status(StatusCode.ERROR, response.text[:120]))
                span.set_status(Status(StatusCode.ERROR, "inventory returned an error"))
                logger.error("Inventory returned status=%s body=%s", response.status_code, response.text[:200])
                raise HTTPException(status_code=503, detail="inventory reservation failed")

            inventory = response.json()
            issue_mode = inventory.get("issue_mode", "unknown")

    except requests.RequestException as exc:
        status = "error"
        http_status = 502
        span.record_exception(exc)
        span.set_status(Status(StatusCode.ERROR, str(exc)))
        logger.exception("Inventory request failed")
        raise HTTPException(status_code=502, detail="inventory request failed") from exc
    finally:
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        attrs = {
            "app.cart.type": selected_cart,
            "app.issue_mode": issue_mode,
            "http.response.status_code": http_status,
            "status": status,
        }
        request_counter.add(1, attrs)
        latency_histogram.record(duration_ms, attrs)
        span.set_attribute("app.checkout.duration_ms", duration_ms)
        span.set_attribute("app.issue_mode", issue_mode)
        if status == "error":
            error_counter.add(1, attrs)

    logger.info(
        "Checkout completed cart=%s sku=%s status=%s issue_mode=%s duration_ms=%s",
        selected_cart,
        sku,
        status,
        issue_mode,
        duration_ms,
    )
    return {
        "status": "accepted",
        "sku": sku,
        "quantity": quantity,
        "cart": selected_cart,
        "cart_value": cart_value,
        "duration_ms": duration_ms,
        "inventory": inventory,
    }
