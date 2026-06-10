import logging
import os
import random
import time

import requests


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("checkout-loadgen")

TARGET_URL = os.getenv("TARGET_URL", "http://checkout-service:8080/checkout")
INTERVAL_SECONDS = float(os.getenv("REQUEST_INTERVAL_SECONDS", "1.0"))
CARTS = ["standard", "express", "enterprise", "bulk"]


def main():
    logger.info("Starting checkout load generator target=%s interval=%s", TARGET_URL, INTERVAL_SECONDS)
    while True:
        cart = random.choice(CARTS)
        try:
            response = requests.get(TARGET_URL, params={"cart": cart}, timeout=10)
            logger.info("Checkout request cart=%s status=%s", cart, response.status_code)
        except requests.RequestException as exc:
            logger.exception("Checkout request failed: %s", exc)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
