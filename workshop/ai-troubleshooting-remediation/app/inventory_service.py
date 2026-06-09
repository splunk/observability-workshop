import logging
import os
import random
import sys
import time

from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("inventory-service")

ISSUE_MODE = os.getenv("ISSUE_MODE", "healthy")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")

if ISSUE_MODE == "crashloop":
    logger.error("ISSUE_MODE=crashloop, exiting to create a Kubernetes restart signal")
    sys.exit(1)

app = FastAPI(title="AI Remediation Inventory Service")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "inventory-service",
        "version": SERVICE_VERSION,
        "issue_mode": ISSUE_MODE,
    }


@app.get("/reserve")
def reserve(sku: str, quantity: int = 1, cart: str = "standard"):
    span = trace.get_current_span()
    mode = os.getenv("ISSUE_MODE", ISSUE_MODE)
    error_rate = float(os.getenv("ERROR_RATE", "0.65"))
    latency_ms = int(os.getenv("LATENCY_MS", "2200"))

    span.set_attribute("app.issue_mode", mode)
    span.set_attribute("app.sku", sku)
    span.set_attribute("app.quantity", quantity)
    span.set_attribute("app.cart.type", cart)
    span.set_attribute("service.version", SERVICE_VERSION)

    if mode in ("latency", "latency-errors"):
        jitter_ms = random.randint(0, 650)
        sleep_seconds = (latency_ms + jitter_ms) / 1000
        logger.warning("Injecting latency sleep_seconds=%s sku=%s", sleep_seconds, sku)
        time.sleep(sleep_seconds)

    if mode in ("errors", "latency-errors") and random.random() < error_rate:
        message = f"inventory reservation failed for sku={sku}"
        span.set_status(Status(StatusCode.ERROR, message))
        logger.error(message)
        raise HTTPException(status_code=503, detail=message)

    logger.info("Inventory reserved sku=%s quantity=%s cart=%s", sku, quantity, cart)
    return {
        "status": "reserved",
        "sku": sku,
        "quantity": quantity,
        "cart": cart,
        "issue_mode": mode,
    }

