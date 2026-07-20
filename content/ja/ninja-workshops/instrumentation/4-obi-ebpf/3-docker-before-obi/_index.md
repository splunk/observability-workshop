---
title: "フェーズ1: Docker（OBI導入前）"
linkTitle: 3. Docker Before OBI
weight: 3
archetype: chapter
time: 15 minutes
description: Docker Composeで3つのマイクロサービスをデプロイし、APMが空であることを確認します。計装がないためトレースは存在しません。
---

このフェーズでは、ポリグロット（またこの言葉です!）マイクロサービススタックをデプロイし、「導入前」の状態を確認します。インフラストラクチャメトリクスはSplunkに送信されますが、アプリケーションにはまったく計装がないため、APMにはトレースがゼロです。

```text
Frontend (Node.js :3000)  →  Order-Processor (Go :8080)  →  Payment-Service (Go :8081)
```
