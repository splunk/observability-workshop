import base64

from locust import HttpUser, TaskSet, task, between
from random import randint, choice
from io import BytesIO


class WebTasks(TaskSet):

    @task
    def load(self):
        string = ('{0}:{1}'.format('user', 'password').replace('\n', '').encode("utf-8"))

        base64string = base64.b64encode(string)

        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("/")
        self.client.get("/login", headers={"Authorization" : "Basic {0}".format(str(base64string, 'utf-8'))})
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")


class Web(HttpUser):
    tasks = [WebTasks]
    wait_time = between(0, 0)
