---
title: "フェーズ 1: Docker -- OBI 導入前"
linkTitle: 3. OBI 導入前の Docker
weight: 3
archetype: chapter
time: 15 minutes
description: Docker Compose で 3 つのマイクロサービスをデプロイし、APM が空であることを確認します。計装がないため、トレースは存在しません。
---

このフェーズでは、ポリグロットなマイクロサービススタックをデプロイし、「導入前」の状態を確認します。インフラストラクチャメトリクスはSplunkに送信されますが、アプリケーションには計装が一切されていないため、APMにはトレースがありません。

```text
Frontend (Node.js :3000)  →  Order-Processor (Go :8080)  →  Payment-Service (Go :8081)
```
