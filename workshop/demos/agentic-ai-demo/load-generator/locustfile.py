from locust import HttpUser, task, between, constant, events
from locust.env import Environment
import random
import os

# Demo data
CUSTOMER_IDS = [1, 2, 3, 4, 5]
STORE_IDS = [1, 2, 3, 4, 5]
PRODUCT_SKUS = [
    "COF-ETH-LG-12",
    "COF-COL-DR-12",
    "ACC-FRP-1L",
    "ACC-MUG-12",
    "ACC-FLT-RUS",
    "COF-GUA-MD-12",
    "ACC-TUM-16",
    "KIT-CB-START",
    "COF-ESP-12",
    "ACC-SCP-2TB",
    "COF-DEC-ORG-12",
    "KIT-POUR-SET",
    "MAC-DRIP-12",
    "ACC-FROTH-HH",
    "ACC-GLS-16",
    "COF-CR-SO-12",
    "ACC-TRAV-20",
    "ACC-TOTE",
    "GIFTCARD25",
    "KIT-SAMPLER",
    "COF-HON-HNY-12",
    "COF-VIE-ROB-12",
    "ACC-CAR-15",
    "MAC-STOVE-6",
    "ACC-PITCH-12",
    "COF-NIC-SO-12",
    "ACC-FRP-MINI",
    "COF-CB-CONC-32",
    "ACC-ESP-4SET",
    "ACC-FILT-100",
    "COF-HOUSE-12",
    "MAC-GRIND-BR",
    "COF-BRA-CER-12",
    "ACC-TAMP-58",
    "COF-KEN-AA-12",
    "ACC-STRAW-SET",
    "KIT-SYRUP",
    "ACC-MUG-MOCHA",
    "COF-HAZ-12",
    "COF-FR-ORG-12",
    "ACC-JAR-1L",
    "ACC-SCALE",
    "COF-RWA-BRB-12",
    "ACC-SYRUP-VAN",
    "ACC-FLT-SS",
    "GIFTCARD50",
    "COF-COL-DEC-12",
    "APP-HOOD-M",
    "APP-HOOD-L",
]

def build_order_request():
    # Choose 1–3 unique SKUs and 1–3 quantity for each.
    n_items = random.randint(1, 3)
    skus = random.sample(PRODUCT_SKUS, n_items)
    item_phrases = []
    for sku in skus:
        qty = random.randint(1, 3)
        item_phrases.append(f"{qty} of sku {sku}")
    items_text = " and ".join(item_phrases)
    store_id = random.choice(STORE_IDS)
    return f"I'd like to order {items_text}, for pickup at store_id {store_id}."

def build_insecure_order_request():
    # take a regular order request and make it insecure by adding a credit card number
    secure_order_request = build_order_request()
    return f" My credit card number is 5555555555554444."

def build_previous_order_question():
    return "What products were included in my most recent order?"

def build_product_info_question():
    # Keep your example; you can add more variations if desired.
    return "What's the most expensive product you sell?"

def build_inventory_question():
    sku = random.choice(PRODUCT_SKUS)
    # Ask for all stores 1, 2, and 3 as in your example.
    return f"What is the inventory for product_sku {sku} at store_id 1, 2, and 3?"

def choose_request_text():
    """
    Return (kind, request_text) where kind is used to name the request in Locust UI.
    Weighted to send more 'order' traffic, with a mix of questions.
    """
    r = random.random()
    if r < 0.10:
        return ("order", build_insecure_order_request())
    elif r < 0.35:
        return ("order", build_order_request())
    elif r < 0.50:
        return ("previous_orders", build_previous_order_question())
    elif r < 0.80:
        return ("product_info", build_product_info_question())
    else:
        return ("inventory", build_inventory_question())

class ChatUser(HttpUser):
    host = f"http://{os.getenv('APP_ADDR')}"
    wait_time = between(30, 90)

    @task
    def chat(self):
        customer_id = random.choice(CUSTOMER_IDS)
        kind, request_text = choose_request_text()

        payload = {
            "customer_id": customer_id,
            "request": request_text,
        }

        # Name the request so you can see breakdown in Locust UI.
        with self.client.post(
            "/chat",
            json=payload,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            name=f"chat:{kind}",
            catch_response=True,
        ) as resp:
            # Mark failures in the UI if status is not 2xx.
            if resp.status_code < 200 or resp.status_code >= 300:
                resp.failure(f"HTTP {resp.status_code}: {resp.text}")

# New HttpUser class for the periodic inventory refresh
class InventoryRefresher(HttpUser):
    host = f"http://{os.getenv('APP_ADDR')}"
    # Wait exactly 1 hour (3600 seconds) between calls for each user of this type.
    wait_time = constant(3600)

    @task
    def refresh_inventory(self):
        with self.client.get(
            "/refresh_inventory",
            name="Inventory Refresh: /refresh_inventory", # Name for Locust UI
            catch_response=True,
        ) as resp:
            if resp.status_code < 200 or resp.status_code >= 300:
                resp.failure(f"HTTP {resp.status_code}: {resp.text}")
            else:
                resp.success() # Explicitly mark success if needed, though 2xx is default success.

# New HttpUser class for the periodic order archival
class ArchiveOrders(HttpUser):
    host = f"http://{os.getenv('APP_ADDR')}"
    # Wait exactly 6 hours (21,600 seconds) between calls for each user of this type.
    wait_time = constant(21600)

    @task
    def archive_orders(self):
        with self.client.get(
            "/archive_orders",
            name="Archive Orders: /archive_orders", # Name for Locust UI
            catch_response=True,
        ) as resp:
            if resp.status_code < 200 or resp.status_code >= 300:
                resp.failure(f"HTTP {resp.status_code}: {resp.text}")
            else:
                resp.success() # Explicitly mark success if needed, though 2xx is default success.

# This function will be called when Locust initializes
@events.init.add_listener
def on_locust_init(environment: Environment, **kwargs):
    # Set the user classes and their weights
    # For 1 user of each, you can assign them equal weights.
    # Locust will then distribute the total --users count proportionally.
    # If you specify --users 2, it will spawn 1 of each.
    environment.user_classes = {
        ChatUser: 1, # Weight of 1 for ChatUser
        InventoryRefresher: 1, # Weight of 1 for InventoryRefresher
        ArchiveOrders: 1 # Weight of 1 for ArchiveOrders
    }
    # If you were to run with --users 30, it would spawn 1 ChatUsers, 1 InventoryRefreshers, and 1 ArchiveOrders.
    # Since we want exactly 1 of each, we'll set --users to 3 in the CMD.