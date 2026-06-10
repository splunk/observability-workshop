import logging
import os
import random
import time

from fastapi import FastAPI, HTTPException, Query
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("inventory-service")

app = FastAPI(title="On-Call Workshop Inventory Service")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")
VALID_MODES = {"healthy", "latency", "errors", "latency-errors"}
state = {"mode": os.getenv("ISSUE_MODE", "healthy")}


def current_mode() -> str:
    mode = state.get("mode", "healthy")
    if mode not in VALID_MODES:
        return "healthy"
    return mode


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "inventory-service",
        "version": SERVICE_VERSION,
        "issue_mode": current_mode(),
    }


@app.get("/mode")
def get_mode():
    return {
        "service": "inventory-service",
        "issue_mode": current_mode(),
        "valid_modes": sorted(VALID_MODES),
    }


@app.post("/mode")
def set_mode(mode: str = Query(..., description="healthy, latency, errors, or latency-errors")):
    if mode not in VALID_MODES:
        raise HTTPException(status_code=400, detail=f"mode must be one of {sorted(VALID_MODES)}")
    state["mode"] = mode
    logger.warning("Issue mode changed to %s", mode)
    return {
        "service": "inventory-service",
        "issue_mode": mode,
        "message": "inventory issue mode updated",
    }


@app.get("/reserve")
def reserve(sku: str, quantity: int = 1, cart: str = "standard"):
    span = trace.get_current_span()
    mode = current_mode()
    error_rate = float(os.getenv("ERROR_RATE", "0.65"))
    latency_ms = int(os.getenv("LATENCY_MS", "2200"))

    span.set_attribute("app.issue_mode", mode)
    span.set_attribute("app.sku", sku)
    span.set_attribute("app.quantity", quantity)
    span.set_attribute("app.cart.type", cart)
    span.set_attribute("service.version", SERVICE_VERSION)

    if mode in ("latency", "latency-errors"):
        jitter_ms = random.randint(0, 750)
        sleep_seconds = (latency_ms + jitter_ms) / 1000
        logger.warning("Injecting inventory latency sleep_seconds=%s sku=%s cart=%s", sleep_seconds, sku, cart)
        time.sleep(sleep_seconds)

    if mode in ("errors", "latency-errors") and random.random() < error_rate:
        message = f"inventory reservation failed for sku={sku}"
        span.set_status(Status(StatusCode.ERROR, message))
        logger.error(message)
        raise HTTPException(status_code=503, detail=message)

    logger.info("Inventory reserved sku=%s quantity=%s cart=%s mode=%s", sku, quantity, cart, mode)
    return {
        "status": "reserved",
        "sku": sku,
        "quantity": quantity,
        "cart": cart,
        "issue_mode": mode,
    }
