---
title: ワークショップ概要
linkTitle: 1. ワークショップ概要
weight: 1
time: 5 minutes
description: ワークショップの目標とアーキテクチャについて説明します。
---

## はじめに

多くの企業では、**リバースプロキシ、API ゲートウェイ、またはサービスメッシュ**を運用しており、これらが未知の HTTP ヘッダー（W3C Trace Context ヘッダーである `traceparent`、`tracestate`、場合によっては `baggage` を含む）を除去することがあります。この場合、OpenTelemetry の自動プロパゲーションが機能しなくなり、トレースが無関係なルートに分断されます。

このハンズオンワークショップでは、Python マイクロサービスに **Splunk OpenTelemetry** を実装し、nginx が W3C ヘッダーを除去した際に**分散トレースが破損する**状況を再現し、**手動コンテキストの inject/extract** でプロパゲーションを修正し、**Splunk Observability Cloud** で検証します。

## ワークショップの構成（約75分）

| # | モジュール | 時間 |
| - | ------ | ---- |
| 1 | [前提条件](docs/workshop/1-prerequisites.md) | 5 min |
| 2 | [アプリケーションサービスのデプロイ](docs/workshop/2-deploy-services.md) | 10 min |
| 3 | [Splunk OTel Collector のデプロイ](docs/workshop/3-deploy-collector.md) | 10 min |
| 4 | [手動コンテキストプロパゲーション](docs/workshop/4-manual-propagation.md) | 30 min |
| 5 | [Tag Spotlight](docs/workshop/5-tag-spotlight.md) | 15 min |
| 6 | [まとめ](docs/workshop/6-summary.md) | 5 min |

## アプリケーションアーキテクチャ

### リクエストフロー（アプリケーションデータ）

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
