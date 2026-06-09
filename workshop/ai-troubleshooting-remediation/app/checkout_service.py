import logging
import os
import random
import time

import requests
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("checkout-service")

app = FastAPI(title="AI Remediation Checkout Service")
tracer = trace.get_tracer(__name__)

INVENTORY_URL = os.getenv("INVENTORY_URL", "http://inventory-service:8081")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "checkout-service", "version": SERVICE_VERSION}


@app.get("/checkout")
def checkout(cart: str = "standard"):
    start = time.time()
    span = trace.get_current_span()
    sku = random.choice(["camera", "headphones", "speaker", "laptop"])
    quantity = random.choice([1, 1, 1, 2])
    cart_value = random.choice([49, 79, 149, 299, 499])

    span.set_attribute("app.cart.type", cart)
    span.set_attribute("app.cart.value", cart_value)
    span.set_attribute("app.sku", sku)
    span.set_attribute("service.version", SERVICE_VERSION)

    with tracer.start_as_current_span("checkout.reserve_inventory") as reserve_span:
        reserve_span.set_attribute("app.sku", sku)
        reserve_span.set_attribute("app.quantity", quantity)
        try:
            response = requests.get(
                f"{INVENTORY_URL}/reserve",
                params={"sku": sku, "quantity": quantity, "cart": cart},
                timeout=5,
            )
        except requests.RequestException as exc:
            reserve_span.record_exception(exc)
            reserve_span.set_status(Status(StatusCode.ERROR, str(exc)))
            span.set_status(Status(StatusCode.ERROR, "inventory request failed"))
            logger.exception("Inventory request failed")
            raise HTTPException(status_code=502, detail="inventory request failed") from exc

        if response.status_code >= 400:
            reserve_span.set_attribute("http.response.status_code", response.status_code)
            reserve_span.set_status(Status(StatusCode.ERROR, response.text[:120]))
            span.set_status(Status(StatusCode.ERROR, "inventory returned an error"))
            logger.error(
                "Inventory returned error status=%s body=%s",
                response.status_code,
                response.text[:200],
            )
            raise HTTPException(status_code=502, detail="inventory returned an error")

    duration_ms = round((time.time() - start) * 1000, 2)
    span.set_attribute("app.checkout.duration_ms", duration_ms)
    logger.info("Checkout completed sku=%s cart=%s duration_ms=%s", sku, cart, duration_ms)
    return {
        "status": "accepted",
        "sku": sku,
        "quantity": quantity,
        "cart": cart,
        "cart_value": cart_value,
        "duration_ms": duration_ms,
        "inventory": response.json(),
    }

