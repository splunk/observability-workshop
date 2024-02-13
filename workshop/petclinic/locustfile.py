import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.get("/")

    @task(3)
    def view_items(self):
        for item_id in range(1, 10):
            self.client.get(f"/owners/{item_id}", name="/owners")
            time.sleep(1)
