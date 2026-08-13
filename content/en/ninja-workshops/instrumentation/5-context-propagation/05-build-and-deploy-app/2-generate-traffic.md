---
title: Generate Traffic
linkTitle: 2. Generate Traffic
weight: 2
time: 15 minutes

---

In this step, you'll generate traffic through Cosmic Observatory Shop. 

## Access the Application

From your laptop, open a new ssh window and type

```
ssh -p 2222 \
  -L 30080:localhost:30080 \
  -L 15672:localhost:15672 \
  user@1.111.11.111 //Change this to your actual ssh user & IP Address for your instsance
```

Keep that session open. Then Open the Cosmic Observatory Shop in your browser:

```
http://localhost:30080
```
You should see the astronomy equipment catalog with telescopes, eyepieces, and astrophotography gear...

![cosmic-shop](../images/cosmic-shop.png)

Optional - RabbitMQ management UI: (login: `guest` / `guest`)
```
http://localhost:15672 
```
![rabbitmq](../images/rabbitmq.png)

If the UI does not load, verify the loadbalancer port and use port-forward:

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
kubectl -n cosmic-shop port-forward svc/rabbitmq 15672:15672
```

## Generate Initial Traffic

1. After opening the shop at http://localhost:30080
2. Enter an email address (e.g. `observer@cosmic.shop`)
3. Click **Purchase** on any product
4. Confirm the order in the modal

Repeat a few times to generate trace data.
