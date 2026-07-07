---
draft: true
title: Context Propagation
linkTitle: Context Propagation
weight: 20
layout: chapter
time: 90 minutes
authors: ["Diana Omuoyo"]
description: Distributed tracing breaks silently when proxies and message buses drop W3C trace context. This workshop contains a sample e-commerce application with some of the common context & correlation breaks  
aliases:
  - /ninja-workshops/20-context-propagation/
---

## Overview

In this workshop, you'll deploy the **Cosmic Observatory Shop** - an astronomy equipment storefront - and instrument it with Splunk RUM and Splunk APM. 

You will observe fragmented service map and traces when required W3C headers are stripped at these **three** layers. 
1. **Edge NGINX gateway** - drops W3C trace headers (frontend-api → order API)
2. **Payment gateway proxy** - instrumented Node.js proxy drops headers (frontend-api → payment API)
3. **RabbitMQ message bus** - async payment → fulfillment with no trace context in AMQP headers

We will then fix the issues to restore end-to-end context propagation across all service and infrastructure layers.


## Architecture | Expected Output

```text
Browser (RUM)
    → Frontend → Frontend API (BFF)
         ├─ catalog path ──► Catalog API
         └─ purchase workflow ──► Edge Gateway → Order API
                              └─► Payment Gateway → Payment API → RabbitMQ → Fulfillment Worker
                                        ▲                    ▲              ▲
                                   Break #1              Break #2       Break #3
                                   (Step 06)             (Step 07)      (Step 08)
```

Let's get started!

