---
title: Workshop Overview
linkTitle: 1. Workshop Overview
weight: 1
time: 5 minutes
description: Goals and architecture for the workshop.
---

## Introduction

Many enterprises run **reverse proxies, API gateways, or service meshes** that remove unknown HTTP headers—including W3C Trace Context headers (`traceparent`, `tracestate`, and sometimes `baggage`). When that happens, automatic OpenTelemetry propagation stops working and traces fragment into unrelated roots.

In this Hands-on Workshop, we will instrument Python microservices with **Splunk OpenTelemetry**, reproduce **broken distributed traces** when nginx strips W3C headers, fix propagation with **manual context inject/extract**, and validate in **Splunk Observability Cloud**.

## Workshop Outline (~75 min)

| # | Module | Time |
| - | ------ | ---- |
| 1 | [Prerequisites](docs/workshop/1-prerequisites.md) | 5 min |
| 2 | [Deploy application services](docs/workshop/2-deploy-services.md) | 10 min |
| 3 | [Deploy Splunk OTel Collector](docs/workshop/3-deploy-collector.md) | 10 min |
| 4 | [Manual context propagation](docs/workshop/4-manual-propagation.md) | 30 min |
| 5 | [Tag Spotlight](docs/workshop/5-tag-spotlight.md) | 15 min |
| 6 | [Summary](docs/workshop/6-summary.md) | 5 min |

## Application Architecture

### Request flow (application data)

```text
Client / load-generator
    │
    ▼ HTTP
edge-proxy (nginx)
    │
    ▼ HTTP
storefront-service          ← GET /api/order
    ├──────────────────────────────┐
    ▼ HTTP                         ▼ HTTP
inventory-service            payment-proxy
GET /api/reserve                  │  (Phase 1: outbound to payment strips trace context)
                                  ▼ HTTP
                             payment-service
                             GET /api/payment/authorize
                                  │
                                  ▼ HTTP
                             order-service
                             GET /api/order/quote
                                  │
                                  ▼ AMQP publish (Phase 1: no trace headers on messages)
                             RabbitMQ  (workshop.quote.request)
                                  │
                                  ▼ AMQP consume
                             fulfilment-service
                                  │
                                  ▼ HTTP POST
                             email-service
                             /api/email/send-confirmation
```
