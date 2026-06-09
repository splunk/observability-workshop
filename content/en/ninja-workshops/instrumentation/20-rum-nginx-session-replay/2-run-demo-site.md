---
title: 2. Run the Demo Site
linkTitle: 2. Run Demo
weight: 2
---

Start the sample nginx site:

```bash
cd workshop/rum-nginx-session-replay
docker compose up -d
```

Open the local page:

```text
http://localhost:8088
```

The page includes a small checkout journey that creates browser activity for RUM and DXA:

- product view and route-change activity,
- add-to-cart clicks,
- checkout start and submit clicks,
- a controlled JavaScript error,
- safe and sensitive DOM regions for RUM privacy and Session Replay controls.

## Verify the container

Check that nginx is running:

```bash
docker compose ps
```

Fetch the rendered page and look for the injected marker:

```bash
curl -s http://localhost:8088 | grep 'splunk-dxa-rum-injected'
```

Expected output:

```html
<meta name="splunk-dxa-rum-injected" content="nginx">
```

If the marker is missing, nginx did not rewrite the HTML response. The operational checklist covers the common causes.

## Generate sample browser activity

In the demo site:

1. Select a product.
2. Click **Add to cart**.
3. Click **Begin checkout**.
4. Change the shipping method.
5. Submit the checkout form.
6. Click **Trigger JavaScript error**.

Repeat the flow a few times, including one abandoned checkout where you stop after **Begin checkout**. DXA needs enough event volume to make funnel and time-series views useful.
