---
title: "Phase 1: Docker (Before OBI)"
linkTitle: 3. Docker Before OBI
weight: 3
archetype: chapter
time: 15 minutes
description: Docker Compose で 3 つのマイクロサービスをデプロイし、APM が空であることを確認します。インストルメンテーションがないため、トレースは一切存在しません。
---

このフェーズでは、ポリグロット（またこの言葉です！）なマイクロサービススタックをデプロイし、「Before」の状態を確立します。インフラストラクチャメトリクスは Splunk に流れますが、アプリケーションにはインストルメンテーションが一切ないため、APM にトレースは 1 件もありません。

```text
Frontend (Node.js :3000)  →  Order-Processor (Go :8080)  →  Payment-Service (Go :8081)
```
