# Context Propagation Workshop

Distributed tracing breaks silently when proxies and message buses drop W3C trace context. This repository contains **Cosmic Observatory Shop** — an astronomy e-commerce demo with **three deliberate correlation breaks**:

1. **Edge NGINX gateway** — strips headers from browser → order API
2. **Payment gateway proxy** — instrumented Node.js proxy strips headers from order → payment API (visible in Splunk APM service map)
3. **RabbitMQ** — async payment → fulfillment with no trace context in message headers

## Quick start

```bash
cp .env.example .env
# Edit .env with Splunk credentials

make setup-k3d
make build
make deploy          # auto-installs Splunk OTel Collector if missing
open http://localhost:30080
```

## Services

| Service | Port | Stage |
|---------|------|-------|
| frontend | 30080 (k3d) | Shop UI + Splunk RUM |
| gateway | — | Edge NGINX proxy |
| order-api | 3001 | Order placement |
| payment-gateway | 3004 | Payment proxy (APM-visible) |
| payment-api | 3005 | Payment + RabbitMQ publish |
| fulfillment-worker | 3006 | Async fulfillment consumer |
| catalog-api | 3002 | Product catalog |
| rabbitmq | 15672 | Management UI (guest/guest) |

**RabbitMQ UI not loading?** Verify k3d mapped the port, then port-forward if needed:

```bash
docker ps --filter name=k3d-cosmic-shop-serverlb --format '{{.Ports}}'
kubectl -n cosmic-shop port-forward svc/rabbitmq 15672:15672
```

## Cleanup

```bash
make cleanup              # Full teardown: k3d cluster, collector, images, Compose
make cleanup-apps         # Remove apps only; keep k3d cluster
```
